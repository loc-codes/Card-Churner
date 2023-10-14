# Card Churner

## Overview

The Card Churner project is designed to assist those interested in the practice of card churning, a technique where individuals sign up for credit cards to avail of promotional offers and rewards, and then potentially close them after reaping the benefits. This project automates the process by scraping the `rwrds.com.au` website for Qantas and gift card reward offers, computing important metrics, and highlighting the most lucrative offers. The result is an easily digestible HTML file with top offers.

## Context on Card Churning

Card churning can be seen as a side hustle that requires minimal time investment, especially if one's existing rent or bills are routed through services like Sniip, Yakpay, or Rental Rewards. By strategically using these services in conjunction with card churning, one can maximize rewards without incurring additional expenses.

## Potential Risks

Before reading further, it's extremely important to understand the risks associated with card churning:

- **Overspending:** The allure of meeting minimum spending requirements for bonuses might lead to unnecessary expenditures, potentially resulting in a negative ROI or loss.
- **Missed Payments:** Failing to pay off the card balance on time can result in substantial fees and interest rates. These costs rapidly overshadow any gains from rewards.
- **Credit Score Impact:** Engaging in card churning can lead to multiple credit inquiries, which might adversely affect one's credit score. This can hinder other parts of your financial life, including mortgage refinancing opportunities.
- **Time Investment vs. Upside Limit:** The potential profits from card churning have a ceiling. It's essential to evaluate if the time spent learning and practicing card churning offers a worthwhile return.
- **Changing Terms and Conditions:** Credit card issuers may adjust their terms, benefits, or eligibility criteria without notice, which can affect the profitability of churning strategies.

## Caution

Before evaluating information from this product, please:
- Thoroughly research and understand the risks of credit cards, how churning works and compound interest. [You can start here](https://www.youtube.com/watch?v=MFkBoXhl5SU)
- Recognize that while there are potential gains, there are also caps to these upsides.
- Always remember that information and recommendations provided by this project do not constitute personal financial advice.

## Features

- **Scraping:** Extracts reward card data from rwrds.com.au.
- **Processing:** Computes key metrics for each card offer.
- **Filtering:** Excludes offers that were taken up in the last 12 months.
- **Visualization:** Outputs a styled HTML file with the top offers.

## How it Works

1. **Data Collection:**
   - `fetch_data_from_csv()`: Reads a CSV file which maintains a history of offers taken up.
   - `fetch_data_from_url()`: Fetches webpage content from a given URL.
2. **Data Extraction:**
   - `extract_data_from_html()`: Processes the HTML content to extract relevant offer details using regex patterns.
3. **Data Transformation:**
   - `process_offers()`: Computes various metrics such as 'Monthly Spend', 'Net Monthly Profit', and 'Monthly ROI'.
   - `filter_offers()`: Filters out offers that were taken up in the last 12 months and sorts by monthly ROI.
   - `format_data_for_display()`: Prepares the offers for display, adjusting formats for better readability.
4. **Visualization:**
   - `save_and_open_html_combined()`: Creates a combined HTML file for both Qantas and cash offers, applying custom styling and presenting top offers.
5. **Main Processing:** The script fetches previous churn history, scrapes current offers, processes, and formats the data, and finally generates an HTML file showcasing the top offers. The table will strike out rows with monthly spends over $1000, as spends over this would change my financial behaviour. You can adjust this to your needs.

## Prerequisites

- Python 3
  - **Required Libraries:**
    - BeautifulSoup4
    - requests
    - pandas
    - re
    - datetime

## Usage

1. Update `churn_history.csv` with your card churn history.
2. Run the script:
   ```bash
   python card_churner.py
3. Open `current_offers.html` in your browser to view the top offers.

> **Note**
> - Ensure `churn_history.csv` is updated with relevant data before running the script.
> - Make sure all the required libraries are installed.

**Contributions**
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

Happy Churning! 🎉
