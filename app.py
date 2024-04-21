from flask import Flask, render_template, request

import requests
import os

app = Flask(__name__)

# Function to fetch token prices from the provided API response
def get_token_prices(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for any HTTP error

        # Parse the JSON response
        data = response.json()

        print("API Response:", data)  # Print the entire API response for debugging

        # Check if the API response contains the expected data structure
        if 'pairs' not in data or len(data['pairs']) == 0:
            raise ValueError("Unexpected API response format")

        # Extract token prices
        token_price_usd = float(data['pairs'][0]['priceUsd'])
        

        return token_price_usd,

    except Exception as e:
        print(f"Error fetching token prices: {e}")
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token1 = request.form['token1']
        token2 = request.form['token2']

        # API URLs for DRB and DRD tokens
        drb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd2d6690ca1575777e385ccfb59f2d346fe16aedc"
        drd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0xaba1ea940ba57aaeb8a2fd2891ad7cd0ea6cc3ec"
        dbrd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x98dc0d054d89ca6dfa591f9d5a46646181acf564"
        dbrb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xc1bf9be5070c2124070824b59f483835e971eb66"
        dbotd_api_url = "https://api.dexscreener.com/latest/dex/pairs/degenchain/0x8a30d9d40b7fff6d601ce40bcde489d9467361d8"
        dbotb_api_url = "https://api.dexscreener.com/latest/dex/pairs/base/0xd7baabd9310b8b5457f18847c512e25d4492b406"
    
        # Fetch token prices
        drb_price_usd,  = get_token_prices(drb_api_url)
        drd_price_usd,  = get_token_prices(drd_api_url)
        dbrd_price_usd, = get_token_prices(dbrd_api_url)  # Unpack the tuple properly
        dbrb_price_usd, = get_token_prices(dbrb_api_url)
        dbotd_price_usd, = get_token_prices(dbotd_api_url)  # Unpack the tuple properly
        dbotb_price_usd, = get_token_prices(dbotb_api_url)
       

        # Calculate price difference
        if drb_price_usd is not None and drd_price_usd is not None:
            price_difference_dr = (100 * (drd_price_usd - drb_price_usd) / drb_price_usd)
            result = f"Price difference (DR): % {price_difference_dr:.2f},"

        if dbrd_price_usd is not None and dbrb_price_usd is not None:
            price_difference_dbr = (100 * (dbrd_price_usd - dbrb_price_usd) / dbrb_price_usd)
            result += f" Price difference (DBR): % {price_difference_dbr:.2f},"  # Append to the result
        if dbotd_price_usd is not None and dbotb_price_usd is not None:
            price_difference_dbr = (100 * (dbotd_price_usd - dbotb_price_usd) / dbotb_price_usd)
            result += f" Price difference (DBOT): % {price_difference_dbr:.2f},"
        else:
            result = "Error calculating price difference"

        return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
   
