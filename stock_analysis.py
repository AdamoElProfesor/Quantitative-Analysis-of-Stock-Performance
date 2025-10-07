import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np


# Choose stocks to compare
stock_names = ["AAPL", "GOOG", "AMZN"]

# Download stocks
data = yf.download(stock_names, start="2024-09-01", end="2025-09-01",interval="1wk")

# Store every stock separartely
stock_data = []
for stock_name in stock_names:
    stock_data.append(data.xs(stock_name, axis=1, level=1))

# Extract the dates for the y axis
x_values = stock_data[0].index

# Extract the close value of every stock
y_values = []
for stock in stock_data:
    y_values.append(stock['Close'].values)

# Generate an individual graph for every stock
plt.figure(figsize=(9,6))
for i, y_value in enumerate(y_values):
    plt.plot(x_values, y_value)
    plt.grid(True)
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title(stock_names[i])
    plt.savefig("./graphs/stock_prices_" + stock_names[i] + ".png")
    plt.close()


# Generate a graph containing all stocks

# Normalize the price
y_values = []
for stock in stock_data:
    y_values.append(stock['Close'] / stock['Close'].iloc[0] * 100)

plt.figure(figsize=(9,6))
for i, y_value in enumerate(y_values):
    plt.plot(x_values, y_value, label=stock_names[i])

plt.xlabel("Date")
plt.ylabel("Closing Price (USD)")
plt.title("Stocks")
plt.legend() 
plt.grid(True)
plt.savefig("./graphs/stock_prices.png")
plt.close()


# Work on volatility

# Find volatily values

stock_return = []
stock_data_clean = []
for stock in stock_data:
    stock['Return'] = stock['Close'].pct_change()
    stock_data_clean.append(stock.dropna())

    # Compute the standard deviation

    stock['Volatility'] = stock['Return'].rolling(4).std()
    stock['Volatility'] = stock['Volatility'] * np.sqrt(13)


# Plot volatility graph

x_values = stock_data[0].index
y_values = []

for stock in stock_data:
    y_values.append(stock['Volatility'].values)

plt.figure(figsize=(9,6))
for i, y_value in enumerate(y_values):
    plt.plot(x_values, y_value, label=stock_names[i])

plt.title("Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.gcf().autofmt_xdate()
plt.grid(True)
plt.legend() 
plt.savefig("./graphs/volatility.png")
plt.close()



# Volume plot
plt.figure(figsize=(9,6))
for i, stock in enumerate(stock_data):
    plt.plot(x_values, stock['Volume'] / 1e6, label=stock_names[i])

plt.title("Volume")
plt.xlabel("Date")
plt.ylabel("Volume (Millions of shares per week)")  
plt.legend()
plt.savefig("./graphs/volume.png")
plt.grid(True)
plt.close()