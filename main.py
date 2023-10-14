from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_data_from_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)

def fetch_data_from_url(url: str) -> str:
    response = requests.get(url)
    return response.text

def is_within_last_12_months(date_str: str) -> bool:
    try:
        close_date = datetime.strptime(date_str, '%d/%m/%y')
        delta = datetime.now() - close_date
        return delta < timedelta(days=365)
    except ValueError:
        return True

def extract_data_from_html(html: str, patterns: dict) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    objects = soup.find_all('div', class_='flex flex-col sm:flex-row gap-4')
    offers = []
    for obj in objects:
        obj_text = obj.get_text()
        offer = {}
        for keyword, pattern in patterns.items():
            match = re.search(pattern, obj_text)
            if match:
                if keyword == 'Card Name':
                    offer[keyword] = match.group(2)
                else:
                    offer[keyword] = int(match.group(1).replace(',', ''))
        offers.append(offer)
    return offers

def process_offers(offers: list, offer_type: str) -> list:
    for offer in offers:
        if offer.get('Spend') and offer.get('Days'):
            days_needed = offer['Spend'] / 1000 * 30
            actual_days = min(days_needed, offer['Days'])
            offer['Time To Reach Bonus'] = f'{round(actual_days)} days'
            offer['Monthly Spend'] = round(offer['Spend'] / actual_days * 30)
            del offer['Spend']

            if offer_type == "qantas" and offer.get('Fee') and offer.get('Points'):
                offer['Net Revenue'] = round(0.015 * offer['Points'] - 0.015 * offer['Monthly Spend'])
                offer['Net Total Profit'] = round(offer['Net Revenue'] - offer['Fee'])
                offer['Net Monthly Profit'] = round(offer['Net Total Profit'] / actual_days * 30)
            elif offer_type == "cash" and offer.get('Profit'):
                offer['Net Revenue'] = 'N/A'
                offer['Monthly Profit'] = round(offer['Profit'] / actual_days * 30)
                offer['Net Monthly Profit'] = round(offer['Monthly Profit'] - 0.015 * offer['Monthly Spend'])
                offer['Net Total Profit'] = offer['Net Monthly Profit'] * actual_days / 30

            if 'Net Monthly Profit' in offer and 'Monthly Spend' in offer:
                offer['Monthly ROI'] = round(offer['Net Monthly Profit'] / offer['Monthly Spend'] * 100, 2)
        offers = [offer for offer in offers if offer.get('Monthly Spend', 0) <= 2000]

    return filter_offers(offers)

def filter_offers(offers: list) -> list:
    filtered_offers = []
    for offer in offers:
        card_name = offer.get('Card Name', '').lower()
        is_valid = True
        for _, row in csv_data.iterrows():
            bank = row['Bank'].lower()
            card_type = row['Type'].lower()
            close_date = row['Close Date']
            if bank in card_name and card_type in card_name and is_within_last_12_months(close_date):
                is_valid = False
                break
        if is_valid:
            filtered_offers.append(offer)
    return sorted(filtered_offers, key=lambda x: x.get('Monthly ROI', 0), reverse=True)

def format_data_for_display(offers: list) -> list:
    for offer in offers:
        offer['Card Name'] = re.sub(r"\(.*\)", "", offer['Card Name']).strip()
        if 'Monthly ROI' in offer:
            offer['Monthly ROI'] = f"{offer['Monthly ROI']}%"
        for key in ['Net Revenue','Fee', 'Monthly Spend', 'Net Monthly Profit', 'Net Total Profit']:
            if key in offer:
                offer[key] = f"${offer[key]}"
    return offers

