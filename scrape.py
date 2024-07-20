import asyncio
import time
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime, timedelta

def get_monday_date(current_date):
    if current_date.weekday() == 1:
        current_date = current_date - timedelta(days=1)
    elif current_date.weekday() == 2:
        current_date = current_date - timedelta(days=2)
    elif current_date.weekday() == 3:
        current_date = current_date - timedelta(days=3) 
    elif current_date.weekday() == 4:
        current_date = current_date - timedelta(days=4)
    elif current_date.weekday() == 5:
        current_date = current_date + timedelta(days=2)
    elif current_date.weekday() == 6:
        current_date = current_date + timedelta(days=1)

    return current_date.strftime('%Y-%m-%d')

async def scrape_earnings_data(date):

    data = []
    url = "https://www.nasdaq.com/market-activity/earnings"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=120000)

        await page.click('button#onetrust-accept-btn-handler', timeout=0)
        
        monday = get_monday_date(datetime.now())
        monday_date = pd.to_datetime(monday)

        friday_date = monday_date + timedelta(days=4)

        if not await page.query_selector(f'button[data-year="{monday_date.year}"][data-month="{monday_date.month:02}"][data-day="{monday_date.day:02}"]'):
            await page.click('button.time-belt__prev')
            await page.wait_for_timeout(1000)
        
        if not await page.query_selector(f'button[data-year="{friday_date.year}"][data-month="{friday_date.month:02}"][data-day="{friday_date.day:02}"]'):
            await page.click('button.time-belt__next')
            await page.wait_for_timeout(1000)

        for i in range(5):
            current_date = monday_date + timedelta(days=i)
            year = current_date.year
            month = current_date.month
            day = current_date.day
            
            await page.wait_for_selector(f'button[data-year="{year}"][data-month="{month:02}"][data-day="{day:02}"]')
            await page.click(f'button[data-year="{year}"][data-month="{month:02}"][data-day="{day:02}"]')
            
            time.sleep(5)

            await page.wait_for_selector('tr.market-calendar-table__row')
            rows = await page.query_selector_all('tr.market-calendar-table__row')
            
            for row in rows[:2]:
                cols = await row.query_selector_all('td')
                if len(cols) >= 2:
                    ticker = await cols[0].inner_text()
                    company = await cols[1].inner_text()
                    data.append({'ticker': ticker, 'company': company, 'date': current_date.strftime('%Y-%m-%d')})

    return data
