import sys
import os
# Програма показує меню:
# Редагувати контакт
# Вийти
# Користувач обирає дію.
# Програма виконує дію та повертається в меню.


cont_dict = {

    'Police' : 102,

    'Emergency' : 103,

    'DSNS' : 101

    }



def start():

    while True:
        print("Please choose an option below:")
        print("1 — Add contact\n2 — Show all contacts\n3 — Find contact\n4 — Change contact\n5 — Delete contact\n6 — Clear all contacts\n7 - Exit\n")
        choice = int(input('Enter: '))
        match choice:
            case 1:
                os.system("cls" if os.name == "nt" else "clear")
                add_contact()
                continue
            case 2:
                os.system("cls" if os.name == "nt" else "clear")
                show_contacts()
                continue
            case 3:
                os.system("cls" if os.name == "nt" else "clear")
                find_contact()
                continue
            case 4:
                os.system("cls" if os.name == "nt" else "clear")
                change_contact()
                continue
            case 5:
                os.system("cls" if os.name == "nt" else "clear")
                delete_contact()
                continue
            case 6:
                os.system("cls" if os.name == "nt" else "clear")
                clear_book()
                continue
            case 7:
                os.system("cls" if os.name == "nt" else "clear")
                exit_()
            case _:
                os.system("cls" if os.name == "nt" else "clear")
                print("Invalid choice! Try more!")
                continue

def exit_():
    print("Are you sure you want to close the book? ")
    while True:
        choice = input("\nEnter yes or no: ").lower()
        match choice:
            case 'yes':
                print(" ")
                print("Phone book closed! ")
                sys.exit(0)
            case 'no':
                os.system("cls" if os.name == "nt" else "clear")
                print("Closing canceled!")
                break
            case _:
                print("\nInvalid answer entered! Try more!")


def add_contact ():
    key_name = (input("Enter new contact name: ").lower()).capitalize()
    value_number = int(input("Enter new contact number: "))
    # global cont_dict
    cont_dict[key_name] = value_number
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Contact added! New contact name: {key_name} || Number: {value_number}")
    print("\n\n")

def show_contacts():
    if cont_dict == {}:
        os.system("cls" if os.name == "nt" else "clear")
        print("The book is empty!\n\n")
    else:
        count = 1
        os.system("cls" if os.name == "nt" else "clear")
        for k, v in cont_dict.items():
            print(f"{count}. {k}: {v} ")
            count += 1
        print("\n\n")


def find_contact():
    entered = input("Enter name or number to find contact: ")
    os.system("cls" if os.name == "nt" else "clear")
    finder(entered)
    print("\n\n")


def finder(entered):
    is_found = False
    try:
        number = int(entered)
        for k, v in cont_dict.items():
            if number == v:
                print(f"Contact found! Name: {k}  || Number: {v}\n")
                return k
        if not is_found:
            os.system("cls" if os.name == "nt" else "clear")
            print("Contact does not exist! ")
            return False
    except:
        for k, v in cont_dict.items():
            if entered.lower() == k.lower():
                print(f"Contact found! Name: {k}  || Number: {v}\n")
                return k
        if not is_found:
            os.system("cls" if os.name == "nt" else "clear")
            print("Contact does not exist! ")
            return False

def delete_contact ():
    show_contacts()
    entered = input("Enter name or number to delete contact: ")
    cont_to_delete = finder(entered)
    if cont_to_delete != False:
        print(f"\nAre you sure you want to delete {cont_to_delete}?")
        while True:
            choice = input("Enter yes or no: ").lower()
            match choice:
                case 'yes':
                        # global cont_dict
                        for i in range(len(cont_dict)):
                            if cont_to_delete in cont_dict.keys():
                                cont_dict.pop(f'{cont_to_delete}')
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"Contact {cont_to_delete} deleted!\n\n")
                            else: continue
                        break
                case 'no':
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Deleting canceled!\n\n")
                        break
                case _:
                        print("Invalid answer entered! Try more!\n")
                        continue
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Contact can not be deleted, because it does not exist!\n\n")

def clear_book():
    print("Are you sure you want to clear all contacts?\n")
    while True:
        choice = input("Enter yes or no: ").lower()
        match choice:
            case 'yes':
                cont_dict.clear()
                os.system("cls" if os.name == "nt" else "clear")
                print("Phone book cleared!\n\n")
                break
            case 'no':
                os.system("cls" if os.name == "nt" else "clear")
                print("Deleting canceled!\n\n")
                break
            case _:
                print("Invalid answer entered! Try more!\n")


def change_contact():
    entered = input("Enter name or number of contact you want to change: ")
    cont_to_change = finder(entered)
    if cont_to_change != False:
        # global cont_dict
        print("\n1. Change name")
        print("2. Change number")
        while True:
            try:
                while True:
                    choice = int(input("Enter you choice (1 or 2): "))
                    match choice:
                        case 1:
                            new_name = input("Enter new name: ")
                            for k in cont_dict.keys():
                                if cont_to_change == k:
                                    temp_num = cont_dict[k]
                                    cont_dict.pop(k)
                                    cont_dict[new_name] = temp_num
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Name changed! New name: {new_name}\n\n")
                                    break
                            break
                        case 2:
                            new_number = int(input("Enter new number : "))
                            for k, v in cont_dict.items():
                                if cont_dict[cont_to_change] == v:
                                    cont_dict[k] = new_number
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Number changed! New {k}’s number is: {new_number}\n\n")
                                    break
                            break
                        case _:
                            print("Invalid answer entered! Try more!")
                    break

            except:
                print("Invalid answer entered! Try more!")
                continue
            break

    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Contact can not be changed, because it does not exist!\n\n")




