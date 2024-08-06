import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import openai
import json
import threading
from tkinter.ttk import Progressbar
import re

# Function to attach the JSON file
def attach_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        attached_file_label.config(text=file_path)

# Function to read the attached JSON file and prepare the content for GPT-4o
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Use regex to add double quotes around keys if missing
            content = re.sub(r'(?<=[:\{\[,])(\s*)(\w+)(\s*):', r'\1"\2":', content)
            # Remove trailing commas
            content = re.sub(r',(\s*[\}\]])', r'\1', content)
            return json.loads(content)
    except (json.JSONDecodeError, ValueError) as e:
        messagebox.showerror("JSON Error", f"Failed to decode JSON: {e}")
        raise e

# Function to generate the GPT-4 prompt
def generate_prompt(json_content):
    return f"""
### JSON Key-Value Pair Discovery

The provided JSON file contains the following content:
```json
{json.dumps(json_content, indent=4)}
```

Please analyze the JSON and provide the following information:
1. A list of all key-value pairs.
2. For each key-value pair, provide the Python code snippet to access it using the `get` method.

The output should be formatted in Markdown with the following structure:
```markdown
# JSON Key-Value Pairs

## Key-Value List
- `key1`: `value1`
- `key2`: `value2`
...

## Python Access Code
- `key1`: `json_data.get('key1')`
- `key2`: `json_data.get('key2')`
...
```
"""

# Function to submit the request to OpenAI API
def submit_request():
    file_path = attached_file_label.cget("text")
    if not file_path:
        messagebox.showwarning("Input Error", "No JSON file attached.")
        return

    json_content = read_json_file(file_path)
    prompt = generate_prompt(json_content)

    def run_api_request():
        try:
            log_message("Initializing OpenAI client...")
            client = openai.OpenAI()
            log_message("Sending request to OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert software engineer specializing in exploring JSON files."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=16384
            )

            log_message("Processing response from OpenAI API...")
            result = response.choices[0].message.content

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, result)
            log_message("Operation completed successfully.")

        except Exception as e:
            log_message(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            progress_bar.stop()
            submit_button.config(state=tk.NORMAL)

    submit_button.config(state=tk.DISABLED)
    progress_bar.start()
    threading.Thread(target=run_api_request).start()

# Function to log messages in the GUI
def log_message(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)
    root.update_idletasks()

# GUI setup
root = tk.Tk()
root.title("JSON Key-Value Discovery Tool")

# JSON file attachment
tk.Label(root, text="Attach JSON File:").grid(row=0, column=0, sticky=tk.W)
attach_button = tk.Button(root, text="Attach File", command=attach_file)
attach_button.grid(row=0, column=1, pady=5)
attached_file_label = tk.Label(root, text="", wraplength=300)
attached_file_label.grid(row=1, column=0, columnspan=2, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_request)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result text
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=3, column=0, columnspan=2, pady=10)

# Log box
tk.Label(root, text="Log:").grid(row=4, column=0, sticky=tk.W)
log_box = scrolledtext.ScrolledText(root, width=80, height=10)
log_box.grid(row=5, column=0, columnspan=2, pady=5)

# Progress bar
progress_bar = Progressbar(root, mode='indeterminate')
progress_bar.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
