import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk, ImageFilter
import random
import os

class StockMarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Simulator")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')

        # Initialize stock data
        self.prices = {"AAPL": 150.0, "GOOGL": 2800.0, "TSLA": 700.0, "AMZN": 3400.0}
        self.portfolio = {}
        self.money = 1000000.0
        self.transaction_history = []
        self.total_profit = 0.0  # Track total profit from sales
        self.purchase_prices = {}  # Track purchase prices for each stock

        # Load and blur background image
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "stocks.jpg")
            self.bg_image = Image.open(image_path)

            # Resize to screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.bg_image = self.bg_image.resize((screen_width, screen_height), Image.LANCZOS)

            # Apply blur effect
            self.bg_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=10))

            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_label = tk.Label(self.root, bg="black")
            self.bg_label.place(relwidth=1, relheight=1)

        # Create UI components
        self.create_ui()

    def create_ui(self):
        # Main container with semi-transparent background
        main_frame = tk.Frame(self.root, bg="gray20", bd=5)  # Changed from #00000080 to gray20
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Stock prices display
        self.stock_display = tk.Label(main_frame,
                                    text=self.get_stock_text(),
                                    font=("Arial", 12),
                                    bg="gray20",  # Changed from #00000080
                                    fg="white",
                                    justify="left")
        self.stock_display.pack(pady=10)

        # Portfolio display
        self.portfolio_display = tk.Label(main_frame,
                                        text=self.get_portfolio_text(),
                                        font=("Arial", 12),
                                        bg="gray20",  # Changed from #00000080
                                        fg="white",
                                        justify="left")
        self.portfolio_display.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(main_frame, bg="gray20")  # Changed from #00000080
        input_frame.pack(pady=10)

        # Symbol input
        tk.Label(input_frame, text="Stock Symbol:", bg="gray20", fg="white").grid(row=0, column=0, padx=5)
        self.symbol_entry = ttk.Entry(input_frame, font=("Arial", 12), width=10)
        self.symbol_entry.grid(row=0, column=1, padx=5)

        # Shares input
        tk.Label(input_frame, text="Shares:", bg="gray20", fg="white").grid(row=1, column=0, padx=5)
        self.shares_entry = ttk.Entry(input_frame, font=("Arial", 12), width=10)
        self.shares_entry.grid(row=1, column=1, padx=5)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="gray20")  # Changed from #00000080
        button_frame.pack(pady=10)

        # Buttons
        ttk.Button(button_frame, text="Buy Stock", command=self.buy_stock, style="Green.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sell Stock", command=self.sell_stock, style="Red.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Simulate Market", command=self.simulate_market).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View History", command=self.view_transaction_history).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset Portfolio", command=self.reset_portfolio).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)

        # Configure styles - FIXED: Changed foreground to black for better visibility
        style = ttk.Style()
        style.configure("Green.TButton", background="green", foreground="black", font=("Arial", 12, "bold"))
        style.configure("Red.TButton", background="red", foreground="black", font=("Arial", 12, "bold"))
        style.map("Green.TButton",
                background=[('active', 'dark green')],
                foreground=[('active', 'black')])
        style.map("Red.TButton",
                background=[('active', 'dark red')],
                foreground=[('active', 'black')])

    def get_stock_text(self):
        return "Available Stocks:\n" + "\n".join([f"  {s}: ${p:.2f}" for s, p in self.prices.items()])

    def get_portfolio_text(self):
        portfolio_text = "Your Portfolio:\n"
        if self.portfolio:
            portfolio_text += "\n".join([f"  {s}: {sh} shares" for s, sh in self.portfolio.items()])
        else:
            portfolio_text += "  No stocks owned"
        return portfolio_text + f"\n  Available Cash: ${self.money:.2f}\n  Total Profit: ${self.total_profit:.2f}"

    def update_display(self):
        self.stock_display.config(text=self.get_stock_text())
        self.portfolio_display.config(text=self.get_portfolio_text())

    def buy_stock(self):
        symbol = self.symbol_entry.get().strip().upper()
        try:
            shares = int(self.shares_entry.get())
            if shares <= 0:
                raise ValueError("Shares must be positive")

            if symbol not in self.prices:
                messagebox.showerror("Error", f"Stock {symbol} not available")
                return

            cost = self.prices[symbol] * shares
            if cost > self.money:
                messagebox.showerror("Error", "Insufficient funds")
                return

            self.money -= cost
            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + shares
            # Store the purchase price for the shares
            if symbol not in self.purchase_prices:
                self.purchase_prices[symbol] = []
            self.purchase_prices[symbol].extend([self.prices[symbol]] * shares)
            self.transaction_history.append(f"Bought {shares} shares of {symbol} at ${self.prices[symbol]:.2f} each")
            messagebox.showinfo("Success", f"Purchased {shares} shares of {symbol}")
            self.update_display()

        except ValueError as f:
            messagebox.showerror("Error", str(f) if str(f) else "Invalid input")

    def sell_stock(self):
        symbol = self.symbol_entry.get().strip().upper()
        try:
            shares = int(self.shares_entry.get())
            if shares <= 0:
                raise ValueError("Shares must be positive")

            if symbol not in self.portfolio or self.portfolio[symbol] < shares:
                messagebox.showerror("Error", "Insufficient shares to sell")
                return

            # Calculate average purchase price for the shares being sold
            purchase_prices = self.purchase_prices[symbol][:shares]
            avg_purchase_price = sum(purchase_prices) / shares
            del self.purchase_prices[symbol][:shares]

            revenue = self.prices[symbol] * shares
            profit = revenue - (avg_purchase_price * shares)
            self.total_profit += profit
            self.money += revenue
            self.portfolio[symbol] -= shares
            if self.portfolio[symbol] == 0:
                del self.portfolio[symbol]
                del self.purchase_prices[symbol]
            self.transaction_history.append(f"Sold {shares} shares of {symbol} at ${self.prices[symbol]:.2f} each (Profit: ${profit:.2f})")
            messagebox.showinfo("Success", f"Sold {shares} shares of {symbol}\nProfit: ${profit:.2f}\nTotal Profit: ${self.total_profit:.2f}")
            self.update_display()

        except ValueError as f:
            messagebox.showerror("Error", str(f) if str(f) else "Invalid input")

    def simulate_market(self):
        for symbol in self.prices:
            change = random.uniform(-0.05, 0.05)
            self.prices[symbol] = round(self.prices[symbol] * (1 + change), 2)
        messagebox.showinfo("Market Update", "Stock prices have been updated")
        self.update_display()

    def view_transaction_history(self):
        if not self.transaction_history:
            messagebox.showinfo("Transaction History", "No transactions yet")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("400x300")

        scrollbar = ttk.Scrollbar(history_window)
        scrollbar.pack(side="right", fill="y")

        history_text = tk.Text(history_window, wrap="word", yscrollcommand=scrollbar.set)
        history_text.insert("end", "\n".join(self.transaction_history))
        history_text.config(state="disabled")
        history_text.pack(expand=True, fill="both")

        scrollbar.config(command=history_text.yview)

    def reset_portfolio(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset your portfolio?")
        if confirm:
            self.portfolio.clear()
            self.money = 10000.0
            self.transaction_history.clear()
            self.update_display()
            messagebox.showinfo("Success", "Portfolio has been reset")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockMarketApp(root)
    root.mainloop()
