import requests as req
import websocket as ws
from bs4 import BeautifulSoup as bs
import re
import time
import json


uri = "ws://127.0.0.1:42069/websocket"
trig = ws.WebSocket()
trig.connect(uri)


def coin(trig):
    print("coin")
    uri = "ws://127.0.0.1:42069/websocket"
    trig = ws.WebSocket()
    trig.connect(uri)
    trig.send(payload=coin_message, opcode=1)
    trig.close()


def dollar(trig):
    print("dollar")
    uri = "ws://127.0.0.1:42069/websocket"
    trig = ws.WebSocket()
    trig.connect(uri)
    trig.send(payload=dollar_message, opcode=1)
    trig.close()


def gold(trig):
    print("gold")
    uri = "ws://127.0.0.1:42069/websocket"
    trig = ws.WebSocket()
    trig.connect(uri)
    trig.send(payload=gold_message, opcode=1)
    trig.close()


def on_message(connection, message):
    amount = int(find_amount.findall(message)[0][9:])
    print("Amount : " + str(amount))
    if amount < 5000:
        coin(trig)
        print('-'*50)
    elif amount < 10000:
        dollar(trig)
        print('-'*50)
    else:
        gold(trig)
        print('-'*50)


if __name__ == "__main__":
    try:
        with open("DTT_data.txt", 'r') as DTT_data:
            data = DTT_data.readlines()
            alertbox = data[0]
            channel = data[1]
            coin_message = data[2]
            dollar_message = data[3]
            gold_message = data[4]
            print("="*50 + "\nConnected to", channel + "\n" + "-"*50)

    except FileNotFoundError:
        with open("DTT_data.txt", 'w') as DTT_data:
            print("="*50 + "\n파일이 존재하지 않습니다.\n등록을 진행합니다.\n")
            alertbox = input("Toonation alertbox URL : ")
            DTT_data.write(alertbox)
            DTT_data.write("\n")
            channel = input("Twitch ID : ")
            DTT_data.write(channel)
            DTT_data.write("\n")
            req_message = str({
                "apiName": "TITSPublicApi",
                "apiVersion": "1.0",
                "requestID": "1",
                "messageType": "TITSTriggerListRequest"
            })
            trig_message = {
                "apiName": "TITSPublicApi",
                "apiVersion": "1.0",
                "requestID": "someID",
                "messageType": "TITSTriggerActivateRequest",
                "data": {
                    "triggerID": ""
                }
            }
            trig.send(payload=req_message, opcode=1)
            trig_data = json.loads(trig.recv())['data']['triggers']
            for i in trig_data:
                if i['name'] == 'coin':
                    coin_message = trig_message.copy()
                    coin_message["data"]["triggerID"] = i['ID']
                    coin_message = str(coin_message)
                    DTT_data.write(coin_message)
                    DTT_data.write("\n")
                    print("coin 등록 완료")
                elif i['name'] == 'dollar':
                    dollar_message = trig_message.copy()
                    dollar_message["data"]["triggerID"] = i['ID']
                    dollar_message = str(dollar_message)
                    DTT_data.write(dollar_message)
                    DTT_data.write("\n")
                    print("dollar 등록 완료")
                elif i['name'] == 'gold':
                    gold_message = trig_message.copy()
                    gold_message["data"]["triggerID"] = i['ID']
                    gold_message = str(gold_message)
                    DTT_data.write(gold_message)
                    print("gold 등록 완료")
            print("\n등록이 완료되었습니다.\n" + "=" * 50 + "\nConnected to", channel + "\n" + "-" * 50)

    except IndexError:
        with open("DTT_data.txt", 'w') as DTT_data:
            print("="*50 + "\n파일 오류.\n재등록을 진행합니다.\n")
            alertbox = input("Toonation alertbox URL : ")
            DTT_data.write(alertbox)
            DTT_data.write("\n")
            channel = input("Twitch ID : ")
            DTT_data.write(channel)
            DTT_data.write("\n")
            req_message = str({
                "apiName": "TITSPublicApi",
                "apiVersion": "1.0",
                "requestID": "1",
                "messageType": "TITSTriggerListRequest"
            })
            trig_message = {
                "apiName": "TITSPublicApi",
                "apiVersion": "1.0",
                "requestID": "someID",
                "messageType": "TITSTriggerActivateRequest",
                "data": {
                    "triggerID": ""
                }
            }
            trig.send(payload=req_message, opcode=1)
            trig_data = json.loads(trig.recv())['data']['triggers']
            for i in trig_data:
                if i['name'] == 'coin':
                    coin_message = trig_message.copy()
                    coin_message["data"]["triggerID"] = i['ID']
                    coin_message = str(coin_message)
                    DTT_data.write(coin_message)
                    DTT_data.write("\n")
                    print("coin 등록 완료")
                elif i['name'] == 'dollar':
                    dollar_message = trig_message.copy()
                    dollar_message["data"]["triggerID"] = i['ID']
                    dollar_message = str(dollar_message)
                    DTT_data.write(dollar_message)
                    DTT_data.write("\n")
                    print("dollar 등록 완료")
                elif i['name'] == 'gold':
                    gold_message = trig_message.copy()
                    gold_message["data"]["triggerID"] = i['ID']
                    gold_message = str(gold_message)
                    DTT_data.write(gold_message)
                    print("gold 등록 완료")
            print("\n등록이 완료되었습니다.\n" + "=" * 50 + "\nConnected to", channel + "\n" + "-" * 50)

    raw_data = req.post(alertbox)

    find_payload = re.compile("\"payload\":\"\w+")
    find_amount = re.compile("\"amount\":\d+")

    while True:
        payload = None

        try:
            if str(raw_data) != "<Response [200]>":
                print("Alertbox Response not 200. Automatically restarting after 5 seconds.")
                time.sleep(5)
            else:
                print('-'*50 + "\nDTT 1.1\n" + '-'*50)
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
