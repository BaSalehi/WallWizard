import os
import keyboard

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options, selected_index):
    clear_screen()
    for index, option in enumerate(options):
        if index == selected_index:
            print(f"> {option}  ")
        else:
            print(f"  {option}  ")

def main_menu():
    options = ["Login", "Sign Up", "Exit"]
    selected_index = 0

    while True:
        display_menu(options, selected_index)

        if keyboard.is_pressed('up'):
            selected_index = (selected_index - 1) % len(options)
            while keyboard.is_pressed('up'):
                pass
        elif keyboard.is_pressed('down'):
            selected_index = (selected_index + 1) % len(options)
            while keyboard.is_pressed('down'):
                pass
        elif keyboard.is_pressed('enter'):
            break

    return options[selected_index]

