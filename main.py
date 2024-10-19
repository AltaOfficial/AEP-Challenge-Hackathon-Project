import ollama
import flask
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from colorama import Fore, Style

if __name__ == "__main__":
    conversation = []
    startingInfo = """
            1. Suspended load 
            2. mobile equipment/traffic with workers on foot 
            3. Heavy Rotating Equipment
            4. steam
            5. explosion
            6. electrical contact with source
            7. high dose of toxic chemical radiation
            8. fall from elevation
            9. motor vehicle incident (occupant)
            10. high temperature
            11. fire with sustained fuel source
            12. excavation or trench
            13. arc flash
            
            every single message after me if it is one of those hazards
            """
    conversation.append({"role": "user", "content": startingInfo})
    # csv_input = input("")
    # root = tk.Tk()
    # root.withdraw()
    # print("choose a csv file")
    # hazardous_examples_file_path = filedialog.askopenfilename()
    # df = pd.read_csv(hazardous_examples_file_path)
    # print(Fore.RED, df.iloc[:, 4])
    # print(Style.RESET_ALL)
    response = ollama.chat(model="llama3.1", messages=
        conversation
    )
    conversation.append({"role": "assistant", "content": response["message"]["content"]})

    print(Fore.GREEN + "ASSISTANT: \n" + response["message"]["content"] + "\n")
    print(Style.RESET_ALL)

    while(True):
        print("USER: ")
        user_input = input("")
        conversation.append({"role": "user", "content": user_input})
        response = ollama.chat(model="llama3.1", messages=conversation)
        conversation.append({"role": "assistant", "content": response["message"]["content"]})
        print(Fore.GREEN + "ASSISTANT: \n" + response["message"]["content"] + "\n")
        print(Style.RESET_ALL)

