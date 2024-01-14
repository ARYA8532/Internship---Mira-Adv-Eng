from tkinter import *
from tkinter import messagebox
from tkinter import ttk

f = ("Century", 20, "bold")

def calculate_rectangle_area():
    try:
        length = float(length_entry.get())
        breadth = float(breadth_entry.get())
        if length <= 0 or breadth <= 0:
            messagebox.showerror("Error", "Invalid input value. Please enter a positive number.")
        else:
            area = length * breadth
            result_label.config(text=f"Area: {area:.2f}")

    except ValueError:
        messagebox.showerror("Error", "Enter a numeric value")

def calculate_triangle_area():
    try:
        base = float(base_entry.get())
        height = float(height_entry.get())
        if base <= 0 or height <= 0:
            messagebox.showerror("Error", "Invalid input value. Please enter a positive number.")
        else:
            area = 0.5 * base * height
            result_label.config(text=f"Area: {area:.2f}")
            
    except ValueError:
        messagebox.showerror("Error", "Enter a numeric value")

def calculate_square_area():
    try:
        side = float(side_entry.get())
        if side <= 0:
            messagebox.showerror("Error", "Invalid input value. Please enter a positive number.")
        else:
            area = side ** 2
            result_label.config(text=f"Area: {area:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Enter a numeric value")

def calculate_circle_area():
    try:
        radius = float(radius_entry.get())
        if radius <= 0:
            messagebox.showerror("Error", "Invalid input value. Please enter a positive number.")
        else:
            area = 3.14 * radius ** 2
            result_label.config(text=f"Area: {area:.2f}")

    except ValueError:
        messagebox.showerror("Error", "Enter a numeric value")

def update_shape(*args):
    selected_shape = shape_var.get()
    result_label.config(text="Area")

    length_label.grid_remove()
    length_entry.grid_remove()
    breadth_label.grid_remove()
    breadth_entry.grid_remove()
    base_label.grid_remove()
    base_entry.grid_remove()
    height_label.grid_remove()
    height_entry.grid_remove()
    side_label.grid_remove()
    side_entry.grid_remove()
    radius_label.grid_remove()
    radius_entry.grid_remove()

    calculate_button.grid_remove()

    
    if selected_shape == "Rectangle":
        length_label.grid(row=4, column=3)
        length_entry.grid(row=4, column=4, padx=10, pady=10)
        breadth_label.grid(row=5, column=3)
        breadth_entry.grid(row=5, column=4, padx=10, pady=10)
        calculate_button.config(command=calculate_rectangle_area)

    elif selected_shape == "Triangle":
        base_label.grid(row=4, column=3)
        base_entry.grid(row=4, column=4, padx=10, pady=10)
        height_label.grid(row=5, column=3)
        height_entry.grid(row=5, column=4, padx=10, pady=10)
        calculate_button.config(command=calculate_triangle_area)

    elif selected_shape == "Square":
        side_label.grid(row=4, column=3)
        side_entry.grid(row=4, column=4, padx=10, pady=10)
        calculate_button.config(command=calculate_square_area)

    elif selected_shape == "Circle":
        radius_label.grid(row=4, column=3)
        radius_entry.grid(row=4, column=4, padx=10, pady=10)
        calculate_button.config(command=calculate_circle_area)

    calculate_button.grid(row=6, column=3, columnspan=2, pady=10)


root = Tk()
root.title("Area Calculator")

shape_var = StringVar(value="Rectangle")
shape_label = Label(root, text="Select Shape:", font=f)
shape_label.grid(row=0, column=4)

shape_combobox = ttk.Combobox(root, textvariable=shape_var, values=("Rectangle", "Triangle", "Square", "Circle"), font=f)
shape_combobox.grid(row=0, column=6, padx=10, pady=10)
shape_combobox.bind("<<ComboboxSelected>>", update_shape)

length_label = Label(root, text="Length:", font=f)
length_entry = Entry(root, font=f)

breadth_label = Label(root, text="Breadth:", font=f)
breadth_entry = Entry(root, font=f)

base_label = Label(root, text="Base:", font=f)
base_entry = Entry(root, font=f)

height_label = Label(root, text="Height:", font=f)
height_entry = Entry(root, font=f)

side_label = Label(root, text="Side:", font=f)
side_entry = Entry(root, font=f)

radius_label = Label(root, text="Radius:", font=f)
radius_entry = Entry(root, font=f)

result_label = Label(root, text="Area:", font=f)
result_label.grid(row=6, column=5, columnspan=2)


calculate_button = Button(root, text="Calculate", font=f, command=calculate_rectangle_area)
update_shape()
root.iconbitmap("area.ico")
root.geometry("1000x600+50+50")
root.mainloop()
