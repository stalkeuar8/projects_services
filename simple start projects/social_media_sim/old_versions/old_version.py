# # переробити список posts на словник
# #   прибрати input і print з методів
# #   прибрати використання класу адміністратора в юзері
# #  прибрати finder і зробити два окремих методи на пошук і видалення
# # прибрати "хотів, але передумав"
#
# import datetime
#
# def add_to_file(filename: str, text_content: str):
#     with open(filename, 'a', encoding='utf-8') as file:
#         file.write("\n" + text_content)
#
#
# def time_logger():
#     now = datetime.datetime.now()
#     formatted_time = now.strftime("%H:%M:%S (%d/%m/%Y)")
#     return formatted_time
#
# class User:
#
#     post_qty = 0
#     operations_qty = 0
#     all_user_logs = []
#     created_profiles = 0
#     profiles_list = []
#
#
#     def logger(self, log_message):
#         if self.is_admin:
#             add_to_file('admin_logs.txt', log_message)
#             self.user_logs.append(log_message)
#             Administrator.all_user_logs.append(log_message)
#             add_to_file(f"{self.nickname}_logs.txt", log_message)
#             add_to_file("all_logs.txt", log_message)
#         else:
#             self.user_logs.append(log_message)
#             Administrator.all_user_logs.append(log_message)
#             add_to_file(f"{self.nickname}_logs.txt", log_message)
#             add_to_file("all_logs.txt", log_message)
#
#     def root_checker(self):
#         if self.is_admin:
#             pass
#         else: raise PermissionError(f"Permission error! User {self.nickname} does not have admin roots!")
#
#     def __init__(self, nickname, email):
#         self.nickname = nickname
#         self.email = email
#         self.posts = {}
#         self.user_logs = []
#         self.is_admin = False
#         self.is_banned = False
#         self.user_post_qty = 0
#         User.created_profiles += 1
#         User.profiles_list.append(f"{self.nickname.lower()}")
#         # log = f"User '{self.nickname}' created! Email: {self.email} || Time: {time_logger()}"
#         # self.logger(log)
#
#     def action(self):
#         User.operations_qty += 1
#
#     def create_post(self, text_to_post):
#         if not self.is_banned:
#             User.post_qty += 1
#             self.user_post_qty += 1
#             self.posts[f'Id: {User.post_qty}'] = text_to_post
#             self.action()
#             log = f"User '{self.nickname}' created a post. Post text: '{text_to_post}'. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#             self.logger(log)
#             return f"\nPost created! Post id: {User.post_qty} || Text: {text_to_post}\n"
#         else:
#             log = f"Banned user '{self.nickname}' had an attempt to make a post! Unsuccessful! Time: {time_logger()}"
#             self.logger(log)
#             return f"\nUser '{self.nickname}' is banned! Cant make a post.\n"
#
#     def show_posts(self):
#         self.action()
#         output = f"\n----{self.nickname} posts----\n\n"
#         if len(self.posts) > 0:
#             # return self.posts
#             for k, v in self.posts.items():
#                 output += f"{k} || Text: {v}\n"
#             # for post in self.posts:
#             #     for post_id, text in post.items():
#             #         print(f"{post_id} || Text: {text}")
#             # log = f"User '{self.nickname}' watched his posts. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#             # self.logger(log)
#             return output
#         else:
#             return "No posts"
#
#     def __str__(self):
#         return f"Nickname: {self.nickname} || Email: {self.email} || Is admin? : {self.is_admin}"
#
#
#     def finder(self, id__, action, action_for_log):
#         try:
#             if action.lower() == 'find' and action_for_log.lower() == 'found' or action_for_log.lower() == 'deleted' and action.lower() == 'delete':
#                 id_to_find = 'Id: ' + id__
#                 for post in self.posts:
#                     if id_to_find in post.keys():
#                         self.action()
#                         print(f"Post {action_for_log}! Post id: {id__} || Text: {post[id_to_find]}")
#                         log = f"User '{self.nickname}' {action_for_log} his post (Post id: {id__}) Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                         self.logger(log)
#                         if action == 'delete':
#                             return id_to_find
#                         else:
#                             return True
#                 print("Post was not found! ")
#                 log = f"User '{self.nickname}' wanted to {action} his post (by id: {id__}) Post was not found! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#             else:
#                 raise ValueError("Invalid action!")
#         except Exception as e:
#             print(e)
#
#     def find_post_by_id(self):
#         ACTION = 'find'
#         ACTION_FOR_LOG = 'found'
#         post_id = input("Enter post id to find: ")
#         self.finder(post_id, ACTION, ACTION_FOR_LOG)
#
#     def delete_my_post_by_id(self):
#         ACTION = 'delete'
#         ACTION_FOR_LOG = 'deleted'
#         post_id = input("Enter post id to delete: ")
#         post_key_to_delete = self.finder(post_id, ACTION, ACTION_FOR_LOG)
#         key_for_loop = post_key_to_delete
#         for post in self.posts:
#             if key_for_loop in post.keys():
#                 self.posts.remove(post)
#                 break
#
#
#     # def delete_all_my_posts(self):
#     #     print("Are you sure you want to delete all your posts?")
#     #     while True:
#     #         choice = input("Enter Yes or No: ")
#     #         match choice.lower():
#     #             case 'yes':
#     #                 print("\nYour posts are deleted!\n")
#     #                 self.posts.clear()
#     #                 log = f"User '{self.nickname}' deleted all his posts! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#     #                 self.logger(log)
#     #                 break
#     #             case 'no':
#     #                 print("\nDeleting canceled! ")
#     #                 log = f"User '{self.nickname}' wanted to delete all his posts, but operation CANCELED! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#     #                 self.logger(log)
#     #                 break
#     #             case _:
#     #                 print("\nInvalid choice!\n")
#     #                 continue
#
#     def delete_all_my_posts(self):
#             self.posts.clear()
#             log = f"User '{self.nickname}' deleted all his posts! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#             self.logger(log)
#
#
# class Administrator(User):
#     admin_logs = []
#
#     def __init__(self, name, email):
#         super().__init__(nickname=name, email=email)
#         self.is_admin = True
#
#
#     def check_all_logs(self):
#         print("----All logs----")
#         for log in self.all_user_logs:
#             print(log)
#         self.action()
#         log = f"Admin '{self.nickname}' watched all logs. Operation ID: {User.operations_qty}  || Time: {time_logger()} "
#         self.logger(log)
#
#     def check_admin_user_logs(self):
#         print(f"----Admin logs----")
#         for log in Administrator.admin_logs:
#             print(log)
#         self.action()
#         log = f"Admin {self.nickname} watched admins logs. Operation ID: {User.operations_qty}  || Time: {time_logger()} "
#         self.logger(log)
#
#
#     def check_user_logs(self, user):
#         print(f"----{user.nickname} logs----")
#         for log in user.user_logs:
#             print(log)
#         self.action()
#         log = f"Admin '{self.nickname}' watched '{user.nickname}' logs. Operation ID: {User.operations_qty}  || Time: {time_logger()} "
#         self.logger(log)
#
#
#     def clear_user_logs(self, user):
#         print(f"Are you sure you want to delete '{user.nickname}' logs?")
#         while True:
#             choice = input('Print Yes or No: ')
#             if choice.lower() == "yes":
#                 self.action()
#                 with open(f"{user.nickname}_logs.txt", 'w', encoding='utf-8') as file:
#                     file.write("")
#                     log = f"Admin '{self.nickname}' cleared logs of user: '{user.nickname}'. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                     self.logger(log)
#                     break
#             elif choice.lower() == 'no':
#                 self.action()
#                 log = f"Admin '{self.nickname}' wanted to clear logs of user: '{user.nickname}'. Operation CANCELED! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#                 break
#             else:
#                 print("Invalid choice!\n")
#                 continue
#
#     def clear_all_logs(self):
#         print(f"Are you sure you want to delete all logs?")
#         while True:
#             choice = input('Print Yes or No: ')
#             if choice.lower() == "yes":
#                 self.action()
#                 with open(f"all_logs.txt", 'w', encoding='utf-8') as file:
#                     file.write("")
#                     log = f"Admin '{self.nickname}' cleared ALL logs. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                     self.logger(log)
#                     break
#             elif choice.lower() == 'no':
#                 self.action()
#                 log = f"Admin '{self.nickname}' wanted to clear ALL logs. Operation CANCELED! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#                 break
#             else:
#                 print("Invalid choice!\n")
#                 continue
#
#     def delete_all_user_posts(self, user):
#         print(f"Are you sure you want to delete {user.nickname} posts?")
#         while True:
#             choice = input('Print Yes or No: ')
#             if choice.lower() == "yes":
#                 self.action()
#                 user.posts.clear()
#                 log = f"Admin '{self.nickname}' cleared {user.nickname} posts. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#                 return True
#             elif choice.lower() == 'no':
#                 self.action()
#                 log = f"Admin '{self.nickname}' wanted to clear {user.nickname} posts. Operation CANCELED! Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#                 return False
#             else:
#                 print("Invalid choice!\n")
#                 continue
#
#     def find_user_post_by_id(self, user):
#         post_id = input("Enter post id to find: ")
#         id_to_find = 'Id: ' + post_id
#         for post in user.posts:
#             if id_to_find in post.keys():
#                 print(post[id_to_find])
#                 log = f"Admin '{self.nickname}' found '{user.nickname}' post (by id: {post_id}). Operation ID: {User.operations_qty} || Time: {time_logger()}"
#                 self.logger(log)
#                 return
#         print("Post was not found! ")
#         log = f"Admin '{self.nickname}' wanted to find '{user.nickname}' post (by id: {post_id}), but post was NOT found!. Operation ID: {User.operations_qty} || Time: {time_logger()}"
#         self.logger(log)
#
#     def ban_user(self, user):
#         self.action()
#         user.is_banned = True
#         log = f"Admin '{self.nickname}' banned user '{user.nickname}'. Operation ID: {User.operations_qty}  || Time: {time_logger()}"
#         self.logger(log)
#
#     def unban_user(self, user):
#         self.action()
#         user.is_banned = False
#         log = f"Admin '{self.nickname}' unbanned user '{user.nickname}'. Operation ID: {User.operations_qty}  || Time: {time_logger()}"
#         self.logger(log)
#
#
#
#
# bob_user = User('bob', 'bobs_email@gmail.com')
# user_admin = Administrator("Administrator", "pussy@gmail.com")
# bob_user.create_post('i love pussy')
# bob_user.create_post("i love licking")
# # print(bob_user.show_posts())
#
#
#
#
#
#
#
# # def delete_all_posts(self):
# #     print(f"Are you sure you want to delete all posts?")
# #     while True:
# #         choice = input('Print Yes or No: ')
# #         if choice.lower() == "yes":
# #             self.action()
# #             for profile in User.profiles_list:
# #                 profile.posts.clear()
# #             log = f"Admin '{self.nickname}' cleared ALL posts. Operation ID: {User.operations_qty} || Time: {time_logger()}"
# #             self.logger(log)
# #             break
# #         elif choice.lower() == 'no':
# #             self.action()
# #             log = f"Admin '{self.nickname}' wanted to clear ALL posts. Operation CANCELED! Operation ID: {User.operations_qty} || Time: {time_logger()}"
# #             self.logger(log)
# #             break
# #         else:
# #             print("Invalid choice!\n")
# #             continue
#
#
