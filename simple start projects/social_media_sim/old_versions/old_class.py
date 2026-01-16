#
#
# попросити gemini зробити відступи та sys('cls')
#
#
#

import datetime
import json
import os


def add_to_file(filename: str, text_content: str):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write("\n" + text_content)

def clear_file(file_name, text_content):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("\n" + text_content)


def time_logger():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S (%d/%m/%Y)")
    return formatted_time


def json_loader(file_name):
    if not os.path.exists(file_name):
        return {}

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        output = {}
        return output


def update_json(file_name, dict_to_update):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(dict_to_update, file, indent=4)
    except Exception as e:
        print(e)



def is_registered(dict_to_check, nick_to_check):
    if nick_to_check.lower() in dict_to_check.keys():
        return True
    else: return False


def pass_checker(dict_to_check, pass_to_check):
    if pass_to_check == dict_to_check['passcode']:
        return True
    else: return False


def new_user_json(old_dict, new_user_nick, new_user_pass):
    new_dict = old_dict
    new_dict[new_user_nick] = new_user_pass
    return new_dict


all_logs = []
admin_logs = []

class User:

    general_info = json_loader('general_info.json')
    post_qty = general_info['post_qty']
    operations_qty = general_info['operations_qty']
    profiles_list = []


    def logger(self, log_message, is_user_admin=True):
        if not is_user_admin:
            self.user_logs.append(log_message)
            all_logs.append(f"\n{log_message}")
            add_to_file(f"{self.nickname}_logs.txt", log_message)
            add_to_file("all_logs.txt", log_message)
            current_user_logs = json_loader('user_logs.json')
            current_user_logs[self.nickname].append(f"\n{log_message}")
            update_json('user_logs.json', current_user_logs)
        else:
            all_logs.append(f"\n{log_message}")
            add_to_file(f"{self.nickname}_logs.txt", log_message)
            add_to_file("all_logs.txt", log_message)
            admin_logs.append(f"\n{log_message}")

    def root_checker(self):
        if self.is_admin:
            pass
        else: raise PermissionError(f"Permission error! User {self.nickname} does not have admin roots!")

    def __init__(self, nickname, email, passcode):
        self.nickname = nickname
        self.email = email
        self.passcode = passcode
        # self.posts = {}
        self.user_logs = []
        self.is_admin = False
        self.is_banned = False
        self.user_post_qty = 0
        User.profiles_list.append(f"{self.nickname.lower()}")



    @staticmethod
    def action():
        User.operations_qty += 1
        User.general_info['operations_qty'] += 1
        update_json('general_info.json', User.general_info)

    def create_post(self, text_to_post):
        User.post_qty += 1
        User.general_info['post_qty'] += 1
        update_json('general_info.json', User.general_info)
        self.user_post_qty += 1
        self.action()
        log = f"User '{self.nickname}' created a post. Post text: '{text_to_post}'. Operation ID: {User.operations_qty} || Time: {time_logger()}"
        self.logger(log, False)
        return f"\nPost created! Post id: {User.post_qty} || Text: {text_to_post}\n"


    def show_posts(self, dict_to_show):
        output = f"\n----{self.nickname} posts----\n\n"
        if len(dict_to_show) > 0:
            for k, v in dict_to_show.items():
                output += f"{k} || Text: {v}\n"
            self.action()
            return output
        else:
            output += "\nNo posts\n"
            return output

    def __str__(self):
        return f"Nickname: {self.nickname} || Email: {self.email} || Is admin? : {self.is_admin}"

    @staticmethod
    def find_post_by_id(find_id, dict_to_find):
        for k, v in dict_to_find.items():
            if find_id == k:
                return f"Post found! Post {k} || Text: {v}"
        return "Post was not found!"


    def delete_my_post_by_id(self, delete_id, dict_to_change):
        del dict_to_change[delete_id]
        log = f"User '{self.nickname}' deleted his post (by {delete_id}). Operation ID: {User.operations_qty} || Time: {time_logger()}"
        self.logger(log, False)
        return dict_to_change

    def delete_all_my_posts(self):
            log = f"User '{self.nickname}' deleted all his posts! Operation ID: {User.operations_qty} || Time: {time_logger()}"
            self.logger(log, False)
            return True


class Administrator(User):


    def __init__(self, name, email, passcode):
        super().__init__(nickname=name, email=email, passcode=passcode)
        self.is_admin = True

    @staticmethod
    def check_all_logs():
        output = "\n\n----All this session logs----\n"
        if len(all_logs) > 0:
            for log in all_logs:
                output += f"{log}\n"
            return output
        else:
            return "Logs are empty."

    @staticmethod
    def check_admin_logs():
        output = "\n\n----This session admin logs----\n"
        for log in admin_logs:
            output += f"{log}\n"
        return output

    @staticmethod
    def check_user_logs(user, list_to_check):
        output = f"\n----{user.nickname} logs----\n"
        for log in list_to_check:
            output += f"{log}\n"
        return output


    def clear_user_logs(self):
        global_dict = json_loader('user_logs.json')
        for user_logs in global_dict.keys():
            global_dict[user_logs] = []
        update_json('user_logs.json', global_dict)
        log = f"Admin cleared all user logs data base. Operation ID: {User.post_qty} || Time: {time_logger()}"
        self.logger(log)

    def clear_all_logs(self):
        log = f"Admin cleared all logs data base. Operation ID: {User.operations_qty} || Time: {time_logger()}"
        self.logger(log)
        return True

    def delete_all_user_posts(self, user_nickname, global_dict):
        global_dict[user_nickname]["posts"] = {}
        update_json('user_info.json', global_dict)
        log = f"Admin deleted all '{user_nickname}' posts. Operation ID: {User.operations_qty} || Time: {time_logger()}"
        self.logger(log)
        return True

    @staticmethod
    def find_user_post_by_id(user_nickname, id_to_find, dict_to_find):
        result = User.find_post_by_id(id_to_find, dict_to_find)
        if not result == "Post was not found!":
            result += f" || Owner: {user_nickname}."
            return result
        else: return "Post was not found! "


    def ban_user(self, user_nickname, global_dict_to_change):
        self.action()
        global_dict_to_change[user_nickname]["is_banned"] = True
        global_dict_to_change[user_nickname]["posts"] = {}
        global_dict_to_change[user_nickname]['user_post_qty'] = 0
        general_info_to_change = json_loader('general_info.json')
        general_info_to_change['post_qty'] -= global_dict_to_change[user_nickname]['user_post_qty']
        update_json('general_info.json', general_info_to_change)
        update_json('user_info.json', global_dict_to_change)
        log = f"Admin banned user '{user_nickname}'. Operation ID: {User.operations_qty}  || Time: {time_logger()}"
        self.logger(log)

    def unban_user(self, user_nickname, global_dict_to_change):
        self.action()
        global_dict_to_change[user_nickname]["is_banned"] = False
        update_json('user_info.json', global_dict_to_change)
        log = f"Admin unbanned user '{user_nickname}'. Operation ID: {User.operations_qty}  || Time: {time_logger()}"
        self.logger(log)

current_user = None
