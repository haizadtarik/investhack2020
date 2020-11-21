import requests
import pandas as pd

TOKEN = '1291071980:AAE5nltPjU627ZeFgCWE5PtjLdw1_cbnt1o'
bot = "https://api.telegram.org/bot"+TOKEN+"/"
df = pd.read_csv('stock.csv')

def get_reply(input_text):
    names = df['Name'].to_list()
    tickers = df['Ticker'].to_list()

    for x in tickers:
        if x.lower() in input_text.lower():
            ticker = x

    stock = df.loc[df['Ticker'] == ticker]['Name'].values[0]

    response = requests.get('http://localhost:5000/ta?text='+stock)
    return response.text

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
    while True:
        chat_id, message, update_id = get_message()
        if update_id > last_update_id:
            # print(message)
            if message == '/start':
                reply = 'Hello! I\'m Trading Helper. How I may help you?'
                send_message(chat_id, reply)
            elif message == 'Invalid input type':
                send_message(chat_id, message)
            else:
                reply = get_reply(message) 
                send_message(chat_id, reply)
            last_update_id = update_id
        else:
            continue

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()