print("Welcome to your phone book!")
start()


















def exit_():
    print("Are you sure you want to close the book? ")
    while True:
        choice = input("\nEnter yes or no: ").lower()
        match choice:
            case 'yes':
                print(" ")
                print("Phone book closed! ")
                sys.exit(0)
            case 'no':
                os.system("cls" if os.name == "nt" else "clear")
                print("Closing canceled!")
                break
            case _:
                print("\nInvalid answer entered! Try more!")


def add_contact ():
    key_name = (input("Enter new contact name: ").lower()).capitalize()
    value_number = int(input("Enter new contact number: "))
    # global cont_dict
    cont_dict[key_name] = value_number
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Contact added! New contact name: {key_name} || Number: {value_number}")
    print("\n\n")

def show_contacts():
    if cont_dict == {}:
        os.system("cls" if os.name == "nt" else "clear")
        print("The book is empty!\n\n")
    else:
        count = 1
        os.system("cls" if os.name == "nt" else "clear")
        for k, v in cont_dict.items():
            print(f"{count}. {k}: {v} ")
            count += 1
        print("\n\n")


def find_contact():
    entered = input("Enter name or number to find contact: ")
    os.system("cls" if os.name == "nt" else "clear")
    finder(entered)
    print("\n\n")


def finder(entered):
    is_found = False
    try:
        number = int(entered)
        for k, v in cont_dict.items():
            if number == v:
                print(f"Contact found! Name: {k}  || Number: {v}\n")
                return k
        if not is_found:
            os.system("cls" if os.name == "nt" else "clear")
            print("Contact does not exist! ")
            return False
    except:
        for k, v in cont_dict.items():
            if entered.lower() == k.lower():
                print(f"Contact found! Name: {k}  || Number: {v}\n")
                return k
        if not is_found:
            os.system("cls" if os.name == "nt" else "clear")
            print("Contact does not exist! ")
            return False

def delete_contact ():
    show_contacts()
    entered = input("Enter name or number to delete contact: ")
    cont_to_delete = finder(entered)
    if cont_to_delete != False:
        print(f"\nAre you sure you want to delete {cont_to_delete}?")
        while True:
            choice = input("Enter yes or no: ").lower()
            match choice:
                case 'yes':
                        # global cont_dict
                        for i in range(len(cont_dict)):
                            if cont_to_delete in cont_dict.keys():
                                cont_dict.pop(f'{cont_to_delete}')
                                os.system("cls" if os.name == "nt" else "clear")
                                print(f"Contact {cont_to_delete} deleted!\n\n")
                            else: continue
                        break
                case 'no':
                        os.system("cls" if os.name == "nt" else "clear")
                        print("Deleting canceled!\n\n")
                        break
                case _:
                        print("Invalid answer entered! Try more!\n")
                        continue
    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Contact can not be deleted, because it does not exist!\n\n")

def clear_book():
    print("Are you sure you want to clear all contacts?\n")
    while True:
        choice = input("Enter yes or no: ").lower()
        match choice:
            case 'yes':
                cont_dict.clear()
                os.system("cls" if os.name == "nt" else "clear")
                print("Phone book cleared!\n\n")
                break
            case 'no':
                os.system("cls" if os.name == "nt" else "clear")
                print("Deleting canceled!\n\n")
                break
            case _:
                print("Invalid answer entered! Try more!\n")


def change_contact():
    entered = input("Enter name or number of contact you want to change: ")
    cont_to_change = finder(entered)
    if cont_to_change != False:
        # global cont_dict
        print("\n1. Change name")
        print("2. Change number")
        while True:
            try:
                while True:
                    choice = int(input("Enter you choice (1 or 2): "))
                    match choice:
                        case 1:
                            new_name = input("Enter new name: ")
                            for k in cont_dict.keys():
                                if cont_to_change == k:
                                    temp_num = cont_dict[k]
                                    cont_dict.pop(k)
                                    cont_dict[new_name] = temp_num
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Name changed! New name: {new_name}\n\n")
                                    break
                            break
                        case 2:
                            new_number = int(input("Enter new number : "))
                            for k, v in cont_dict.items():
                                if cont_dict[cont_to_change] == v:
                                    cont_dict[k] = new_number
                                    os.system("cls" if os.name == "nt" else "clear")
                                    print(f"Number changed! New {k}’s number is: {new_number}\n\n")
                                    break
                            break
                        case _:
                            print("Invalid answer entered! Try more!")
                    break

            except:
                print("Invalid answer entered! Try more!")
                continue
            break

    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("Contact can not be changed, because it does not exist!\n\n")
