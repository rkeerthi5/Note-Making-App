import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   username TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes(
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               note TEXT,
               FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

def register():
    username=input("Enter Username: ")
    password=input("Enter Password: ")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
    conn.commit()
    conn.close()

def login():
    username=input("Enter Username: ")
    password=input("Enter Password: ")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

    user=cursor.fetchone()
    conn.close()

    if user:
        print("Login Successful!")
        return user[0]
    else:
        print("Invalid username or password")
        return None

def save_note(user_id,note):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO notes(user_id,note) VALUES(?,?)",(user_id,note))
    conn.commit()
    conn.close()
    print("Note saved successfully!")

def display_notes(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE user_id=?",(user_id,))
    notes=cursor.fetchall()
    conn.close()

    if notes:
        print("Your Notes: ")
        for note in notes:
            print(note[2])
    else:
        print("You have no notes yet")

def main():
    create_database()

    while True:
        print("\n1. Register \n2. Login \n3. Exit")

        choice=input("Enter your choice: ")

        if choice=='1':
            register()
        elif choice=='2':
            user_id=login()
            if user_id:
                while True:
                    print("\n1. Add Note \n2. View Note \n3. Logout")

                    option=input("Enter your option: ")

                    if option=='1':
                        note=input("Start typing... ")
                        save_note(user_id,note)
                    elif option=='2':
                        display_notes(user_id)
                    elif option=='3':
                        break
                    else:
                        print("Invalid Option.")
        elif choice=='3':
            break
        else:
            print("Invalid choice.")

main()
