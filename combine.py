import asyncio
from data import get_data
from scrape import scrape_earnings_data
from datetime import datetime, timedelta



def organize_all_data():
    companies = asyncio.run(scrape_earnings_data(datetime.now()))
    start_day = "2023-01-01"
    end_day = datetime.now().strftime('%Y-%m-%d')
    prompt_data = ""
    for company in companies:
        company_data = get_data(company['ticker'], start_day, end_day)
        if not company_data:
            continue  
        prompt_data += f"Company name: {company['company']} ({company['ticker']})\n"
        prompt_data += f"Earnings day: {company['date']}\n"
        
        historical_data_str = company_data['historical_data'].to_string() if not company_data['historical_data'].empty else "No historical data available"
        financials_str = company_data['financials'].to_string() if not company_data['financials'].empty else "No financials available"
        news_str = "\n".join(company_data['news']) if company_data['news'] else "No news available"
        
        prompt_data += f"Historical Data: {historical_data_str}\n"
        prompt_data += f"Financials: {financials_str}\n"
        prompt_data += f"Marketcap: {company_data['marketcap']}\n"
        prompt_data += f"Current Price: {company_data['current_price']}\n"
        prompt_data += f"EPS: {company_data['eps']}\n"
        prompt_data += f"Recent News Headlines: {news_str}\n"
        prompt_data += "--------------------------------------------------------------------------------------------------------------------\n"

    return prompt_data
