import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import json

class WebhookPoster:
    def __init__(self, root):
        self.root = root
        self.root.title("Webhook POST Request Sender")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # URL Input
        self.url_label = tk.Label(root, text="Webhook URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=80)
        self.url_entry.pack(pady=5)

        # Payload Input
        self.payload_label = tk.Label(root, text="Payload (JSON):")
        self.payload_label.pack(pady=5)
        self.payload_text = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
        self.payload_text.pack(pady=5)

        # Submit Button
        self.send_button = tk.Button(root, text="Send POST Request", command=self.send_request)
        self.send_button.pack(pady=10)

        # Response Text Area
        self.response_label = tk.Label(root, text="Response:")
        self.response_label.pack(pady=5)
        self.response_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
        self.response_text.pack(pady=5)

    def send_request(self):
        url = self.url_entry.get().strip()
        payload = self.payload_text.get("1.0", tk.END).strip()

        # Validate URL
        if not url:
            messagebox.showerror("Error", "Webhook URL cannot be empty.")
            return

        # Validate Payload
        try:
            json_payload = json.loads(payload)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON payload.")
            return

        # Send POST Request
        try:
            response = requests.post(url, json=json_payload)
            response.raise_for_status()
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Status Code: {response.status_code}\nResponse: {response.text}")
        except requests.exceptions.RequestException as e:
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebhookPoster(root)
    root.mainloop()
