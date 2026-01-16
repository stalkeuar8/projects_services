import random
import time
import os

is_working = False
dirt_level = 0
water_level = 0
bean_level = 0
coffee_list = {"Americano" : 200, "Cappuccino": 300, "Latte" : 500, "Espresso" : 100}


def start_choice():
    while True:
        choice = int(input("\n1. Turn on the machine\n"
                           "2. Make coffee\n3. Check the resources\n4. Add water\n5. Add coffee beans"
                           "\n6. Clean the machine\n7. Turn off the machine\n8. Stop program\n\nEnter: "))
        if 0 < choice < 8:
            match choice:
                case 1:
                    turn_on()
                    continue
                case 2:
                    choose_coffee()
                    continue
                case 3:
                    check_level()
                    continue
                case 4:
                    add_water()
                    continue
                case 5:
                    add_beans()
                    continue
                case 6:
                    clean_machine()
                    continue
                case 7:
                    turn_off()
                    continue
                case 8:
                    break
                case _:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Invalid choice! Try more!")
                    continue
        break

def turn_on ():
    def vault_check():
        voltage = random.randint(180, 250)
        if 240 > voltage > 200:
            return True
        else:
            return False
    global is_working
    if not is_working:
        if vault_check():
            is_working = True
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Machine is turned on! ")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid voltage value! Unable to turn on! ")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Machine is already turned on!")



def turn_off ():
    global is_working
    is_working = False
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Machine is turned off! ")


def clean_machine():
    if not is_working:
        global dirt_level
        dirt_level = 0
        os.system('cls' if os.name == 'nt' else 'clear')
        print("cleaning process", end="")
        for i in range(10):
            print(".", end="")
            time.sleep(0.35)
        print(f"\nMachine is cleaned! Dirt level: {dirt_level}")
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Machine must be turned off while cleaning! Turn off!")


def check_level():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Water level: ", water_level)
    print("Coffee bean level: ", bean_level)
    print("Dirt level: ", dirt_level, "%")


def add_beans():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        global bean_level
        temp = int(input("Enter amount of beans to add (max 50): "))
        if  0 <= bean_level + temp <= 50:
            if 0 <= temp <= 50:
                bean_level += temp
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Beans added! New bean level: {bean_level}")
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Invalid value of beans to add! Must be between 0 and 50! Current value: {bean_level}")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Invalid value of beans to add! Must be between 0 and 50! Current value: {bean_level}")

def add_water():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        global water_level
        temp = int(input("Enter amount of water to add (max 700): "))
        if 0 <= water_level + temp <= 700:
            if 0 <= temp <= 700:
                water_level += temp
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Water added! New water level: {water_level}")
                break
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid value of water to add! Must be between 0 and 700!")
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid value of water to add! Must be between 0 and 700!")



def choose_coffee():
    if is_working:
        count = 1
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in coffee_list:
            print(f"{count}.", end="")
            count += 1
            print(i)
        while True:
            coffee_choice = input("\nEnter your choice: ").capitalize()
            if coffee_choice in coffee_list:
                index = list(coffee_list).index(f"{coffee_choice}")
                coffee_making(index)
                break
            elif len(coffee_choice) == 1:
                if 0 < int(coffee_choice) < 5:
                    index = int(coffee_choice) - 1
                    coffee_making(index)
                    break
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Invalid choice! Try more! ")
                    continue
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid choice! Try more! ")
                continue
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Turn on the machine to make a coffee!")



def coffee_making(index):
    while True:
        global water_level
        global bean_level
        global dirt_level
        key_name = list(coffee_list)[index]
        if ((water_level - coffee_list[f'{key_name}']) < 0 or ((bean_level - 15) < 0)) or (
                (water_level - coffee_list[f'{key_name}']) < 0 and ((bean_level - 15) < 0)):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Not enough resources to make {list(coffee_list)[index]}!")
            break
        else:
            if dirt_level >= 100:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Machine is too dirty! Clean it before making a coffee! ")
                break
            else:
                print(f"{list(coffee_list)[index]} chosen!")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\nmaking process", end="")
                for i in range(10):
                    print(".", end="")
                    time.sleep(0.35)
                print(f"\n{list(coffee_list)[index]} made! Take cup out of machine! ")
                water_level -= coffee_list[f'{key_name}']
                bean_level -= 25
                dirt_level += 20
                break


