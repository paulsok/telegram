from credentials import TOKEN
from telegram.ext import Updater, CommandHandler
import requests
from datetime import datetime

USAGE = '/ticker <SYMBOL> (for example: /ticker BTC or /ticker ETH)'


def start(update, context):
    update.message.reply_text(USAGE)


def get_ticker(symbol):
    headers = {'User-agent': 'Mozilla/5.0'}
    url = f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}-USD'
    response = requests.get(url, headers=headers)

    result = []
    if response.status_code == 200:
        data = response.json()
        result = data['quoteResponse']['result']
    else:
        print('API request failed!')

    return result


def command(update, context):
    currency = ''

    if len(context.args) == 1:
        currency = context.args[0]
        result = get_ticker(currency)

    if len(result) > 0:
        quote_url = f'https://finance.yahoo.com/quote/{currency}-USD'

        result = result[0]
        graph_up = u'\U0001F4C8'
        graph_down = u'\U0001F4C9'
        trend = ''
        percent_change = float(round(result['regularMarketChangePercent']))

        if percent_change > 0:
            trend = graph_up
        else:
            trend = graph_down

        msg = '<strong><a href="{}">{}-USD: {}</a>{}</strong>'.format(quote_url, currency, result['regularMarketPrice'], trend)
        msg += f'\n<strong>Percentage Change:</strong> {percent_change}%'
        msg += '\n<strong>Open:</strong> {}'.format(result['regularMarketOpen'])
        msg += '\n<strong>Close:</strong> {}'.format(result['regularMarketPreviousClose'])
        msg += '\n<strong>High:</strong> {}'.format(result['regularMarketDayHigh'])
        msg += '\n<strong>Low:</strong> {}'.format(result['regularMarketDayLow'])
        msg += '\n<strong>Time:</strong> {}'.format(datetime.fromtimestamp(result['regularMarketTime']))

        update.message.reply_text(msg, parse_mode='html')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ticker", command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
