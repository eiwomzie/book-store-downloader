from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import urllib.request as urllib
import os


selected_title = None
selected_link = None
selected_title1 = None
selected_link1 = None
book_dict = {}
book_dict1 = {}
downloaded_books= []

##### MICHELLE'S DEF CODE
def show_frame(frame):
    frame.tkraise()

def password_command():
    if password_entry1.cget('show') == '•':
        password_entry1.config(show='')
    else:
        password_entry1.config(show='•')

def login():
    conn= sqlite3.connect('ReGLog.db')
    cursor= conn.cursor()

    find_user= 'SELECT * FROM RegLog WHERE EMAIL = ? and password =?'
    cursor.execute(find_user, [(email_entry.get()), (password_entry.get())])

    result= cursor.fetchall()
    if result:
        messagebox.showinfo('Success', 'You have logged in successfully to your Book Store Downloader')
        show_frame(BookPage)
    else:
        messagebox.showerror('Failed', 'Wrong Login details, please try again')

def forgot_password():
    win = Toplevel()
    window_width = 350
    window_height = 350
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    position_top = int(screen_height / 4 - window_height / 4)
    position_right = int(screen_width / 2 - window_width / 2)
    win.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    win.title('Forgot Password')
    win.iconbitmap(r'C:\Users\USER\Pictures\loginpics\aa.ico')
    win.configure(background='#f8f8f8')
    win.resizable(0, 0)

    #variables
    email = StringVar()
    password= StringVar()
    confirmPassword= StringVar()


    # ====== Email ====================
    email_entry2 = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2, textvariable=email)
    email_entry2.place(x=40, y=30, width=256, height=34)
    email_entry2.config(highlightbackground="black", highlightcolor="black")
    email_label2 = Label(win, text='• Email account', fg="#89898b", bg='#f8f8f8',
                         font=("yu gothic ui", 11, 'bold'))
    email_label2.place(x=40, y=0)

    # ====  New Password ==================
    new_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2, textvariable=password)
    new_password_entry.place(x=40, y=110, width=256, height=34)
    new_password_entry.config(highlightbackground="black", highlightcolor="black")
    new_password_label = Label(win, text='• New Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
    new_password_label.place(x=40, y=80)

    # ====  Confirm Password ==================
    confirm_password_entry = Entry(win, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2, textvariable=confirmPassword)
    confirm_password_entry.place(x=40, y=190, width=256, height=34)
    confirm_password_entry.config(highlightbackground="black", highlightcolor="black")
    confirm_password_label = Label(win, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                                   font=("yu gothic ui", 11, 'bold'))
    confirm_password_label.place(x=40, y=160)

    # ======= Update password Button ============
    update_pass = Button(win, fg='#f8f8f8', text='Update Password', bg='#1b87d2', font=("yu gothic ui bold",14),
                         cursor='hand2', activebackground='#1b87d2', command= lambda: change_password())
    update_pass.place(x=40, y=240, width=256, height=50)

    #================= DATABASE CONNECTION FOR FORGOT PASSWORD===========
    def change_password():
        if new_password_entry.get()== confirm_password_entry.get():
            db= sqlite3.connect('Reglog.db')
            cur= db.cursor()

            insert= '''update Reglog set Password= ?, ConfirmPassword=? where Email=?'''
            cur.execute(insert, [new_password_entry.get(), confirm_password_entry.get(), email_entry2.get()])
            db.commit()
            db.close()
            messagebox.showinfo('Congrats', 'Password changed successfully')
        else:
            messagebox.showerror('Error', "Password didn't match")

def password_command2():
    if password_entry.cget('show') == '•':
        password_entry.config(show='')
    else:
        password_entry.config(show='•')

def submit():
    check_counter= 0
    warn= ''
    if name_entry.get()== '':
        warn= "full Name field can't be empty"
    else:
        check_counter += 1

    if email_entry.get() =='':
        warn= "Email field can't be empty"
    else:
        check_counter += 1

    if password_entry.get()=='':
        warn="Password field can't be empty"
    else:
        check_counter += 1

    if confirmPassword_entry.get() == '':
        warn = "Sorry can't sign up, make sure all fields are complete"
    else:
        check_counter += 1

    if password_entry.get() != confirmPassword_entry.get():
        warn = "Password did not match"
    else:
        check_counter += 1


    if check_counter == 5:
        try:
            connection= sqlite3.connect('Reglog.db')
            cur= connection.cursor()
            cur.execute('INSERT INTO Reglog values(?,?,?,?)',
                        (Email.get(), FullName.get(), Password.get(), ConfirmPassword.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo('Success', 'New Book Store account created Successfully')
        except Exception as ep:
            messagebox.showerror(  '', ep)
    else:
        messagebox.showerror('Error', warn)

### IWOMI'S DEF CODE
def search():
    # Clear the existing list of books
    listbox.delete(0, END)

    # Ask the user for the book name to search for
    book_name = search_bar.get()
    if ' ' in book_name:
        url_bookname = book_name.replace(' ', '+') + '&submit_search=Go%21'
    else:
        url_bookname = book_name + '&submit_search=Go%21'

    book_dict = search_book_online(url_bookname)

    # Add book titles to the listbox
    if book_dict:
        for i, title in enumerate(book_dict.keys(), start=1):
            listbox.insert(END, f"{i}. {title}")
        if i < 3 or i == 2:
            messagebox.showinfo("Not Found", "Book not found, Click more to search for more books")
    else:
        messagebox.showerror("Not Found", "Book not found, Click more to search for more books")

def more_books():
    global book_dict1
    downloaded_books.clear()
    book_dict.clear()
    listbox.delete(0, END)
    book_name = search_bar.get()

    url_bookname = book_name.replace(' ', '-') + '-books.html'
    url = 'https://www.pdfdrive.com/' + url_bookname
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}
    webpage = requests.get(url, headers=headers)

    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.text, "html.parser")
        book_elements = soup.find_all('h2')
        book_dict1 = {}

        for element in book_elements:
            title = element.text.strip()
            link_tag = element.find_parent('a')
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
                book_dict1[title] = link
    else:
        messagebox.showerror("Not Reachable", "Website could not be reached")

    if book_dict1:
        for i, title in enumerate(book_dict1.keys(), start=1):
            listbox.insert(END, f"{i}. {title}")
        if i < 3 or i == 2:
            messagebox.showinfo("Not Found", "Book not found, Click EXIT to end program\n or search for another book")
    else:
        messagebox.showerror("Not Found", "Book not found, Click EXIT to end program\n or search for another book")

def search_book_online(url_bookname):
    global book_dict
    url = 'https://www.gutenberg.org/ebooks/search/?query=' + url_bookname
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}
    webpage = requests.get(url, headers=headers)

    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.text, "html.parser")
        book_elements = soup.find_all('span', class_='title')[4:]
        book_dict = {}

        for element in book_elements:
            title = element.text.strip()
            link_tag = element.find_parent('a')
            if link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
                book_dict[title] = link

        return book_dict
    else:
        messagebox.showerror("Not Reachable", "Website could not be reached")
        return {}


