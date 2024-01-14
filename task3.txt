from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
import sqlite3

f = ("Century", 20, "bold")

conn = sqlite3.connect('order_management.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS orders
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,choices TEXT)''')
conn.commit()

class CustomDialog:
    def __init__(self, parent, title, prompt, font):
        self.result = None

        self.top = Toplevel(parent)
        self.top.title(title)

        Label(self.top, text=prompt, font=f).pack()
        self.entry_var = StringVar()
        Entry(self.top, textvariable=self.entry_var, font=f).pack()

        Button(self.top, text="OK", command=self.on_ok, font=f).pack()

        self.top.wait_window()

    def on_ok(self):
        self.result = self.entry_var.get()
        self.top.destroy()

class OrderManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Management System")

        self.label_name = Label(root, text="Name:", font=f)
        self.entry_name = Entry(root, font=f)

        self.label_phone = Label(root, text="Phone:", font=f)
        self.entry_phone = Entry(root, font=f)

        self.label_email = Label(root, text="Email:", font=f)
        self.entry_email = Entry(root, font=f)

        self.label_address = Label(root, text="Address:", font=f)
        self.entry_address = Entry(root, font=f)

        self.label_choices = Label(root, text="Menu Choices:", font=f)
        self.choices_var = StringVar()
        self.choices_var.set("Tea")
        menu_choices = ["Tea", "Coffee", "Juice", "Milkshake", "Soda"]
        self.choices_combobox = ttk.Combobox(root, textvariable=self.choices_var, values=menu_choices, font=f)

        self.choices_combobox["style"] = "TCombobox"

        self.submit_button = Button(root, text="Submit Order", command=self.submit_order, font=f)
        self.quit_button = Button(root, text="Quit", command=self.on_close, font=f)
        admin_login_button = Button(root, text="Admin Login", command=self.admin_login, font=f)

        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky=E)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_phone.grid(row=1, column=0, padx=10, pady=5, sticky=E)
        self.entry_phone.grid(row=1, column=1, padx=10, pady=5)

        self.label_email.grid(row=2, column=0, padx=10, pady=5, sticky=E)
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        self.label_address.grid(row=3, column=0, padx=10, pady=5, sticky=E)
        self.entry_address.grid(row=3, column=1, padx=10, pady=5)

        self.label_choices.grid(row=4, column=0, padx=10, pady=5, sticky=E)
        self.choices_combobox.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        self.submit_button.grid(row=5, column=1, pady=10)
        self.quit_button.grid(row=6, column=2, pady=10)
        admin_login_button.grid(row=6, column=0, columnspan=2)

    def submit_order(self):
        if not self.validate_inputs():
            return
        order_data = (self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_address.get(),self.choices_var.get())
        c.execute('INSERT INTO orders (name, phone, email, address, choices) VALUES (?, ?, ?, ?, ?)', order_data)
        conn.commit()

        messagebox.showinfo("Order Submitted", "Order has been submitted successfully.")
    def validate_inputs(self):
        name = self.entry_name.get()
        if not name or not name.isalpha():
            messagebox.showerror("Error", "Invalid name.")
            return False

        phone = self.entry_phone.get()
        if not phone or not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Error", "Invalid phone number.")
            return False

        email = self.entry_email.get()
        if not email or '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Invalid email.")
            return False

        address = self.entry_address.get()
        if not address:
            messagebox.showerror("Error", "Invalid address.")
            return False

        return True

    def admin_login(self):
        admin_password = "admin123"
        custom_dialog = CustomDialog(self.root, "Admin Login", "Enter Admin Password:", font=f)
        entered_password = custom_dialog.result

        if entered_password == admin_password:
            self.open_admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect password.")
    def open_admin_panel(self):
        admin_panel = Toplevel(self.root)
        admin_panel.title("Admin Panel")

        title_label = Label(admin_panel, text="Order Details", font=("Century", 24, "bold"))
        title_label.pack(pady=10)

        orders = c.execute("SELECT * FROM orders").fetchall()
        for order in orders:
            order_info = f"Order ID: {order[0]}, Name: {order[1]}, Phone: {order[2]}, "f"Email: {order[3]}, Address: {order[4]}, Choice: {order[5]}"
            order_label = Label(admin_panel, text=order_info, font=("Arial", 14))
            order_label.pack()

        delete_button = Button(admin_panel, text="Delete Order", command=self.delete_order, font=("Century", 14, "bold"))
        delete_button.pack(pady=20)

    def show_delete_confirmation(self):
        confirmation_dialog = CustomDialog(self.root, "Delete Order", "Do you really want to delete this order?")
        confirmation_dialog.transient(self.root) 
        confirmation_dialog.grab_set() 
        self.root.wait_window(confirmation_dialog)  
        
        if confirmation_dialog.result:
            self.delete_order()
    def delete_order(self):
        order_id = simpledialog.askstring("Delete Order", "Enter Order ID to delete:")
        if order_id and order_id.isdigit():
            order_id = int(order_id)
            confirm = messagebox.askyesno("Confirmation", f"Do you really want to delete Order ID {order_id}?")
            if confirm:
                c.execute("DELETE FROM orders WHERE id=?", (order_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Order ID {order_id} deleted successfully.")
        else:
            messagebox.showerror("Error", "Invalid Order ID.")
    def on_close(self):
        conn.close()
        root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = OrderManagementApp(root)
    root.geometry("1000x600+50+50")
    root.mainloop()
