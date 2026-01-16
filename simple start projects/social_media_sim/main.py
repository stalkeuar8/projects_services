import user_class as main
import sys
import time



def run_program():
    with open('all_logs.txt', 'a', encoding='utf-8') as file:
        file.write(f"\n\nProgram started: {main.time_logger()}")
    with open('admin_logs.txt', 'a', encoding='utf-8') as file:
        file.write(f"\n\nProgram started: {main.time_logger()}")
    for profile in main.User.profiles_list:
        with open(f'{profile}_logs.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n\nProgram started: {main.time_logger()}")

    print("\n\nProgram 'Social media simulator' started!")

    while True:
        print("\nMake your choice: ")
        print("\n\n1 - Log in\n2 - Sign up\n3 - Quit")
        try:
            choice = int(input("\nEnter: "))
            match choice:
                case 1:
                    temp_nickname = input("Enter nickname: ")
                    all_user_info_dict = main.json_loader('user_info.json')
                    if main.is_registered(all_user_info_dict, temp_nickname):
                        current_user_info = all_user_info_dict[temp_nickname]
                        for attempt in range(1, 4):
                            temp_passcode = input("Enter passcode: ")
                            if main.pass_checker(current_user_info, temp_passcode):
                                print("\nLogged successfully!")
                                if not current_user_info['is_admin']:
                                    current_user = main.User(temp_nickname, temp_passcode, current_user_info['email'])
                                    while True:
                                        print("1 - Create post\n2 - See all my posts\n"
                                              "3 - Find my post by id\n4 - Delete post by id\n5 - Delete all my posts\n\n"
                                              "6 - Change user\n7 - Stop program")
                                        gl_choice = int(input("Enter your choice: "))
                                        match gl_choice:
                                            case 1:
                                                # create post
                                                if not all_user_info_dict[current_user.nickname]["is_banned"]:
                                                    text = input("Enter what do you want to post: ")
                                                    print(current_user.create_post(text))
                                                    all_user_info_dict[temp_nickname]['user_post_qty'] += 1
                                                    all_user_info_dict[temp_nickname]['posts'][f"Id: {main.User.post_qty}"] = text
                                                    main.update_json('user_info.json', all_user_info_dict)
                                                    continue
                                                else:
                                                    print(f"\nUser '{current_user.nickname}' is banned! Cant make a post.\n")
                                            case 2:
                                                # show posts
                                                all_user_info_dict = main.json_loader('user_info.json')
                                                print(current_user.show_posts(all_user_info_dict[current_user.nickname]['posts']))
                                                continue
                                            case 3:
                                                num_id = input("Enter post id to find: ")
                                                id_to_find = 'Id: ' + num_id
                                                print(current_user.find_post_by_id(id_to_find, all_user_info_dict[current_user.nickname]['posts']))
                                                continue
                                            case 4:
                                                num_id = input("Enter post id to delete: ")
                                                id_to_delete = 'Id: ' + num_id
                                                print("Are you sure you want to delete post?")
                                                while True:
                                                    temp_choice = input("Enter Yes or No: ")
                                                    if temp_choice.lower() == 'yes':
                                                        if id_to_delete in all_user_info_dict[current_user.nickname]['posts'].keys():
                                                            updated_dict = current_user.delete_my_post_by_id(id_to_delete, all_user_info_dict[current_user.nickname]['posts'])
                                                            all_user_info_dict[current_user.nickname]['posts'] = updated_dict
                                                            print(f"Post (by {id_to_delete}) deleted!")
                                                            all_user_info_dict[current_user.nickname]['user_post_qty'] -= 1
                                                            main.update_json('user_info.json', all_user_info_dict)
                                                        else:
                                                            print(f"\nNo such posts in {current_user.nickname}’s library\n\n")
                                                        break
                                                    elif temp_choice.lower() == 'no':
                                                        print("\nDeleting canceled!\n\n")
                                                        break
                                                    else:
                                                        print("\nWrong choice! Please try more\n")
                                                        continue
                                                continue
                                            case 5:
                                                print("Are you sure you want to delete all your posts?")
                                                while True:
                                                    choice = input("Enter Yes or No: ")
                                                    if choice.lower() == 'yes':
                                                        print("\nYour posts are deleted!\n")
                                                        all_user_info_dict[current_user.nickname]['user_post_qty'] = 0
                                                        all_user_info_dict[current_user.nickname]['posts'] = {}
                                                        current_user.delete_all_my_posts()
                                                        main.update_json('user_info.json', all_user_info_dict)
                                                        break
                                                    elif choice.lower() == 'no':
                                                        print("\nDeleting canceled! ")
                                                        break
                                                    else:
                                                        print("\nInvalid choice!\n")
                                                        continue
                                                continue
                                            case 6:
                                                print('\nloging out', end='')
                                                for i in range(10):
                                                    print(".", end='')
                                                    time.sleep(0.2)
                                                print("\n\nLogged out successfully!")
                                                break
                                            case 7:
                                                print("\n\nProgram stopped!\n\n")
                                                sys.exit()
                                else:
                                    current_user = main.Administrator(temp_nickname, current_user_info['email'], temp_passcode)
                                    while True:
                                        print("\n1 - Check all logs\n2 - Check admin logs\n"
                                              "3 - Check user logs\n4 - Clear user logs\n5 - Clear all logs\n6 - Find user posts\n7 - Ban user\n8 - Unban user\n9 - Delete user post by id\n10 - Delete all user posts\n\n11 - Change user\n12 - Quit")
                                        gl_choice = int(input("Enter your choice: "))
                                        match gl_choice:
                                            case 1:
                                                # check all logs
                                                print(current_user.check_all_logs())
                                                continue
                                            case 2:
                                                # check admin logs
                                                print(current_user.check_admin_logs())
                                                continue
                                            case 3:
                                                pass
                                                # check user logs
                                                current_user_logs = main.json_loader('user_logs.json')
                                                user_to_check = input("\nEnter nickname of user: ")
                                                if user_to_check in current_user_logs.keys():
                                                    user_to_check = main.User(user_to_check, all_user_info_dict[user_to_check]['email'], all_user_info_dict[user_to_check]['passcode'])
                                                    print(current_user.check_user_logs(user_to_check, current_user_logs[user_to_check.nickname]))
                                                    continue
                                                else:
                                                    print("\nNo such user registered!\n\n")
                                                    continue
                                            case 4:
                                                # clear user logs
                                                while True:
                                                    choice = input("Are you sure you want to delete all user logs? ")
                                                    if choice.lower() == 'yes':
                                                        current_user.clear_user_logs()
                                                        print("\nAll user logs deleted!\n")
                                                        break
                                                    elif choice.lower() == 'no':
                                                        print("\nDeleting canceled!")
                                                        break
                                                    else:
                                                        print("\nInvalid choice! Try more.")
                                                        continue
                                            case 5:
                                                # clear all logs
                                                print("1 - Clear all this session logs\n2 - Clear all logs data base\n3 - Cancel\n\n")
                                                while True:
                                                    try:
                                                        while True:
                                                            choice = int(input("Enter your choice: "))
                                                            if choice == 1:
                                                                while True:
                                                                    sec_choice = input("\nPress 'Yes' to delete all this session logs. Press 'No' to cancel: \n")
                                                                    if sec_choice.lower() == 'yes':
                                                                        main.all_logs = []
                                                                        print("\nAll this session logs cleared!")
                                                                        break
                                                                    elif sec_choice.lower() == 'no':
                                                                        print("\nDeleting canceled!\n")
                                                                        break
                                                                    else:
                                                                        print("Invalid choice! Try more.\n")
                                                                        continue
                                                            elif choice == 2:
                                                                while True:
                                                                    sec_choice = input("\nPress 'Yes' to delete all logs data base. Press 'No' to cancel: \n")
                                                                    if sec_choice.lower() == 'yes':
                                                                        main.clear_file('all_logs.txt', '')
                                                                        current_user.clear_all_logs()
                                                                        print("\nLog data base has been cleared!")
                                                                        break
                                                                    elif sec_choice.lower() == 'no':
                                                                        print("\nDeleting canceled!\n")
                                                                        break
                                                                    else:
                                                                        print("Invalid choice! Try more.\n")
                                                                        continue
                                                            elif choice == 3:
                                                                print("\nDeleting canceled!\n\n")
                                                                break
                                                            break
                                                        break
                                                    except ValueError:
                                                        print("\nChoice must be a number! Try more. \n")
                                                        break
                                                    except TypeError:
                                                        print("\nInvalid choice! Try more. \n")
                                                        break
                                                continue

                                            case 6:
                                                # find user posts by id
                                                user_to_find = input("Enter user nickname to find: ")
                                                if main.is_registered(all_user_info_dict, user_to_find):
                                                    num_id = input("Enter post id to find: ")
                                                    id_to_find = 'Id: ' + num_id
                                                    print("\n")
                                                    print(current_user.find_user_post_by_id(user_to_find, id_to_find, all_user_info_dict[user_to_find]['posts']))
                                                    print("\n")
                                                else:
                                                    print("\nUser not found! Try more.\n\n")
                                                continue
                                            case 7:
                                                # ban user
                                                # видаляються всі пости
                                                user_to_ban = input("Enter nickname of user to ban: ")
                                                if user_to_ban in all_user_info_dict.keys():
                                                    print(f"Are you sure you want to ban user '{user_to_ban}' ? All posts will be deleted!")
                                                    while True:
                                                        ban_choice = input("Enter Yes or No: ")
                                                        if ban_choice.lower() == 'yes':
                                                            current_user.ban_user(user_to_ban, all_user_info_dict)
                                                            print(f"User {user_to_ban} banned! ")
                                                            break
                                                        elif ban_choice.lower() == 'no':
                                                            print("Banning canceled! ")
                                                            break
                                                        else:
                                                            print("\nInvalid choice!\n")
                                                            continue

                                                else:
                                                    print("\nNo such user registered! Try more. \n")

                                                continue
                                            case 8:
                                                # unban user
                                                user_to_unban = input("Enter nickname of user to unban: ")
                                                if user_to_unban in all_user_info_dict.keys():
                                                    current_user.unban_user(user_to_unban, all_user_info_dict)
                                                    print(f"\nUser {user_to_unban} unbanned!\n")
                                                else:
                                                    print("\nNo such user registered! Try more. \n")
                                                continue
                                            case 9:
                                                # delete user post by id
                                                user_to_delete_post = input("Enter user nickname to delete post: ")
                                                if user_to_delete_post in all_user_info_dict.keys():
                                                    while True:
                                                        try:
                                                            post_num = int(input("Enter post id to delete: "))
                                                            id_to_delete = f"Id: {post_num}"
                                                            if id_to_delete in all_user_info_dict[user_to_delete_post]["posts"].keys():
                                                                del all_user_info_dict[user_to_delete_post]["posts"][id_to_delete]
                                                                print(f"\nPost by {id_to_delete} deleted!\n")
                                                                main.update_json('user_info.json', all_user_info_dict)
                                                            else:
                                                                print("Not such post id or this post is published by other user")
                                                            break
                                                        except ValueError:
                                                            print("ID must be a number!")
                                                            continue
                                                continue

                                            case 10:
                                                # delete all user posts
                                                user_to_delete_all_posts = input("Enter user nickname to delete all posts: ")
                                                if main.is_registered(all_user_info_dict, user_to_delete_all_posts):
                                                    print(f"\nAre you sure you want to delete all '{user_to_delete_all_posts}' posts?\n")
                                                    while True:
                                                        choice = input("Enter Yes or No:")
                                                        if choice.lower() == 'yes':
                                                            current_user.delete_all_user_posts(user_to_delete_all_posts, all_user_info_dict)
                                                            print(f"\nAll {user_to_delete_all_posts} posts deleted! \n")
                                                            break
                                                        elif choice.lower() == 'no':
                                                            print("\nDeleting canceled!\n")
                                                            break
                                                        else:
                                                            print("\nInvalid choice! Try more. \n")
                                                            continue
                                                else:
                                                    print("\nNo such user registered! Try more.\n")
                                                    continue

                                            case 11:
                                                # change user
                                                print('\nloging out', end='')
                                                for i in range(10):
                                                    print(".", end='')
                                                    time.sleep(0.2)
                                                print("\n\nLogged out successfully!")
                                                break
                                            case 12:
                                                print("\n\nProgram stopped!\n\n")
                                                sys.exit()

                            else:
                                if attempt == 3:
                                    print("You have no more attempts! Try later.")
                                    break
                                else: print("Invalid pass! Try more! You have 2 tries!") if not 3 - attempt == 1 else print(
                                    "Invalid pass! Try more! You have 1 try!")
                                continue

                            break
                    else:
                        print("Not such logins registered! Try more or sign up!")
                        continue
                    continue
                case 2:
                    print("\n---Register menu---")
                    temp_nickname = input("Enter new nickname: ")
                    temp_passcode = input("Enter new passcode: ")
                    temp_email = input("Enter new email: ")
                    all_user_info_dict = main.json_loader('user_info.json')
                    all_user_info_dict[temp_nickname] = {"passcode" : temp_passcode, "email" : temp_email, "user_post_qty" : 0, "is_admin" : False, "is_banned" : False, "posts" : {}}
                    main.update_json('user_info.json', all_user_info_dict)
                    user_logs_json = main.json_loader('user_logs.json')
                    user_logs_json[temp_nickname] = []
                    main.update_json('user_logs.json', user_logs_json)
                    print("Registered successfully!\n")
                    continue
                case 3:
                    print("\n\nProgram stopped!\n\n")
                    sys.exit()
                case _:
                    print("Invalid choice! Try more.")
                    continue
        except ValueError:
            print("\nChoice must be a number! Try more.\n")
            continue
        except TypeError:
            print("\nInvalid choice! Try more.\n")
            continue

run_program()