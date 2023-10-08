import sqlite3

database = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = database.cursor()

print("""Choose what you want to do:
1. Assign creator
2. Demote""")

a = int(input()) 

print("Enter user ID: ")

user_id = int(input())

if a == 1: 
    print(f'User ({user_id}) was assigned as creator')
    cursor.execute(f'UPDATE users SET user_capabilities == "admin" WHERE user_id == {user_id}')
elif a == 2:
    print(f'User ({user_id}) was demoted')
    cursor.execute(f'UPDATE users SET user_capabilities == Null WHERE user_id == {user_id}')
else:
    print("Err: хуета какая-то")

database.commit()
database.close()