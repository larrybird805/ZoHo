import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import openai
import logging
import markdown2
from xhtml2pdf import pisa
import threading
from tkinter.ttk import Progressbar
from io import BytesIO

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def log_message(message):
    logger.info(message)
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)
    root.update_idletasks()

def attach_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        attached_file_label.config(text=file_path)

def generate_prompt(language, code_snippet, purpose, creator, dependencies, issues, documentation, attachment=None):
    attachment_info = f"\n- **Attachment:** {attachment}" if attachment else ""
    return f"""
### Orphaned Code Analysis and Rewrite Request

**Code Snippet:**
```{language}
{code_snippet}
```

**Language:** {language}

**Context:**
- **Purpose of the Code:** {purpose}
- **Original Creator (if known):** {creator}
- **External Dependencies (websites, frameworks, libraries):** {dependencies}
- **Known Issues or Bugs:** {issues}
- **Related Documentation (if any):** {documentation}{attachment_info}

**Required Analysis:**
1. **Functionality:**
   - What does the code do?
   - How does the code achieve its functionality?
   - **Input/Output:** Describe the input parameters and output results.

2. **Code Comments:**
   - Provide a commented version of the code to enhance readability and maintainability.

3. **Edge Situations:**
   - Address cases where the code is uncommented.
   - Handle lesser-known or proprietary languages.
   - Describe relationships with external websites, frameworks, and libraries.

**Rewrite Standards:**
- **User-Centric Design:** Ensure the code focuses on the needs and experiences of end-users.
- **Scalability:** Plan for future growth in users, data, and functionality.
- **Maintainability:** Write clean, readable, and modular code.
- **Security:** Protect user data and ensure application security.
- **DRY (Don't Repeat Yourself):** Avoid duplicating code by creating reusable components.
- **KISS (Keep It Simple, Stupid):** Keep the code and design as simple as possible.
- **Separation of Concerns:** Divide the application into distinct sections with specific responsibilities.
- **Modularity:** Break down the application into smaller, independent modules.
- **Single Responsibility Principle:** Ensure each module or class has one responsibility.
- **User Experience:** Design with the end-user in mind for ease of use and navigation.

**Deliverable:**
- **Markdown-Formatted Document:** Provide the analysis and the rewrite in a markdown-formatted document with the following sections:
```markdown
# Code Analysis Report

## Original Code
```{{language}}
{{code_snippet}}
```

## Functionality
- **Description:** What does the code do?
- **How it Works:** Detailed explanation of the code's functionality.
- **Input/Output:**
- **Input:** Describe input parameters.
- **Output:** Describe output results.

## Commented Code
```{{language}}
{{commented_code}}
```

## Edge Situations
- **Uncommented Code:** Handling and clarifications.
- **Proprietary Language:** Explanation and usage.
- **External Relationships:** Dependencies and integrations.

## Code Rewrite

### Description
A quick explanation of the benefits and reasons of the code rewrite.

### Rewritten Code
```{{language}}
{{rewritten_code}}
```
```
"""

def submit_request():
    language = language_entry.get()
    code_snippet = code_text.get("1.0", tk.END).strip()
    purpose = purpose_entry.get()
    creator = creator_entry.get()
    dependencies = dependencies_entry.get()
    issues = issues_entry.get()
    documentation = documentation_entry.get()
    attachment = attached_file_label.cget("text")

    if not code_snippet:
        messagebox.showwarning("Input Error", "Code snippet cannot be empty.")
        return
    
    log_message("Generating prompt...")
    prompt = generate_prompt(language, code_snippet, purpose, creator, dependencies, issues, documentation, attachment)
    log_message("Prompt generated successfully.")

    def run_api_request():
        try:
            log_message("Initializing OpenAI client...")
            client = openai.OpenAI()

            log_message("Sending request to OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert software engineer specializing in orphaned code rehabilitation."},
                    {"role": "user", "content": prompt}
                ]
            )

            log_message("Processing response from OpenAI API...")
            result = response.choices[0].message.content

            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, sanitize_markdown(result))
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

def sanitize_markdown(content):
    """
    Remove any occurrences of ```markdown from the content to ensure proper formatting.
    """
    return content.replace("```markdown", "").strip()

