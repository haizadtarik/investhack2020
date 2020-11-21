import requests
import pandas as pd
from analyse import get_fa, get_ta

TOKEN = # <insert-your-bot-token-here>
bot = "https://api.telegram.org/bot"+TOKEN+"/"
df = pd.read_csv('stock.csv')
names = df['Name'].to_list()
tickers = df['Ticker'].to_list()


def get_message():
    params = {'timeout': 100, 'offset': None}
    response = requests.get(bot + 'getUpdates', data=params)
    results = response.json()['result']
    latest_update = len(results) - 1
    chat_id =  results[latest_update]['message']['chat']['id']
    update = results[latest_update]['update_id']
    if 'text' in results[latest_update]['message'].keys():
        text =  results[latest_update]['message']['text'] 
    else:
        text = 'Invalid input type'
    return chat_id, text, update

def send_message(chat, reply_text):
    params = {'chat_id': chat, 'text': reply_text}
    response = requests.post(bot + 'sendMessage', data=params)
    return response

def main():
    last_update_id = 0
    print("Running...")
    stock = ''
    while True:
        chat_id, message, update_id = get_message()
        if update_id > last_update_id:
            # print(message)
            if message == '/start':
                reply = 'Hello! I\'m Trading Helper. Which stock you want to know about?'
                send_message(chat_id, reply)
            elif message == 'Invalid input type':
                send_message(chat_id, message)
            else:
                for x in tickers:
                    if x.lower() in message.lower():
                        ticker = x
                        stock = df.loc[df['Ticker'] == ticker]['Name'].values[0]
                
                if 'ta' in message.lower() or 'technical' in message.lower():
                    if len(stock)>1: 
                        response = get_ta(stock)
                        reply = 'Here is the TA for $'+ticker+':\n' +response + '\n\nTo analyse chart click the following link:\nhttps://www.investing.com/equities/'+stock+'-chart'
                    else:
                        reply = 'Sorry. I forgot the ticker. Can you please say again?'
                elif 'fa' in message.lower() or 'fundamental' in message.lower():
                    if len(stock)>1: 
                        response = get_ta(stock)
                        reply = 'FA'
                        # reply = 'Here is the FA for $'+ticker+':\n' +response + '\nTo analyse chart click the following link:\nhttps://www.investing.com/equities/'+stock+'-chart'
                    else:
                        reply = 'Sorry. I forgot the ticker. Can you please say again?'
                else:
                    reply = 'May I know whether yo want FA or TA information?' 
                    
                send_message(chat_id, reply)

            last_update_id = update_id
        else:
            continue

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()