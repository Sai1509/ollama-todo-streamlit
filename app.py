import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import os

# Define Ollama API settings (local endpoint)
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

system_prompt = """You are a to-do list generator. Based on the user's input, you will create a clear and descriptive
to-do list using bullet points. Only generate the to-do list as bullet points with some explanation and time
frame only if asked for, and nothing else. Be a little descriptive."""

def generate_to_do_list(task_description):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_description}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"

    try:
        json_response = response.json()
        # Adjust how you parse the JSON depending on actual Ollama response structure
        to_do_list = json_response.get("message", {}).get("content", "No to-do list found.")

        formatted_output = "Your To-Do List:\n\n" + to_do_list
        file_name = "to_do_list.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(formatted_output)

        # Optionally generate a PDF here using ReportLab, if you need it:
        # pdf_name = "to_do_list.pdf"
        # c = canvas.Canvas(pdf_name, pagesize=letter)
        # c.setFont("Helvetica", 12)
        # c.drawString(72, 750, "Your To-Do List:")
        # text_object = c.beginText(72, 730)
        # text_object.setFont("Helvetica", 10)
        # for line in to_do_list.split("\n"):
        #     text_object.textLine(line)
        # c.drawText(text_object)
        # c.showPage()
        # c.save()

        return file_name
    except Exception as e:
        return f"Error parsing JSON: {e}"

def main():
    print("=== To-Do List Generator (Ollama) ===")
    task_description = input("Enter the task description for the to-do list: ")
    result = generate_to_do_list(task_description)

    if result.endswith(".txt"):
        print(f"\nTo-do list generated and saved to: {result}")
    else:
        print(f"\nSomething went wrong: {result}")

if __name__ == "__main__":
    main()
