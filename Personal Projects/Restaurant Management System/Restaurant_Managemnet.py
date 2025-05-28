# Restaurant Management App
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

# Greetings to the Customers
print("Welcome To \'World Of Food\'")
print(f"Select your Favorite Dish To Order: ")

# Printing The Menu
for item, price in menu.items():
    print(f"{item}: ₹{price}")
    print("- - - - - - - - - - - - - - - -")

# Ordering Process
order_total = 0

item_1 = input("What would you like to order for satisfying your Hunger?: ")
if item_1 in menu:
    print("Your Order Has Been Added To The Queue!\nEnjoy!")
    order_total += menu[item_1]
else:
    print(f"Order something which we can serve your from our Menu!\n{menu}")

item_2 = input("If you want to order something else, please enter the name: ")
if item_2 in menu:
    print("Your Order Has Been Added To The Queue!\nEnjoy!")
    order_total += menu[item_2]
else:
    print(f"Order something which we can serve your from our Menu!\n{menu}")

print(f"Your Order Total To Pay Is: {order_total}\nKindly Pay It!\nThanks")

# Payment Process
payment = float(input("Please Enter Your Payment Amount: "))
change = payment - order_total
print(f"Your Change Is: {change}")

# Thank You For Your Order, Drop A Review.
print("\nThank You For Visiting \'World Of Food!\'")
print("Do Drop A Review About The Food & Service of Our Restaurant")

# Continuing the Order Process until The User Exits/Quits.

while True:
    more_items = input("Do you want to order more items? (yes/no): ")
    if more_items.lower() == "yes":
        item_3 = input("What would you like to order for satisfying your Hunger?: ")
        if item_3 in menu:
            print("Your Order Has Been Added To The Queue!\nEnjoy!")
            order_total += menu[item_3]
        else:
            print(f"Order something which we can serve your from our Menu!\n{menu}")
    elif more_items.lower() == "no":
        break
    else:
        print("Please enter 'yes' or 'no'.")

print(f"Your Order Total To Pay Is: {order_total}\nKindly Pay It!\nThanks")