def highlighted_book(event, book_dict, book_dict1):
    global selected_title, selected_link, selected_title1, selected_link1
    # Get the indices of the selected items
    selected_indices = listbox.curselection()
    if book_dict:
        if selected_indices:
            # Get the index of the first selected item
            index = selected_indices[0]
            # Get the title of the selected book
            selected_title = listbox.get(index).split(". ", 1)[1]
            # Get the link of the selected book from the book_dict
            selected_link = book_dict.get(selected_title)
        else:
            messagebox.showerror("Error", "No book selected. Please click twice to view\n or type in a book in the search box.")
    elif book_dict1:
        if selected_indices:
            # Get the index of the first selected item
            index = selected_indices[0]
            # Get the title of the selected book
            selected_title1 = listbox.get(index).split(". ", 1)[1]
            # Get the link of the selected book from the book_dict
            selected_link1 = book_dict1.get(selected_title1)
        else:
            messagebox.showerror("Error", "No book selected. Please click twice to view\n or type in a book in the search box.")

def book_edited(selected_title, selected_link):
    url = 'https://www.gutenberg.org/' + selected_link
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"}
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.text, 'html.parser')
    download_book(selected_title, soup)

def download_book(selected_title, soup):
    file_name = f"{selected_title}.zip"
    picture_name = f"{selected_title}.jpg"
    zip_links = soup.find('a', attrs={'type': 'application/zip'})
    for tag in zip_links:
        link = zip_links['href']
    response = requests.get('https://www.gutenberg.org/' + link)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        messagebox.showinfo("Downloaded", f"Book downloaded successfully as {file_name}")
        downloaded_books.append(selected_title)
    else:
        messagebox.showinfo("Not Downloaded", f"{file_name} could not be downloaded")

