import os #Get OS-level helpers. Not used here.
import time #Pauses the loop briefly to not hammer the CPU.
import hashlib #This creates a short hash for unique filename so same snippets won't collide & filenames are predictable.
import pyperclip #Library that reads/writes clipboard. Here we use it to get current copied text with paste() 
import ast #Built-in python module to parse code.

from datetime import datetime #Timing filenames for the snippets.
from plyer import notification #Native desktop notification.
from pathlib import Path #Nicer way to work with file paths.

#Creating the folder where the snippits will be stored.
#CHANGE NEEDED HERE!
STORAGE_DIR = Path("D:/ai_code_helper") / "code_snpt" #Builds folder where snpts will be stored & code_snpt folder will be created inside home folder.
#STORAGE_DIR = Path.home() / "ai_code_helper" / "code_snpt" |PLEASE USE THIS IF YOU DON'T HAVE ABOVE STORAGE OPTION & COMMENT THE ABOVE|
STORAGE_DIR.mkdir(parents= True, exist_ok= True) #Creates directort if not exist ("parents= True" = allows creation of parent folders & "exit_ok= True" = don’t crash if folder already exists).

#Function to check if copied text is python code or not.
def is_python_code(text: str) -> bool:
    try:
        ast.parse(text) #Tries to read the string as python code.
        return True #Valid code.
    except SyntaxError: 
        return False #Not vaild code.
    
#Function to save clipboard text
def save_snpt(text):
    if not text.strip(): #If clipboard has nothing, spaces or newlines.
        return None #ignore empty/whitespace clipboard text.
    
    #Creating unique filename based on hash
    hash_id = hashlib.sha1(text.encode()).hexdigest()[:8] #Creates a short 8-character hash so filenames are unique for each snippet.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #Creates a human readable timestamp.
    filename = STORAGE_DIR / f"snippet_{timestamp}_{hash_id}.txt" #Final filename created.

    #Open file for writing & save clipboard data.
    with open(filename, "w", encoding="utf-8") as f: #encoding="utf-8" ensures non-ASCII cahracters are stored safely.
        f.write(text)

    return filename #Return full path so caller can notify

#Function to notify user
def notify_user(filepath):
    notification.notify( #Calls plyer.notification.notify(...) to display popup.
        title= "Code snippet saved", #Notification title
        message= f"Saved at: {filepath.name}", #Notification message
        timeout= 3 #Tells OS to close popup after 3 seconds
    )

#Main loop function. "poll_interval= 1.0 *seconds" time to wait between clipboard checks
def main(poll_interval= 1.0):
    last_text = "" #Store previous clipboard text. Prevents from saving the same snippet.
    print("Python clipboard monitoring started... (Press CTRL+C to stop)") 

    while True: #Start infinite loop until CTRL+C.
        try: #Wrapping the loop so CTRL+C is cleanly handled.
            text = pyperclip.paste() #Read current clipboard content as a string.

            #If saved success, notify & print saved path in terminal.
            if text != last_text and text.strip(): 
                if is_python_code(text): #Before saving we check if copied text is python code.
                    filepath = save_snpt(text) #Save it to the chosen folder.
                    if filepath:
                        notify_user(filepath) #Notify the user about the save.
                        print(f"Python code detected and saved at: {filepath}") #Print success message.
                else:
                    print("No python code detected") #Print ignored message.
            
            last_text = text #Same snippet not being processed again & again.

            time.sleep(poll_interval) #Pause for "poll_interval" seconds(1 second) before checking again.

        #If user press CTRL+C, print message and exit loop.
        except KeyboardInterrupt:
            print("\nStopped by user.")
            break

#Runs "main". If this file is exicuted, "main" will not run if the file is imported as module.
if __name__ == "__main__":
    main()