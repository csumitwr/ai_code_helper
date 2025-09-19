#Python Clipboard Code Snippet Saver
This script monitors your clipboard for Python code.  
Whenever you copy valid Python code, it automatically saves it as a snippet file and shows you a desktop notification.  

## Features
- Detects valid Python code from clipboard
- Automatically saves snippets into a folder
- Filenames include timestamp + hash to avoid duplicates
- Sends a **desktop notification** when a snippet is saved
- Works on **Windows, macOS, and Linux**

## Requirements
- Python 3.8+
- Dependencies:
  pip install pyperclip plyer
