import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

menu = {
    "Pizza": 50,
    "Burger": 60,
    "Fries": 30,
    "Peri Peri Fries": 45,
    "Cold Coffee": 60,
    "Hot Coffee": 50,
    "Salad": 60,
    "Hot Chocolate": 80,
    "Tea": 20,
    "Green Tea": 30,
    "Soup": 40,
    "Rice": 40,
    "Noodles": 50,
    "Pasta": 60,
    "Fried Momos (Veg)": 50,
    "Steam Momos (Veg)": 60,
    "Schezwan Noodles (Veg)": 100
}

order_total = 0

def add_to_order():
    global order_total
    item = menu_var.get()
    if item in menu:
        order_total += menu[item]
        order_list.insert(tk.END, f"{item} - ₹{menu[item]}")
        total_label.config(text=f"Total: ₹{order_total}")
    else:
        messagebox.showerror("Error", "Please select a valid item!")

def delete_order():
    global order_total
    selected = order_list.curselection()
    if selected:
        item_text = order_list.get(selected[0])
        item_name = item_text.split(" - ")[0]
        order_total -= menu[item_name]
        order_list.delete(selected[0])
        total_label.config(text=f"Total: ₹{order_total}")
    else:
        messagebox.showerror("Error", "Please select an item to delete.")

def make_payment():
    global order_total
    try:
        payment_amount = float(payment_entry.get())
        if payment_amount >= order_total:
            change = payment_amount - order_total
            messagebox.showinfo("Payment Successful", f"Payment Received! Change: ₹{change}")
            order_list.delete(0, tk.END)
            total_label.config(text="Total: ₹0")
            order_total = 0
        else:
            messagebox.showerror("Error", "Insufficient payment! Please pay the full amount.")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid payment amount.")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("World Of Food - Restaurant")
root.attributes('-fullscreen', True)

# Load and Blur Background Image
bg_image = Image.open("C:/Users/shoai/OneDrive/Desktop/Least Used Apps/Python Programs/External Projects/restaurant.jpg")
bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Title
title_label = tk.Label(root, text="Welcome To 'World Of Food'", font=("Arial", 16, "bold"), bg="white", fg="black")
title_label.pack(pady=10)

# Menu Selection
menu_var = tk.StringVar()
menu_var.set("Select an Item")
menu_dropdown = tk.OptionMenu(root, menu_var, *menu.keys())
menu_dropdown.pack(pady=10)

order_button = tk.Button(root, text="Add to Order", command=add_to_order, bg="green", fg="white")
order_button.pack()

delete_button = tk.Button(root, text="Delete Selected Item", command=delete_order, bg="orange", fg="white")
delete_button.pack()

# Order List
order_list = tk.Listbox(root, width=50, height=10)
order_list.pack(pady=10)

total_label = tk.Label(root, text="Total: ₹0", font=("Arial", 12, "bold"), bg="white", fg="black")
total_label.pack()

# Payment Section
payment_label = tk.Label(root, text="Enter Payment Amount:", font=("Arial", 12), bg="white")
payment_label.pack()
payment_entry = tk.Entry(root)
payment_entry.pack()

payment_button = tk.Button(root, text="Make Payment", command=make_payment, bg="blue", fg="white")
payment_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app, bg="red", fg="white")
exit_button.pack(pady=5)

root.mainloop()
