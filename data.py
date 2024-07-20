import yfinance as yf


def get_data(ticker, start, end):
    ticker = ticker.strip()
    stock = yf.Ticker(ticker)

    historical_data = stock.history(start=start, end=end).tail(15)
    financials = stock.financials
    marketcap = stock.info.get('marketCap', 'N/A')
    current_price = stock.info.get('currentPrice', 'N/A')
    eps = stock.info.get('trailingEps', 'N/A')

    news = []
    for article in stock.news[:3]:
        news.append(article['title'])

    return {
        'historical_data': historical_data,
        'financials': financials,
        'marketcap': marketcap,
        'current_price': current_price,
        'eps': eps,
        'news': news
    }
