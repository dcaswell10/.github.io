import os
import json
from tkinter import Tk, filedialog, messagebox
from email import policy
from email.parser import BytesParser

def parse_eml(file_path):
    """Parse the .eml file and extract specific fields."""
    with open(file_path, 'rb') as f:
        email_message = BytesParser(policy=policy.default).parse(f)
    
    # Extract the required fields
    fields = {
        "Received": email_message.get('Received'),
        "Authentication-Results": email_message.get('Authentication-Results'),
        "X-Sender-IP": email_message.get('X-Sender-IP'),
        "Return-Path": email_message.get('Return-Path'),
        "X-SID-Result": email_message.get('X-SID-Result'),
        "To": email_message.get('To'),
        "Subject": email_message.get('Subject'),
        "Date": email_message.get('Date'),
        "Message-ID": email_message.get('Message-ID'),
        "X-IncomingTopHeaderMarker": email_message.get('X-IncomingTopHeaderMarker')
    }
    return fields

def save_to_json(data, output_file):
    """Save the extracted fields to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {output_file}")

def main():
    # Create a graphical interface for file selection
    root = Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Select File", "Please select a .eml file to parse.")
    
    file_path = filedialog.askopenfilename(
        title="Select .eml File",
        filetypes=[("Email Files", "*.eml"), ("All Files", "*.*")]
    )
    
    if not file_path:
        messagebox.showerror("No File Selected", "No file was selected. Exiting.")
        return
    
    if not os.path.isfile(file_path):
        messagebox.showerror("Invalid File", "The selected file is not valid. Exiting.")
        return
    
    # Parse the .eml file
    try:
        fields = parse_eml(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse the file: {e}")
        return
    
    # Display the extracted fields in the console
    print("Extracted Fields:")
    for key, value in fields.items():
        print(f"{key}: {value}")
    
    # Save the extracted fields to a JSON file
    output_file = os.path.splitext(file_path)[0] + "_parsed.json"
    save_to_json(fields, output_file)
    
    # Notify the user
    messagebox.showinfo("Success", f"Fields extracted and saved to {output_file}")

if __name__ == "__main__":
    main()