def export_to_html():
    try:
        markdown_content = result_text.get("1.0", tk.END).strip()
        if not markdown_content:
            messagebox.showwarning("Export Error", "No content to export.")
            return
        
        # Sanitize markdown content
        sanitized_content = sanitize_markdown(markdown_content)

        # Convert markdown to HTML with code highlighting
        html_content = markdown2.markdown(sanitized_content, extras=["fenced-code-blocks", "code-friendly"])

        # Wrap in basic HTML structure
        html_full = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Code Analysis Report</title>
            <style>
                pre {{ background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
                code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                .codehilite {{ background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Save HTML to file
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(html_full)
            log_message(f"Exported to HTML: {file_path}")
    except Exception as e:
        log_message(f"An error occurred while exporting to HTML: {e}")
        messagebox.showerror("Export Error", f"An error occurred while exporting to HTML: {e}")

# Updated export_to_pdf function
def export_to_pdf():
    try:
        markdown_content = result_text.get("1.0", tk.END).strip()
        if not markdown_content:
            messagebox.showwarning("Export Error", "No content to export.")
            return
        
        # Sanitize markdown content
        sanitized_content = sanitize_markdown(markdown_content)

        # Convert markdown to HTML with code highlighting
        html_content = markdown2.markdown(sanitized_content, extras=["fenced-code-blocks", "code-friendly"])

        # Wrap in basic HTML structure
        html_full = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Code Analysis Report</title>
            <style>
                pre {{ background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
                code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                .codehilite {{ background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Save PDF to file
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'wb') as pdf_file:
                pisa_status = pisa.CreatePDF(BytesIO(html_full.encode('utf-8')), dest=pdf_file)
            if pisa_status.err:
                log_message(f"An error occurred while exporting to PDF: {pisa_status.err}")
                messagebox.showerror("Export Error", f"An error occurred while exporting to PDF.")
            else:
                log_message(f"Exported to PDF: {file_path}")
    except Exception as e:
        log_message(f"An error occurred while exporting to PDF: {e}")
        messagebox.showerror("Export Error", f"An error occurred while exporting to PDF: {e}")

# GUI setup
root = tk.Tk()
root.title("Orphaned Code Analysis")

# Prefill toggle function
def toggle_prefill():
    if prefill_var.get():
        language_entry.insert(0, "Zoho Deluge")
        code_text.insert(tk.END, """Insert Zoho Deluge Code here.""")
        purpose_entry.insert(0, "Take a json payload from a third party (Destiny One) through Zoho Flow")
        creator_entry.insert(0, "Incompetent Third Party Contractor")
        dependencies_entry.insert(0, "Unknown")
        issues_entry.insert(0, "No try-catch, no info statements for  logging, no comments in the code, no modularity. Errors should be logged in Flow.")
        documentation_entry.insert(0, "Attached: Zoho Deluge Documentation.")
    else:
        language_entry.delete(0, tk.END)
        code_text.delete("1.0", tk.END)
        purpose_entry.delete(0, tk.END)
        creator_entry.delete(0, tk.END)
        dependencies_entry.delete(0, tk.END)
        issues_entry.delete(0, tk.END)
        documentation_entry.delete(0, tk.END)

# Language input
tk.Label(root, text="Language:").grid(row=0, column=0, sticky=tk.W)
language_entry = tk.Entry(root, width=50)
language_entry.grid(row=0, column=1)

# Code snippet input
tk.Label(root, text="Code Snippet:").grid(row=1, column=0, sticky=tk.W)
code_text = scrolledtext.ScrolledText(root, width=50, height=10)
code_text.grid(row=1, column=1, pady=5)

# Purpose input
tk.Label(root, text="Purpose of the Code:").grid(row=2, column=0, sticky=tk.W)
purpose_entry = tk.Entry(root, width=50)
purpose_entry.grid(row=2, column=1)

# Original Creator input
tk.Label(root, text="Original Creator (if known):").grid(row=3, column=0, sticky=tk.W)
creator_entry = tk.Entry(root, width=50)
creator_entry.grid(row=3, column=1)

# Dependencies input
tk.Label(root, text="External Dependencies:").grid(row=4, column=0, sticky=tk.W)
dependencies_entry = tk.Entry(root, width=50)
dependencies_entry.grid(row=4, column=1)

# Known Issues input
tk.Label(root, text="Known Issues or Bugs:").grid(row=5, column=0, sticky=tk.W)
issues_entry = tk.Entry(root, width=50)
issues_entry.grid(row=5, column=1)

# Documentation input and attach button
tk.Label(root, text="Related Documentation:").grid(row=6, column=0, sticky=tk.W)
documentation_frame = tk.Frame(root)
documentation_frame.grid(row=6, column=1, sticky=tk.W)
documentation_entry = tk.Entry(documentation_frame, width=40)
documentation_entry.pack(side=tk.LEFT)
attach_button = tk.Button(documentation_frame, text="Attach File", command=attach_file)
attach_button.pack(side=tk.LEFT, padx=5)

# Attached file label
attached_file_label = tk.Label(root, text="", wraplength=300)
attached_file_label.grid(row=7, column=1, pady=5)

# Prefill toggle checkbox
prefill_var = tk.BooleanVar()
prefill_checkbox = tk.Checkbutton(root, text="Zoho Deluge Prefill", variable=prefill_var, command=toggle_prefill)
prefill_checkbox.grid(row=8, column=1, sticky=tk.W)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit_request)
submit_button.grid(row=9, column=0, columnspan=2, pady=10)

# Result text
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=10, column=0, columnspan=2, pady=10)

# Export buttons
export_html_button = tk.Button(root, text="Export to HTML", command=export_to_html)
export_html_button.grid(row=11, column=0, pady=5)

export_pdf_button = tk.Button(root, text="Export to PDF", command=export_to_pdf)
export_pdf_button.grid(row=11, column=1, pady=5)

# Log box
tk.Label(root, text="Log:").grid(row=12, column=0, sticky=tk.W)
log_box = scrolledtext.ScrolledText(root, width=80, height=10)
log_box.grid(row=13, column=0, columnspan=2, pady=5)

# Progress bar
progress_bar = Progressbar(root, mode='indeterminate')
progress_bar.grid(row=14, column=0, columnspan=2, pady=5)

root.mainloop()
