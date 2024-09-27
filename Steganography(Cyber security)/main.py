from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import base64
import sqlite3
from io import BytesIO
    

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            email varchar(50) not null,
                            phone integer(12) not null
                            )''')
        self.conn.commit()

    def create_user(self, username, password,email,phone):
        try:
            self.cur.execute("INSERT INTO users (username, password,email,phone) VALUES (?, ?,?,?)", (username, password,email,phone))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        self.cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cur.fetchone()
        if user:
            return True
        else:
            return False

class IMG_Stegno:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.root = Tk()
        self.root.title('ImageSteganography')
        self.root.geometry('500x600')
        self.root.resizable(width=False, height=False)
        self.root.config(bg='#e3f4f1')
        self.current_user = None
        self.create_welcome_frame()

    def create_welcome_frame(self):
        self.clear_screen()
        welcome_label = Label(self.root, text='Welcome to Image Steganography', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        welcome_label.pack(pady=50)

        signup_button = Button(self.root, text='Sign Up', command=self.signup_frame, font=('Helvetica', 14), bg='#e8c1c7')
        signup_button.pack(pady=20)

        login_button = Button(self.root, text='Login', command=self.login_frame, font=('Helvetica', 14), bg='#e8c1c7')
        login_button.pack()
    def signup_frame(self):
        self.clear_screen()

        title = Label(self.root, text='Sign Up', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        title.pack(pady=10)

        username_frame = Frame(self.root, bg='#e3f4f1')
        username_frame.pack(pady=5)
        username_label = Label(username_frame, text='Username:', font=('Helvetica', 14), bg='#e3f4f1')
        username_label.pack(side=LEFT)
        self.username_entry = Entry(username_frame)
        self.username_entry.pack(side=LEFT)

        password_frame = Frame(self.root, bg='#e3f4f1')
        password_frame.pack(pady=5)
        password_label = Label(password_frame, text='Password:', font=('Helvetica', 14), bg='#e3f4f1')
        password_label.pack(side=LEFT)
        self.password_entry = Entry(password_frame, show='*')
        self.password_entry.pack(side=LEFT)

        email_frame = Frame(self.root, bg='#e3f4f1')
        email_frame.pack(pady=5)
        email_label = Label(email_frame, text='Email   :', font=('Helvetica', 14), bg='#e3f4f1')
        email_label.pack(side=LEFT)
        self.email_entry = Entry(email_frame)
        self.email_entry.pack(side=LEFT)

        phone_frame = Frame(self.root, bg='#e3f4f1')
        phone_frame.pack(pady=5)
        phone_label = Label(phone_frame, text='Phone   :', font=('Helvetica', 14), bg='#e3f4f1')
        phone_label.pack(side=LEFT)
        self.phone_entry = Entry(phone_frame)
        self.phone_entry.pack(side=LEFT)

        signup_button = Button(self.root, text='Sign Up', command=self.signup, font=('Helvetica', 14), bg='#e8c1c7')
        signup_button.pack(pady=10)

        back_button = Button(self.root, text='Back', command=self.create_welcome_frame, font=('Helvetica', 14), bg='#e8c1c7')
        back_button.pack(pady=10)



    def login_frame(self):
        self.clear_screen()

        title = Label(self.root, text='Login', font=('Times new roman', 25, 'bold'), bg='#e3f4f1')
        title.pack(pady=10)

        username_frame = Frame(self.root, bg='#e3f4f1')
        username_frame.pack(pady=5)
        username_label = Label(username_frame, text='Username:', font=('Helvetica', 14), bg='#e3f4f1')
        username_label.pack(side=LEFT)
        self.username_entry = Entry(username_frame)
        self.username_entry.pack(side=LEFT)

        password_frame = Frame(self.root, bg='#e3f4f1')
        password_frame.pack(pady=5)
        password_label = Label(password_frame, text='Password:', font=('Helvetica', 14), bg='#e3f4f1')
        password_label.pack(side=LEFT)
        self.password_entry = Entry(password_frame, show='*')
        self.password_entry.pack(side=LEFT)

        login_button = Button(self.root, text='Login', command=self.login, font=('Helvetica', 14), bg='#e8c1c7')
        login_button.pack(pady=10)

        back_button = Button(self.root, text='Back', command=self.create_welcome_frame, font=('Helvetica', 14), bg='#e8c1c7')
        back_button.pack(pady=10)


    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone= self.phone_entry.get()
        if username and password:
            if self.db.create_user(username, password,email,phone,):
                messagebox.showinfo('Success', 'Account created successfully!')
                self.clear_screen()
                self.main(self.root)
            else:
                messagebox.showerror('Error', 'Username already exists!')
        else:
            messagebox.showerror('Error', 'Please fill in all fields!')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if self.db.validate_user(username, password):
                messagebox.showinfo('Success', 'Login successful!')
                self.clear_screen()
                self.main(self.root)
                # Proceed with the rest of your application after login
            else:
                messagebox.showerror('Error', 'Invalid username or password!')
        else:
            messagebox.showerror('Error', 'Please fill in all fields!')
    def main(self,root):
        
        root.title('ImageSteganography')
        root.geometry('500x600')
        root.resizable(width =False, height=False)
        root.config(bg = '#e3f4f1')
        frame = Frame(root)
        frame.grid()
        title = Label(frame,text='Image Steganography')
        title.config(font=('Times new roman',25, 'bold'))
        title.grid(pady=10)
        title.config(bg = '#e3f4f1')
        title.grid(row=1)
        encode = Button(frame,text="Encode",command= lambda :self.encode_frame1(frame), padx=14,bg = '#e3f4f1' )
        encode.config(font=('Helvetica',14), bg='#e8c1c7')
        encode.grid(row=2)
        decode = Button(frame, text="Decode",command=lambda :self.decode_frame1(frame), padx=14,bg = '#e3f4f1')
        decode.config(font=('Helvetica',14), bg='#e8c1c7')
        decode.grid(pady = 12)
        decode.grid(row=3)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
    def back(self,frame):
        frame.destroy()
        self.main(self.root)
    def encode_frame1(self,F):
        F.destroy()
        F2 = Frame(self.root)
        label1= Label(F2,text='Select the Image in which \nyou want to hide text :')
        label1.config(font=('Times new roman',25, 'bold'),bg = '#e3f4f1')
        label1.grid()
        button_bws = Button(F2,text='Select',command=lambda : self.encode_frame2(F2))
        button_bws.config(font=('Helvetica',18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(F2, text='Cancel', command=lambda : IMG_Stegno.back(self,F2))
        button_back.config(font=('Helvetica',18),bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()
    #DataFlair- frame for decode page
    def decode_frame1(self,F):
        F.destroy()
        d_f2 = Frame(self.root)
        label1 = Label(d_f2, text='Select Image with Hidden text:')
        label1.config(font=('Times new roman',25,'bold'),bg = '#e3f4f1')
        label1.grid()
        label1.config(bg = '#e3f4f1')
        button_bws = Button(d_f2, text='Select', command=lambda :self.decode_frame2(d_f2))
        button_bws.config(font=('Helvetica',18), bg='#e8c1c7')
        button_bws.grid()
        button_back = Button(d_f2, text='Cancel', command=lambda : IMG_Stegno.back(self,d_f2))
        button_back.config(font=('Helvetica',18), bg='#e8c1c7')
        button_back.grid(pady=15)
        button_back.grid()
        d_f2.grid()
    #DataFlair- function to encode image 
    def encode_frame2(self,e_F2):
        e_pg = Frame(self.root)
        myfile = tkinter.filedialog.askopenfilename(filetypes=[('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
        else:
            my_img = Image.open(myfile)
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)
            image = Label(e_pg, text='Selected Image')
            image.config(font=('Helvetica', 14, 'bold'))
            image.grid()
            board = Label(e_pg, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid()
            msg= Label(e_pg, text='Enter the message')
            msg.config(font=('Helvetica', 14, 'bold'))
            msg.grid(pady=15)
            text_a = Text(e_pg, width=50, height=5)
            text_a.grid()
            encode_button = Button(e_pg, text='Cancel', command=lambda: IMG_Stegno.back(self, e_pg))
            encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back = Button(e_pg, text='Encode', command=lambda: [self.enc_fun(text_a,my_img),IMG_Stegno.back(self,e_pg)])
            button_back.config(font=('Helvetica',14), bg='#e8c1c7')
            button_back.grid(pady=15)
            encode_button.grid()
            e_pg.grid(row=1)
            e_F2.destroy()
    #DataFlair- function to decode image 
    def decode_frame2(self,d_F2):
        d_F3 = Frame(self.root)
        myfiles = tkinter.filedialog.askopenfilename(filetypes = ([('png', '*.png'),('jpeg', '*.jpeg'),('jpg', '*.jpg'),('All Files', '*.*')]))
        if not myfiles:
            messagebox.showerror("Error","You have selected nothing! ")
        else:
            my_img = Image.open(myfiles, 'r')
            my_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(my_image)
            label4= Label(d_F3,text='Selected Image :')
            label4.config(font=('Helvetica',14,'bold'))
            label4.grid()
            board = Label(d_F3, image=img)
            board.image = img
            board.grid()
            before=self.decode(my_img)
            label2 = Label(d_F3, text='Encrypted Hidden data is :')
            label2.config(font=('Helvetica',14,'bold'))
            label2.grid(pady=10)
            text_a = Text(d_F3, width=50, height=5)
            text_a.insert(INSERT,before)
            text_a.configure(state='disabled')
            text_a.grid()
            after=self.Decrypt(before)
            label3 = Label(d_F3, text='Decrypted Hidden data is :')
            label3.config(font=('Helvetica',14,'bold'))
            label3.grid(pady=10)
            text_b = Text(d_F3, width=50, height=5)
            text_b.insert(INSERT,after)
            text_b.configure(state='disabled')
            text_b.grid()
            button_back = Button(d_F3, text='Cancel', command= lambda :self.frame_3(d_F3))
            button_back.config(font=('Helvetica',14),bg='#e8c1c7')
            button_back.grid(pady=15)
            button_back.grid()
            d_F3.grid(row=1)
            d_F2.destroy()
    #DataFair- function to decode data
    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                return data

    #DataFlair- function to generate data
    def generate_Data(self,data):
        new_data = []
        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data
    #DataFlair- function to modify the pixels of image
    def modify_Pix(self,pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):
            # Extracting 3 pixels at a time
            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]
            
            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            
            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]
    #DataFlair- function to enter the data pixels in image
    def encode_enc(self,newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):
            # Putting modified pixels in the new image
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def Encrypt(self,message):
        key=4
        encrypted_message = ""
        for char in message:
            encrypted_message += chr(ord(char) ^ key)
        return encrypted_message

    def Decrypt(self,encrypted_message):
        key=4
        decrypted_message = ""
        for char in encrypted_message:
            decrypted_message += chr(ord(char) ^ key)
        return decrypted_message
    #DataFlair- function to enter hidden text
    def enc_fun(self,text_a,myImg):
        data = text_a.get("1.0", "end-1c")
        print(data)
        data=self.Encrypt(data)
        print(data)
        if (len(data) == 0):
            messagebox.showinfo("Alert","Kindly enter text in TextBox")
        else:
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            my_file = BytesIO()
            temp=os.path.splitext(os.path.basename(myImg.filename))[0]
            newImg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp,filetypes = ([('png', '*.png')]),defaultextension=".png"))
            self.d_image_size = my_file.tell()
            self.d_image_w,self.d_image_h = newImg.size
            messagebox.showinfo("Success","Encoding Successful\nFile is saved as Image_with_hiddentext.png in the same directory")

    def frame_3(self,frame):
        frame.destroy()
        self.main(self.root)
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    db_name = "user.db"
    app = IMG_Stegno(db_name)
    app.root.mainloop()
