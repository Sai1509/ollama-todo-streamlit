import streamlit as st
import requests

# Adjust these if needed:
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

# System prompt for the model
SYSTEM_PROMPT = """You are a to-do list generator. Based on the user's input, 
you will create a clear and descriptive to-do list using bullet points. 
Only generate the to-do list as bullet points with some explanation and 
time frame if asked, and nothing else. Be a little descriptive."""

def generate_to_do_list(task_description: str) -> str:
    """
    Sends the user input plus a system prompt to Ollama's local API.
    Returns the resulting to-do list text or an error message.
    """
    # Build the request payload
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_description}
        ],
        "stream": False
    }

    try:
        # Send request to Ollama
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
        response.raise_for_status()  # will raise an exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        # Return the exception as a string if there's a network/HTTP error
        return f"Error connecting to Ollama API: {e}"

    # Parse the JSON response
    try:
        json_response = response.json()
        # Adapt this to your actual Ollama response structure
        return json_response.get("message", {}).get("content", "No to-do list found.")
    except Exception as e:
        return f"Error parsing JSON response: {e}"

def main():
    st.title("Ollama To-Do List Generator")
    st.write("Enter a description of what you need to do, and I'll generate a to-do list.")

    task_description = st.text_input("Task Description", "")
    
    if st.button("Generate To-Do"):
        if not task_description.strip():
            st.warning("Please enter a valid task description.")
        else:
            to_do_list = generate_to_do_list(task_description)
            
            st.subheader("Your To-Do List")
            st.write(to_do_list)
            
            # Optional: Provide a download button for the to-do list
            st.download_button(
                label="Download To-Do List",
                data=f"Your To-Do List:\n\n{to_do_list}",
                file_name="to_do_list.txt"
            )

if __name__ == "__main__":
    main()