def view_downloaded_books():
    # Create a new window for displaying downloaded books
    downloaded_books_window = Toplevel()
    downloaded_books_window.title('Downloaded Books')

    # Create a listbox to display downloaded books
    downloads_listbox = Listbox(downloaded_books_window, width=50, height=20)
    downloads_listbox.pack()

    # Bind double-click event to open_book function
    downloads_listbox.bind('<Double-Button-1>', lambda event: open_book(event, downloads_listbox))

    # Populate the listbox with downloaded books
    for book in downloaded_books:
        if book:
            downloads_listbox.insert(END, book)
def download_pdfdrive(selected_title1, selected_link1):
    download_link = 'https://www.pdfdrive.com/' + selected_link1
    webpage = urllib.urlopen(download_link)
    file_name = f"{selected_title1}.html"
    if webpage.status == 200:
        with open(file_name, 'wb') as file:
            for line in webpage:
                file.write(line)
        messagebox.showinfo("Downloaded", f"Book downloaded successfully as {file_name}")
        downloaded_books.append(selected_title1)
    else:
        messagebox.showinfo("Not Downloaded", f"{file_name} could not be downloaded")

def open_book(event,downloads_listbox):
    # Get the index of the selected book
    index = downloads_listbox.curselection()[0]
    # Get the title of the selected book
    selected_book = downloads_listbox.get(index)
    if book_dict:
        os.startfile(f'{selected_book}.zip')
    elif book_dict1:
        os.startfile(f'{selected_book}.html')

def clear_window():
    downloaded_books.clear()
    book_dict.clear()
    book_dict1.clear()

def download_btn_clicked():
    if selected_title and selected_link:
        book_edited(selected_title, selected_link)
    elif selected_title1 and selected_link1:
        download_pdfdrive(selected_title1, selected_link1)

#########  MICHELLE'S MAINCODE

window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')
window.title('BOOK STORE DOWNLOADER')


#window icon Photo
icon= PhotoImage(file=r'C:\Users\USER\Pictures\loginpics\pic-icon.png')
window.iconphoto(True, icon)

LoginPage = Frame(window)
RegistrationPage = Frame(window)
BookPage = Frame(window)

for frame in (LoginPage, RegistrationPage, BookPage):
    frame.grid(row=0, column=0, sticky='nsew')


show_frame(LoginPage)

#database variable
Email = StringVar()
FullName = StringVar()
Password = StringVar()
ConfirmPassword = StringVar()


# =====================================================================================================================
# =====================================================================================================================
# ==================== LOGIN PAGE =====================================================================================
# =====================================================================================================================
# =====================================================================================================================

