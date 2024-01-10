import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create SQLite database and table
conn = sqlite3.connect('order_manage.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        choice TEXT
    )
''')
conn.commit()

class OrderManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Management System")
        self.root.geometry("400x400")

        self.create_widgets()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(self.root, text="Phone:").grid(row=1, column=0, sticky="e")
        tk.Label(self.root, text="Email:").grid(row=2, column=0, sticky="e")
        tk.Label(self.root, text="Address:").grid(row=3, column=0, sticky="e")
        tk.Label(self.root, text="Choice:").grid(row=4, column=0, sticky="e")

        # Entry widgets
        self.name_entry = tk.Entry(self.root)
        self.phone_entry = tk.Entry(self.root)
        self.email_entry = tk.Entry(self.root)
        self.address_entry = tk.Entry(self.root)
        self.choice_entry = tk.Entry(self.root)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1)
        self.address_entry.grid(row=3, column=1)
        self.choice_entry.grid(row=4, column=1)

        # Buttons
        tk.Button(self.root, text="Place Order", command=self.place_order).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Admin Login", command=self.admin_login).grid(row=6, column=0, columnspan=2)

    def place_order(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        choice = self.choice_entry.get()

        # Input validations
        if not all([name, phone, email, address, choice]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # Validate phone number using a simple example
        if not phone.isdigit():
            messagebox.showerror("Error", "Phone number must contain only digits.")
            return

        # Validate email using a simple example
        if not "@" in email or not "." in email:
            messagebox.showerror("Error", "Invalid email address.")
            return

        # Insert order into the database
        cursor.execute("INSERT INTO orders (name, phone, email, address, choice) VALUES (?, ?, ?, ?, ?)",
        (name, phone, email, address, choice))
        conn.commit()

        messagebox.showinfo("Success", "Order placed successfully.")

        # Clear the input fields after placing the order
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.choice_entry.delete(0, tk.END)

    def admin_login(self):
        admin_password = "admin123"  # You can replace this with a more secure authentication mechanism
        entered_password = simple_dialog("Admin Login", "Enter Admin Password:")

        if entered_password == admin_password:
            self.open_admin_panel()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def open_admin_panel(self):
        admin_panel = tk.Toplevel(self.root)
        admin_panel.title("Admin Panel")

        # Display orders
        orders = cursor.execute("SELECT * FROM orders").fetchall()
        for order in orders:
            tk.Label(admin_panel, text=f"Order ID: {order[0]}, Name: {order[1]}, Phone: {order[2]}, "
            f"Email: {order[3]}, Address: {order[4]}, Choice: {order[5]}").pack()

        # Delete order button
        delete_button = tk.Button(admin_panel, text="Delete Order", command=self.delete_order)
        delete_button.pack()

    def delete_order(self):
        order_id = simple_dialog("Delete Order", "Enter Order ID to delete:")
        if not order_id.isdigit():
            messagebox.showerror("Error", "Invalid Order ID.")
            return

        order_id = int(order_id)
        confirm = messagebox.askyesno("Confirmation", f"Do you really want to delete Order ID {order_id}?")
        if confirm:
            cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Order ID {order_id} deleted successfully.")

def simple_dialog(title, prompt):
    top = tk.Toplevel()
    top.title(title)
    tk.Label(top, text=prompt).pack()
    entry = tk.Entry(top)
    entry.pack()
    entry.focus_set()

    def on_ok():
        top.destroy()

    ok_button = tk.Button(top, text="OK", command=on_ok)
    ok_button.pack()

    top.wait_window()

    return entry.get()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.mainloop()

# Close the database connection when the app is closed
conn.close()
