import random

class StockMarket:

    def __init__(self):

        self.prices = {"AAPL" : 150.0, "GOOGL": 2800.0, "TSLA": 700.0, "AMAZN": 3400.0}

        self.portfolio = {}

        self.money = 10000.0

    def simulate_market(self):

        for symbol in self.prices:

            change = random.uniform(-0.05, 0.05)

            self.prices[symbol] = round(self.prices[symbol] * (1 + change), 2)

    def display_stocks(self):

        print("\nAvailable Stocks & Prices:")

        for symbol, price in self.prices.items():

            print(f"  {symbol}: ${price}")

        print()

    def display_portfolio(self):

        print("\nYour Portfolio:")

        if self.portfolio:

            for symbol, shares in self.portfolio.items():

                print(f"  {symbol}: {shares} shares")

        else:

            print("  You do not own any shares yet.")

        print(f"Available cash: ${round(self.money, 2)}\n")

    def buy_stock(self, symbol, shares):

        if symbol not in self.prices:

            print("Stock not available.")

            return

        cost = self.prices[symbol] * shares

        if cost > self.money:

            print("Not enough cash to complete this purchase.")

        else:

            self.money -= cost

            self.portfolio[symbol] = self.portfolio.get(symbol, 0) + shares

            print(f"Bought {shares} shares of {symbol} for ${cost:.2f}")

    def sell_stock(self, symbol, shares):

        if symbol not in self.portfolio or self.portfolio[symbol] < shares:

            print("Not enough shares to sell.")

        else:

            revenue = self.prices[symbol] * shares

            self.money += revenue

            self.portfolio [symbol] -= shares

            if self.portfolio[symbol] == 0:

                del self.portfolio[symbol]

            print(f"Sold {shares} shares of {symbol} for ${revenue:.2f}")

    def main(self):

        while True:

            print("Stock Market App Command Menu:")

            print("  1. Display available stocks")

            print("  2. Display your Portfolio")

            print("  3. Buy Stock")

            print("  4. Sell Stock")

            print("  5. Simulate Market Day")

            print("  6. Quit")

            choice = input("Enter your choice (1-6): ")

            if choice == "1":

                self.display_stocks()

            elif choice == "2":

                self.display_portfolio()

            elif choice == "3":

                symbol = input("Enter stock symbol to buy: ").upper()

                try:
                    shares = int(input("Enter number of shares to buy: "))

                    if shares <= 0:

                        print("Number of shares must be positive.")

                        continue

                except ValueError:

                    print("Invalid number of shares. Please enter an integer.")

                    continue

                self.buy_stock(symbol, shares)

            elif choice == "4":

                symbol = input("Enter stock symbol to sell: ").upper()

                try:

                    shares = int(input("Enter number of shares to sell: "))

                    if shares <= 0:

                        print("Number of shares must be positive.")

                        continue

                except ValueError:

                    print("Invalid number of shares. Please enter an integer.")

                    continue

                self.sell_stock(symbol, shares)

            elif choice == "5":

                self.simulate_market()

                print("Market day simulated. Stock prices have been updated.")

            elif choice == "6":

                print("Exiting the app. Goodbye!")

                break

            else:

                print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":

    app = StockMarket()
    app.main()
