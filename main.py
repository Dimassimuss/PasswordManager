from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generating():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list.append([random.choice(letters) for l in range(nr_letters)])
    password_list.append([random.choice(symbols) for s in range(nr_symbols)])
    password_list.append([random.choice(numbers) for n in range(nr_numbers)])

    password_list = [*password_list[0], *password_list[1], *password_list[2]]
    random.shuffle(password_list)

    password = ''.join([str(char) for char in password_list])
    password_entry.delete(0, END)
    password_entry.insert(END, f'{password}')
    pyperclip.copy(password)

# ---------------------------- SEARCHING ------------------------------- #
def find_password():

    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title='Error', message='File does not exist')
    else:
        if website_entry.get() in data:
            searching_info = data[f'{website_entry.get()}']
            messagebox.showinfo(title='Results', message=f'Your password: {searching_info["password"]}\n'
                                                         f'Your login: {searching_info["email"]}')
        else:
            messagebox.showerror(title='Error', message='No details for the website exists')



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_data = website_entry.get()
    user_name_data = user_name_entry.get()
    password_data = password_entry.get()
    new_data = {
        website_data: {
            'email': user_name_data,
            'password': password_data
        }
    }

    if len(website_data) == 0 or len(password_data) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image = logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text='Website: ')
website_label.grid(column=0, row=1)
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

user_name_label = Label(text='Email/Username: ')
user_name_label.grid(column=0, row=2)
user_name_entry = Entry(width=35)
user_name_entry.insert(END, 'itachi@uchiha.com')
user_name_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text='Password: ')
password_label.grid(column=0, row=3)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)
generate_button = Button(text='Generate Password', command=password_generating)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text='Search', width=21, command=find_password)
search_button.grid(column=2, row=1)







window.mainloop()