def save_and_open_html_combined(offers1: list, title1: str, offers2: list, title2: str, filename: str):
    df1 = pd.DataFrame(offers1)[['Card Name', 'Monthly ROI', 'Time To Reach Bonus', 'Fee', 'Monthly Spend', 'Net Monthly Profit', 'Net Total Profit']]
    df1.dropna(inplace=True)
    
    df2 = pd.DataFrame(offers2)[['Card Name', 'Monthly ROI', 'Time To Reach Bonus', 'Fee', 'Monthly Spend', 'Net Monthly Profit', 'Net Total Profit']]
    df2.dropna(inplace=True)

    df1.index += 1
    df2.index += 1


    # Function to apply custom styling
    def highlight_rows(row):
        try:
            if float(row['Monthly Spend'].replace("$", "")) > 1000:
                return ['color: red; text-decoration: line-through'] * len(row)
            else:
                return [''] * len(row)
        except:
            return [''] * len(row)

    
    styled_df1 = df1.style.apply(highlight_rows, axis=1)
    styled_df2 = df2.style.apply(highlight_rows, axis=1)

    # Add a title and styling to the generated HTML
    html_content = f"""
    <html>
    <head>
        <title>Offers</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            th {{ background-color: #4CAF50; color: white; }}
            h1 {{ margin-top: 40px; }}
        </style>
    </head>
    <body>
        <h1>{title1}</h1>
        {styled_df1.to_html(index=False)}
        <h1>{title2}</h1>
        {styled_df2.to_html(index=False)}
    </body>
    </html>
    """
    
    with open(filename, 'w') as file:
        file.write(html_content)




# Pattern definitions for the two types of offers
patterns_cash = {
    'Card Name': r'(\d+\.)\s(.*?)(?=\w+\s*points)',
    'Profit': r'\$(\d+[,]*\d*)\s*profit after meeting spend requirements',
    'Fee': r'\$(\d+[,]*\d*)\s*faf\.',
    'Points': r'(\d+[,]*\d*)\s*points',
    'Spend': r'Spend\s*\$(\d+[,]*\d*)',
    'Days': r'in\s*(\d+[,]*\d*)\s*days'
}

patterns_qantas = {
    'Card Name': r'(\d+\.)\s(.*?)(?=Qantas points\d+)',
    'Fee': r'\$(\d+[,]*\d*)\s*faf\.',
    'Points': r'(\d+[,]*\d*)\s*points',
    'Spend': r'Spend\s*\$(\d+[,]*\d*)',
    'Days': r'in\s*(\d+[,]*\d*)\s*days'
}

# The main processing:
csv_data = fetch_data_from_csv('churn_history.csv')
patterns_cash = {
    'Card Name': r'(\d+\.)\s(.*?)(?=\w+\s*points)',
    'Profit': r'\$(\d+[,]*\d*)\s*profit after meeting spend requirements',
    'Fee': r'\$(\d+[,]*\d*)\s*faf\.',
    'Points': r'(\d+[,]*\d*)\s*points',
    'Spend': r'Spend\s*\$(\d+[,]*\d*)',
    'Days': r'in\s*(\d+[,]*\d*)\s*days'
}
patterns_qantas = {
    'Card Name': r'(\d+\.)\s(.*?)(?=Qantas points\d+)',
    'Fee': r'\$(\d+[,]*\d*)\s*faf\.',
    'Points': r'(\d+[,]*\d*)\s*points',
    'Spend': r'Spend\s*\$(\d+[,]*\d*)',
    'Days': r'in\s*(\d+[,]*\d*)\s*days'
}

html_cash = fetch_data_from_url("https://www.rwrds.com.au/")
offers_cash = extract_data_from_html(html_cash, patterns_cash)
processed_offers_cash = process_offers(offers_cash, 'cash')
formatted_offers_cash = format_data_for_display(processed_offers_cash)

html_qantas = fetch_data_from_url("https://www.rwrds.com.au/qantas")
offers_qantas = extract_data_from_html(html_qantas, patterns_qantas)
processed_offers_qantas = process_offers(offers_qantas, 'qantas')
formatted_offers_qantas = format_data_for_display(processed_offers_qantas)

save_and_open_html_combined(formatted_offers_cash[:10], "Cash Offers", formatted_offers_qantas[:10], "Qantas Offers", "current_offers.html")
