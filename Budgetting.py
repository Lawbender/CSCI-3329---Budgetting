import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3 
import time 
from customtkinter import *

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS userInfo(
    username text,
    password text,
    first_name text,
    last_name text,
    pronoun text,
    age integer,
    accountBalance real,
    savingBalance real,
    monthlyIncome real
    
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS user_goals (
    username text,
    goal text 
)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
    username text,
    expense text ,
    expense_price real,
    subscription text,
    subscription_price real
)""")
connection.commit()
connection.close()



def main():
    app = App()
    app.mainloop()
class MyFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class myWindow(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = CTkLabel(master=self)
        self.clock.place(relx=0, rely=1, anchor='sw')
        self.getTime()
    
    def getTime(self):
        clockTime = time.strftime("%c")
        self.clock.configure(text=clockTime)
        self.clock.after(1000, self.getTime)


class App(myWindow):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        CTkButton(master = self.my_frame, text = "Login", command=self.login).grid(padx = 150,pady=20, row = 1, column=0)
        CTkButton(master = self.my_frame, text = "Register", command=self.register).grid(padx = 100,pady=10,row = 2, column=0)
    def show(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        data = cursor.execute("SELECT * FROM userInfo")
        table = ""
        for item in data:
            table += str(item) + "\n"
        CTkLabel(self.my_frame, text=table ).grid()
        data = cursor.execute("SELECT * FROM expenses")
        table = ""
        for item in data:
            table += str(item) + "\n"
        CTkLabel(self.my_frame, text=table ).grid()
        
    def login(self):
        login = Login()
        login.mainloop()
        
    def register(self):
        register = Register()
        register.mainloop()
class Login(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x500")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        CTkLabel(master = self.my_frame, text = "Username").grid(padx = 100, row = 1, column=0)
        self.username = CTkEntry(master=self.my_frame,placeholder_text="Username" )
        self.username.grid(row = 1, column=1)

        CTkLabel(master = self.my_frame, text = "Password").grid(padx = 100, row = 2, column=0)
        self.password = CTkEntry(master=self.my_frame,placeholder_text="Password" , show="*")
        self.password.grid(row = 2, column=1)
        CTkButton(master = self.my_frame, text="Login",command=self.verify).grid(row=3,padx=50,columnspan=2)
        
    def verify(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        # Execute the query and retrieve the result
        cursor.execute(f"SELECT username FROM userInfo WHERE username='{self.username.get()}' AND password='{self.password.get()}'")
        result = cursor.fetchone()
        
        # Check if the result is None
        if result is not None:
            # If the result is not None, the username and password are correct
            page = MainPage(self.username.get())
            page.mainloop()
        else:
            tk.messagebox.showinfo('Error', 'Incorrect Username or Password')
        
        # Close the connection
        connection.close()
        
class Register(myWindow):
    def __init__(self):
        super().__init__()

        self.geometry("500x500")
        self.tab_view = MyRegisterTabs(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)
        
        
class MainPage(myWindow):
    def __init__(self, user):
        super().__init__()
        self.geometry("800x500")
        self.user = user
        self.myframe = MyFrame(master=self)
        self.myframe.grid(row=0, column=0, padx = 45)
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        self.balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]
        
        self.actLabel = CTkLabel(master=self.myframe, text=f" Account balance \n ${'{:.2f}'.format(self.balance)}").grid(row=0, column=0)
        
        self.balance = cursor.execute(f"SELECT SavingBalance FROM userInfo WHERE username = '{self.user}';")
        self.balance = cursor.fetchone()[0]
       
        
        CTkLabel(master=self.myframe, text=f" Savings balance \n ${'{:.2f}'.format(self.balance)}").grid(row=0, column=1)
        CTkButton(master=self.myframe, text="Deposit",command=self.addFunds).grid(pady=25, row=1, column=0)
        CTkButton(master=self.myframe, text="Withdrawl").grid(row=2, column=0)
        CTkButton(master = self.myframe,text = "Transfer",command=self.moveFunds).grid(row= 1, column = 1)
        self.goals_frame = MyFrame(master=self)
        self.goals_frame.grid(row=0, column=1)
        CTkLabel(master=self.goals_frame, text="Enter your goals:").grid(row=0, column=0)
        self.goals_entry = CTkEntry(master=self.goals_frame)
        self.goals_entry.grid(row=1, column=0)
        CTkButton(master=self.goals_frame, text="Add Goal", command=self.save_goals).grid(row=2, column=0)
        
        self.load_goals(user)
        
       
        
      
        
   
        
        
    def save_goals(self):
        goal = self.goals_entry.get()
        if goal:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO user_goals (username, goal) VALUES (?, ?)", (self.user, goal))
            connection.commit()
            connection.close()
            self.load_goals(self.user)
            self.goals_entry.delete(0, 'end')
        
    def load_goals(self, user):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        goals = cursor.execute(f"SELECT goal FROM user_goals WHERE username = '{user}';").fetchall()
        connection.close()
        for i, goal in enumerate(goals):
            CTkLabel(master=self.goals_frame, text=f"{i+1}. {goal[0]}").grid(row=i+3, column=0)

    def addFunds(self):
        win = CTkToplevel(self)
        win.geometry("300x300")
        
        CTkLabel(master = win, text = "How much would you like to deposit? ").pack()
        deposit = CTkEntry(master = win)
        deposit.pack()
        
        
        def help():
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()    
            amount = deposit.get()
            current_balance = cursor.execute(f"SELECT accountBalance FROM userInfo WHERE username = '{self.user}';").fetchone()[0]
            new_balance = current_balance+float(amount)
            cursor.execute(f"UPDATE userInfo SET accountBalance = '{new_balance}' WHERE username = '{self.user}';")
            
            connection.commit()
            connection.close()
            
            win.destroy()
        
            
        CTkButton(master = win , text = "Deposit", command =help).pack()
    
    def moveFunds(self):
        win = CTkToplevel(self)
        win.geometry("300x300")

        CTkLabel(master=win, text="How much would you like to transfer and where?").pack()
        deposit = CTkEntry(master=win)
        deposit.pack()

        def help():
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            amount = deposit.get()
            cursor.execute(f"SELECT accountBalance, savingBalance FROM userInfo WHERE username = '{self.user}';")
            result = cursor.fetchone()
            current_balance = float(result[0])
            savings_balance = float(result[1])
            new_balance = current_balance - float(amount)
            if new_balance >= 0:
                cursor.execute(f"UPDATE userInfo SET accountBalance = '{new_balance}' WHERE username = '{self.user}';")
                new_balance = savings_balance + float(amount)
                cursor.execute(f"UPDATE userInfo SET savingBalance = '{new_balance}' WHERE username = '{self.user}';")
                connection.commit()
                connection.close()
                
                win.destroy()
        def helper():
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            amount = deposit.get()
            cursor.execute(f"SELECT accountBalance, savingBalance FROM userInfo WHERE username = '{self.user}';")
            result = cursor.fetchone()
            current_balance = float(result[0])
            savings_balance = float(result[1])
            new_balance = savings_balance - float(amount)
            if new_balance >= 0:
                cursor.execute(f"UPDATE userInfo SET savingBalance = '{new_balance}' WHERE username = '{self.user}';")
                new_balance = current_balance + float(amount)
                cursor.execute(f"UPDATE userInfo SET accountBalance = '{new_balance}' WHERE username = '{self.user}';")
                connection.commit()
                connection.close()
                win.destroy()

        CTkButton(master=win, text="Transfer to Saving", command=help).pack()
        CTkButton(master = win, text= "Transer to Checking account", command = helper).pack()


    

class MyRegisterTabs(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.expenses = []
        self.sublist = []
        self.add("Personal Information")
        self.add("Banking Information")
        self.add("Sign Up")

        # add widgets on tabs
        CTkLabel(master=self.tab("Personal Information") , text="First Name").grid(row=0, column=0, padx=20, pady=10)
        self.user_first_name = CTkEntry(master=self.tab("Personal Information"))
        self.user_first_name.grid(row=1,column=0)

        CTkLabel(master=self.tab("Personal Information") , text="Last Name").grid(row=0, column=1, padx=20, pady=10)
        self.user_last_name = CTkEntry(master = self.tab("Personal Information"),)
        self.user_last_name.grid(row = 1,column=1, padx=20)

        self.user_pronouns = CTkComboBox(master = self.tab("Personal Information"), values=["He/Him", "She/Her", "They/Them"])
        self.user_pronouns.grid(row = 0, column = 2)

        CTkLabel(master = self.tab("Personal Information"), text = "Age").grid(row = 2, column =0)
        self.user_age = CTkEntry(master = self.tab("Personal Information"))
        self.user_age.grid(row = 3 , column = 0)

        CTkLabel(master = self.tab("Banking Information"), text ="Checking account balance").grid(row=0,column=0)
        self.balance = CTkEntry(master = self.tab("Banking Information"))
        self.balance.grid(row=1,column=0)

        CTkLabel(master = self.tab("Banking Information"), text ="Savings account balance").grid(padx=50,row=0,column=1)
        self.savings = CTkEntry(master = self.tab("Banking Information"))
        self.savings.grid(row=1,column=1)

        CTkLabel(master = self.tab("Banking Information"), text ="Monthly income").grid(row=0,column=2)
        self.income = CTkEntry(master = self.tab("Banking Information"))
        self.income.grid(row=1,column=2)

        CTkLabel(master=self.tab("Banking Information"), text="Expenses").grid(row=2,column = 0)
        self.expense_name = CTkEntry(master = self.tab("Banking Information"))
        self.expense_name.grid(row= 3, column = 0)

        CTkLabel(master=self.tab("Banking Information"), text="Price of Expense").grid(row=2,column = 1)
        self.expense_price = CTkEntry(master = self.tab("Banking Information"))
        self.expense_price.grid(row= 3, column = 1)
        
        CTkLabel(master=self.tab("Banking Information"), text="Subscriptions").grid(row=5,column = 0)
        self.sub_name = CTkEntry(master = self.tab("Banking Information"))
        self.sub_name.grid(row= 6, column = 0)

        CTkLabel(master=self.tab("Banking Information"), text="Price of Subscription").grid(row=5,column = 1)
        self.sub_price = CTkEntry(master = self.tab("Banking Information"))
        self.sub_price.grid(row= 6, column = 1)

        CTkButton(master=self.tab("Banking Information"), text="Add Expense", command=self.addExpense).grid(row=4,columnspan=2, pady=10)
        CTkButton(master=self.tab("Banking Information"), text="Add Subscription", command=self.addSubscription).grid(row=7,columnspan=2, pady=10)

        
        CTkLabel(master = self.tab("Sign Up"), text = "Username").grid(row = 0 , column=0)
        self.user_username = CTkEntry(master=self.tab("Sign Up"))
        self.user_username.grid(row = 1,column = 0)
        CTkLabel(master=self.tab("Sign Up"), text="Password").grid(row=2, column=0)
        self.user_password = CTkEntry(master=self.tab("Sign Up"), show="*")
        self.user_password.grid(row=3, column=0, padx=20, pady=10)
        
        CTkButton(master = self.tab("Sign Up"), text = "Submit", command = self.addDataToTable).grid(row = 4,column=0)

        

    def addExpense(self):
        expense_name = self.expense_name.get()
        expense_amount = float(self.expense_price.get())
        self.expense_name.delete(0, 'end')
        self.expense_price.delete(0,'end')
        self.expenses.append((expense_name, expense_amount))
        
    def addSubscription(self):
        sub_name = self.sub_name.get()
        sub_amount = float(self.sub_price.get())
        self.sub_name.delete(0, 'end')
        self.sub_price.delete(0,'end')
        self.sublist.append((sub_name, sub_amount))
        
        
       
   
            
        
    def addDataToTable(self):
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        try:
            cursor.execute(f"SELECT username FROM userInfo WHERE username='{self.user_username.get()}'")
            result = cursor.fetchone()
            if result is not None:
                tk.messagebox.showinfo("Error", "Username Taken")
            else:
                values = (self.user_username.get(), self.user_password.get(),self.user_first_name.get(), self.user_last_name.get(), self.user_pronouns.get(), int(self.user_age.get()), float(self.balance.get()), float(self.savings.get()), float(self.income.get()))
                cursor.execute("INSERT INTO userInfo VALUES (?,?,?, ?, ?, ?, ?, ?, ?)", values)

                # save the expenses to a table
                for expense in self.expenses:
                    name, price = expense
                    cursor.execute("INSERT INTO expenses (username, expense, expense_price) VALUES (?, ?, ?)", (self.user_username.get(), name, price))

                tk.messagebox.showinfo("Success", "Registration successful!")
            
        except ValueError:
            tk.messagebox.showinfo('Error', 'Make Sure All Fields Properly Filled')
        
        connection.commit()
        connection.close()

            
        
        
      
        
            
        
    
                
            
        


main()