design_frame1 = Listbox(LoginPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame1.place(x=0, y=0)

design_frame2 = Listbox(LoginPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame2.place(x=676, y=0)

design_frame3 = Listbox(LoginPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame3.place(x=75, y=106)

design_frame4 = Listbox(LoginPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame4.place(x=676, y=106)

# ====== Email ====================
email_entry = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable=Email)
email_entry.place(x=134, y=170, width=256, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame4, text='• Email account', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=130, y=140)

# ==== Password ==================
password_entry1 = Entry(design_frame4, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                        textvariable=Password)
password_entry1.place(x=134, y=250, width=256, height=34)
password_entry1.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame4, text='• Password', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
password_label.place(x=130, y=220)


# ====== checkbutton ==============
checkButton = Checkbutton(design_frame4, bg='#f8f8f8', command=password_command, text='show password')
checkButton.place(x=140, y=288)

# ========= Buttons ===============
SignUp_button = Button(LoginPage, text='Sign up', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                       command=lambda: show_frame(RegistrationPage), borderwidth=0, activebackground='#1b87d2', cursor='hand2')
SignUp_button.place(x=1100, y=175)

# ===== Welcome Label ==============
welcome_label = Label(design_frame4, text='Welcome', font=('Arial', 20, 'bold'), bg='#f8f8f8')
welcome_label.place(x=130, y=15)

# ======= top Login Button =========
login_button = Button(LoginPage, text='Login', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                      borderwidth=0, activebackground='#1b87d2', command=lambda: login(),cursor='hand2')
login_button.place(x=845, y=175)

login_line = Canvas(LoginPage, width=60, height=5, bg='#1b87d2')
login_line.place(x=840, y=203)

# ==== LOGIN  down button ============
loginBtn1 = Button(design_frame4, fg='#f8f8f8', text='Login', bg='#1b87d2', font=("yu gothic ui bold", 15),
                   cursor='hand2', activebackground='#1b87d2', command= lambda: login())
loginBtn1.place(x=133, y=340, width=256, height=50)

#========LOGIN DATABASE CONNECTION====

# ======= ICONS =================

# ===== Email icon =========
email_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\email-icon.png')
photo = ImageTk.PhotoImage(email_icon)
emailIcon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
emailIcon_label.image = photo
emailIcon_label.place(x=105, y=174)

# ===== password icon =========
password_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\pass-icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
password_icon_label.image = photo
password_icon_label.place(x=105, y=254)

# ===== picture icon =========
picture_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\pic-icon.png')
photo = ImageTk.PhotoImage(picture_icon)
picture_icon_label = Label(design_frame4, image=photo, bg='#f8f8f8')
picture_icon_label.image = photo
picture_icon_label.place(x=280, y=5)

# ===== Left Side Picture ============
side_image = Image.open(r'C:\Users\USER\Pictures\loginpics\vector.png')
photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(design_frame3, image=photo, bg='#1e85d0')
side_image_label.image = photo
side_image_label.place(x=50, y=10)




# ===================================================================================================================
# ===================================================================================================================
# === FORGOT PASSWORD  PAGE =========================================================================================
# ===================================================================================================================
# ===================================================================================================================

forgotPassword = Button(design_frame4, text='Forgot password', font=("yu gothic ui", 8, "bold underline"), bg='#f8f8f8',
                        borderwidth=0, activebackground='#f8f8f8', command= lambda: forgot_password(), cursor='hand2')
forgotPassword.place(x=290, y=290)




# =====================================================================================================================
# =====================================================================================================================
# ==================== REGISTRATION PAGE ==============================================================================
# =====================================================================================================================
# =====================================================================================================================

design_frame5 = Listbox(RegistrationPage, bg='#0c71b9', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame5.place(x=0, y=0)

design_frame6 = Listbox(RegistrationPage, bg='#1e85d0', width=115, height=50, highlightthickness=0, borderwidth=0)
design_frame6.place(x=676, y=0)

design_frame7 = Listbox(RegistrationPage, bg='#1e85d0', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame7.place(x=75, y=106)

design_frame8 = Listbox(RegistrationPage, bg='#f8f8f8', width=100, height=33, highlightthickness=0, borderwidth=0)
design_frame8.place(x=676, y=106)

# ==== Full Name =======
name_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                   textvariable= FullName)
name_entry.place(x=284, y=150, width=286, height=34)
name_entry.config(highlightbackground="black", highlightcolor="black")
name_label = Label(design_frame8, text='•Full Name', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
name_label.place(x=280, y=120)

# ======= Email ===========
email_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                    textvariable= Email)
email_entry.place(x=284, y=220, width=286, height=34)
email_entry.config(highlightbackground="black", highlightcolor="black")
email_label = Label(design_frame8, text='•Email', fg="#89898b", bg='#f8f8f8', font=("yu gothic ui", 11, 'bold'))
email_label.place(x=280, y=190)

# ====== Password =========
password_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2,
                       textvariable= Password)
password_entry.place(x=284, y=295, width=286, height=34)
password_entry.config(highlightbackground="black", highlightcolor="black")
password_label = Label(design_frame8, text='• Password', fg="#89898b", bg='#f8f8f8',
                       font=("yu gothic ui", 11, 'bold'))
password_label.place(x=280, y=265)

checkButton = Checkbutton(design_frame8, bg='#f8f8f8', command=password_command2, text='show password')
checkButton.place(x=290, y=330)


# ====== Confirm Password =============
confirmPassword_entry = Entry(design_frame8, fg="#a7a7a7", font=("yu gothic ui semibold", 12), highlightthickness=2,
                              textvariable= ConfirmPassword)
confirmPassword_entry.place(x=284, y=385, width=286, height=34)
confirmPassword_entry.config(highlightbackground="black", highlightcolor="black")
confirmPassword_label = Label(design_frame8, text='• Confirm Password', fg="#89898b", bg='#f8f8f8',
                              font=("yu gothic ui", 11, 'bold'))
confirmPassword_label.place(x=280, y=355)

# ========= Buttons ====================
SignUp_button = Button(RegistrationPage, text='Sign up', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                       command=lambda: show_frame(LoginPage), borderwidth=0, activebackground='#1b87d2', cursor='hand2')
SignUp_button.place(x=1100, y=175)

SignUp_line = Canvas(RegistrationPage, width=60, height=5, bg='#1b87d2')
SignUp_line.place(x=1100, y=203)

# ===== Welcome Label ==================
welcome_label = Label(design_frame8, text='Welcome', font=('Arial', 20, 'bold'), bg='#f8f8f8')
welcome_label.place(x=130, y=15)

# ========= Login Button =========
login_button = Button(RegistrationPage, text='Login', font=("yu gothic ui bold", 12), bg='#f8f8f8', fg="#89898b",
                      borderwidth=0, activebackground='#1b87d2', command=lambda: show_frame(LoginPage), cursor='hand2')
login_button.place(x=845, y=175)

# ==== SIGN UP down button ============
signUp2 = Button(design_frame8, fg='#f8f8f8', text='Sign Up', bg='#1b87d2', font=("yu gothic ui bold", 15),
                 cursor='hand2', activebackground='#1b87d2', command=lambda: submit())
signUp2.place(x=285, y=435, width=286, height=50)

# ===== password icon =========
password_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\pass-icon.png')
photo = ImageTk.PhotoImage(password_icon)
password_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
password_icon_label.image = photo
password_icon_label.place(x=255, y=300)

# ===== confirm password icon =========
confirmPassword_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\pass-icon.png')
photo = ImageTk.PhotoImage(confirmPassword_icon)
confirmPassword_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
confirmPassword_icon_label.image = photo
confirmPassword_icon_label.place(x=255, y=390)

# ===== Email icon =========
email_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\email-icon.png')
photo = ImageTk.PhotoImage(email_icon)
emailIcon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
emailIcon_label.image = photo
emailIcon_label.place(x=255, y=225)

# ===== Full Name icon =========
name_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\name-icon.png')
photo = ImageTk.PhotoImage(name_icon)
nameIcon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
nameIcon_label.image = photo
nameIcon_label.place(x=252, y=153)

# ===== picture icon =========
picture_icon = Image.open(r'C:\Users\USER\Pictures\loginpics\pic-icon.png')
photo = ImageTk.PhotoImage(picture_icon)
picture_icon_label = Label(design_frame8, image=photo, bg='#f8f8f8')
picture_icon_label.image = photo
picture_icon_label.place(x=280, y=5)

# ===== Left Side Picture ============
side_image = Image.open(r'C:\Users\USER\Pictures\loginpics\vector.png')
photo = ImageTk.PhotoImage(side_image)
side_image_label = Label(design_frame7, image=photo, bg='#1e85d0')
side_image_label.image = photo
side_image_label.place(x=50, y=10)


# =====================================================================================================================
# =====================================================================================================================
# ==================== DATABASE CONNECTION ============================================================================
# =====================================================================================================================
# =====================================================================================================================

connection= sqlite3.connect('Reglog.db')
cur= connection.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS RegLog(Email TEXT PRIMARY KEY, FullName TEXT, Password TEXT,'
            'ConfirmPassword TEXT)')
connection.commit()
connection.close()

### IWOMI'S MAIN CODE


# BookPage.title('BOOK STORE DOWNLOADER')
# BookPage.iconbitmap(r'C:\Users\USER\Pictures\icontable.ico')
# BookPage.geometry('800x700')
BookPage.configure(background='black')
# BookPage.state('zoomed')


# Create a label for the title
mylabel = Label(BookPage, text='Welcome To Book Store Downloader', font=('yu gothic ui', 20, 'bold'),bg='purple',fg='white')
mylabel.grid(row=0, column=1, columnspan=5)

# Create a search bar and label
search_bar = Entry(BookPage, width=70, bg='white', borderwidth=3)
search_bar.grid(row=1, column=1, padx=20, pady=20)
search_bar_label = Label(BookPage, text='Search Book By Name')
search_bar_label.grid(row=1, column=0)

# Create a frame to hold the list of books
frame = Frame(BookPage)
frame.grid(row=2, column=1, columnspan=7, padx=5, pady=5)

# Create a label for the list of books
label_frame = Label(frame, text='See Available Books')
label_frame.grid(row=0, column=2)

# Create a listbox to display the books
listbox = Listbox(frame, width=150, height=20)
listbox.grid(row=1, column=2, padx=10, pady=10)
listbox.bind('<<ListboxSelect>>', lambda event: highlighted_book(event, book_dict, book_dict1))

# Create a scroll bar for the listbox
scrollbar = Scrollbar(frame, orient=VERTICAL)
scrollbar.grid(row=1, column=3, sticky=N + S)
# Link the scroll bar to the listbox
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Create a search button
search_btn = Button(BookPage, text='Search', command=search)
search_btn.grid(row=1, column=2)

# Create a download button
download_btn = Button(BookPage, text='Download', command=download_btn_clicked)
download_btn.grid(row=3, column=1,columnspan=5,ipadx=50,padx=5,pady=5)

# Create a more button
more_btn = Button(BookPage, text='more', command= more_books)
more_btn.grid(row=4, column=1,columnspan=5,ipadx=50,padx=5,pady=5)

# Create a view download button
view_btn = Button(BookPage, text='View Downloads', command=view_downloaded_books)
view_btn.grid(row=5, column=1,columnspan=5,ipadx=50,padx=5,pady=5)




quit_button= Button(BookPage, text='EXIT', command=lambda:[window.quit(), clear_window()])
quit_button.grid(row=6,column=1,columnspan=5,ipadx=180,padx=5,pady=5)



window.mainloop()