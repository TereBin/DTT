import requests as req
import websocket as ws
from bs4 import BeautifulSoup as bs
import re
from twitch_chat_irc import twitch_chat_irc
import time


def send_chat(channel, message):
    chat_connection.send(channel, message)
    time.sleep(3)


def on_message(connection, message):
    amount = int(find_amount.findall(message)[0][9:])
    print("Amount : " + str(amount))
    if amount < 5000:
        send_chat(channel, "!coin")
        print('-'*50)
    elif amount < 10000:
        send_chat(channel, "!dollar")
        print('-'*50)
    else:
        send_chat(channel, "!gold")
        print('-'*50)

if __name__ == "__main__":
    try:
        with open("DTT_data.txt", 'r') as DTT_data:
            data = DTT_data.readlines()
            alertbox = data[0]
            channel = data[1]
            print("="*50 + "\nConnected to", channel + "\n" + "-"*50)

    except FileNotFoundError:
        with open("DTT_data.txt", 'w') as DTT_data:
            print("="*50 + "\n파일이 존재하지 않습니다.\n등록을 진행합니다.\n")
            alertbox = input("Toonation alertbox URL : ")
            DTT_data.write(alertbox)
            DTT_data.write("\n")
            channel = input("Twitch ID : ")
            DTT_data.write(channel)
            print("\n등록이 완료되었습니다.\n" + "=" * 50 + "\nConnected to", channel + "\n" + "-" * 50)

    except IndexError:
        with open("DTT_data.txt", 'w') as DTT_data:
            print("="*50 + "\n파일 오류.\n재등록을 진행합니다.\n")
            alertbox = input("Toonation alertbox URL : ")
            DTT_data.write(alertbox)
            DTT_data.write("\n")
            channel = input("Twitch ID : ")
            DTT_data.write(channel)
            print("\n등록이 완료되었습니다.\n" + "=" * 50 + "\nConnected to", channel + "\n" + "-" * 50)

    raw_data = req.post(alertbox)

    find_payload = re.compile("\"payload\":\"\w+")
    find_amount = re.compile("\"amount\":\d+")

    username = 'TereBin_Bot'
    oauth = "oauth:******************************"
    chat_connection = twitch_chat_irc.TwitchChatIRC(username, oauth)

    while True:
        payload = None

        try:
            if str(raw_data) != "<Response [200]>":
                print("Alertbox Response not 200. Automatically restarting after 5 seconds.")
                time.sleep(5)
            else:
                print('-'*50 + "\nAlertbox Response 200\n" + '-'*50)
                data = bs(raw_data.text, "html.parser")
                data = data.select('head')
                payload = find_payload.findall(str(data))[0][11:]
                print("Toonation payload parsed\n" + '-'*50)

                ws_connection = ws.WebSocketApp("wss://toon.at:8071/" + payload, on_message=on_message)

                while True:
                    print("Connected to toonation\n" + '='*50)
                    ws_connection.run_forever()
                    print("Toonation timeout. re-connecting\n" + "-"*50)

        except:
            print("Error occurred. Automatically restarting after 5 seconds.")
            time.sleep(5)
            pass
