import ccxt
import pandas as pd
import numpy as np
import talib
import time

# Binance API credentials
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Initialize Binance API
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

# Symbol for Ethereum
symbol = 'ETH/USDT'

# Bollinger Bands parameters
window = 20
std_dev = 2

# CSV file to save data
csv_filename = 'bollinger_bands_eth.csv'

def calculate_bollinger_bands(data):
    close_prices = data['close'].astype(float)
    upper_band, middle_band, lower_band = talib.BBANDS(close_prices, timeperiod=window, nbdevup=std_dev, nbdevdn=std_dev)
    return upper_band, middle_band, lower_band

def main():
    print("Calculating Bollinger Bands for Ethereum...")
    
    while True:
        try:
            # Fetch historical data
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=window)

            # Create a DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Calculate Bollinger Bands
            upper_band, middle_band, lower_band = calculate_bollinger_bands(df)

            # Display values on screen
            print("Upper Band:", upper_band.iloc[-1])
            print("Middle Band:", middle_band.iloc[-1])
            print("Lower Band:", lower_band.iloc[-1])
            print("")

            # Save values to CSV file
            df['upper_band'] = upper_band
            df['middle_band'] = middle_band
            df['lower_band'] = lower_band
            df.to_csv(csv_filename, index=False)

            # Wait for the next data point
            time.sleep(60)  # You may adjust this interval based on your preferences

        except Exception as e:
            print("Error:", e)
            time.sleep(60)  # Wait for a minute before trying again

if __name__ == "__main__":
    main()
