from appwrite.client import Client
import os
import json
import time
import traceback
import jwt
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests

from appwrite.services.account import Account
from appwrite.services.avatars import Avatars
from appwrite.services.databases import Databases
from appwrite.services.functions import Functions
from appwrite.services.health import Health
from appwrite.services.locale import Locale
from appwrite.services.storage import Storage
from appwrite.services.teams import Teams
from appwrite.services.users import Users
from appwrite.query import Query
from datetime import datetime, timedelta
from agora_token_builder import RtcTokenBuilder


# This is your Appwrite function
# It's executed each time we get a request
def generate_agora_token(app_id, app_certificate, channel_name, user_id, expiration_time_in_seconds=3600):
      
        agora_key = app_id
        agora_secret = app_certificate
        agora_channel_name = channel_name
        agora_user_id = user_id

        expiration_time = int(time.time()) + expiration_time_in_seconds
   
        token_payload = {
        "iss": agora_key,
        "exp": expiration_time,
        "sub": agora_channel_name,
        "user": {
            "uid": agora_user_id,
        },
        }  

        return RtcTokenBuilder.buildTokenWithUid(agora_key, agora_secret, agora_channel_name, agora_user_id, agora_user_id,
                                             expiration_time)
   


def send_data_only_message(registration_token, custom_data):
    # FCM API URL'si
    url = 'https://fcm.googleapis.com/fcm/send'

    # Firebase Console'dan oluşturduğunuz server key'i
    server_key = 'key=AAAA6X4hP80:APA91bHWyK0tS9iYEiOTMC9ij-Sc1oPyHLd9jKGE9sZMjvy-mb1U4loRBsv0fnhdJeIM_6H5VgE2kBTX5hWv31duB7i5rjBljpWBH-USklu_MAwgVRdTr_031OuF81IvwofGwL_kxMsl'

    # Veri içeriğini oluştur
    data = {
        'data': custom_data,
        'to': registration_token
    }

    # Headers ayarları
    headers = {
        'Authorization': server_key,
        'Content-Type': 'application/json'
    }

    # Veri içeren mesajı gönder
    response = requests.post(url, json=data, headers=headers)
    print(headers)

    # İsteğin başarılı olup olmadığını kontrol et
    if response.status_code == 200:
        print("Veri içeren mesaj başarıyla gönderildi.")
    else:
        print("Veri içeren mesaj gönderme hatası:", response.text)
        
def main(context):
    client = Client()
    client.set_endpoint("http://162.19.255.235/v1")
    client.set_project("6506073c9158e012f6d3")
    client.set_key("f70c6d75b3cd8878c999dd211a18509d52269c25d4bb5f4fc8e8edc42fec27e7087b29e51ec6fbb52546f520757aa46b3624902f5b58cfc8a0fc1d3b30b5cd20602f6b6e156603551c40b97d99534d841bb1e175093f954d7cc9d3fb41a78e75bc60740d67b4b69ef911392029892d6a8ae0698cc981df34d100b2fccc45aa5b")
    client.set_self_signed(True)

  # You can remove services you don't use
    account = Account(client)
    avatars = Avatars(client)
    database = Databases(client)
    functions = Functions(client)
    health = Health(client)
    locale = Locale(client)
    storage = Storage(client)
    teams = Teams(client)
    users = Users(client)

    parsed_data = json.loads(context.req.body)

# "gender" parametresini alın
    gender = parsed_data.get("gender")

    callId =  parsed_data.get("callId")
    channelId = parsed_data.get("channelId")
    hostUserId =  parsed_data.get("hostUserId")
    guestUserId = parsed_data.get("guestUserId")

    callFilter = [Query.equal('id', callId)]
    print(callId)
    callData = database.list_documents('chat-1', "002", callFilter)
    callObject = callData['documents'][0]
    print(callObject)

    channelFilter = [Query.equal('id', channelId)]
    channelData = database.list_documents('chat-1', "003", channelFilter)
    channelObject = channelData['documents'][0]
    print(channelObject)

    app_id = "11a2e38247e641cf930c51e93803509d"
    app_certificate = "7a8e8b3dd56e4991861bd7b46ae8814f"
    channel_name = channelObject["agoraChannelName"]
    user1_id = 0
    user2_id = 0
    print(app_id)
    print(app_certificate)
    print(channel_name)
    print(user1_id)
    # İlk kullanıcı için token oluşturun
    user1_token = generate_agora_token(app_id, app_certificate, channel_name, user1_id)

    # İkinci kullanıcı için token oluşturun
    user2_token = generate_agora_token(app_id, app_certificate, channel_name, user2_id)

    # Token'ları yazdırın
    print("User 1 Token:", user1_token)
    print("User 2 Token:", user2_token)
    channelObject["agoraTokenHost"] = user1_token
    channelObject["agoraTokenGuest"] = user2_token

    documentId = channelObject["$id"].replace(" ", "")
    print("test" + documentId)
    

    updated_data = {
        'agoraTokenHost': user1_token,
        'agoraTokenGuest': user2_token,
        # Diğer alanlar ve değerleri
    }
    result = database.update_document('chat-1', "003", documentId, updated_data)

    hostFilter = [Query.equal('userId', hostUserId)]
    hostData = database.list_documents('chat-1', "001", hostFilter)
    hostObject = hostData['documents'][0]
    print(hostObject)

    guestFilter = [Query.equal('userId', guestUserId)]
    guestData = database.list_documents('chat-1', "001", guestFilter)
    guestObject = guestData['documents'][0]
    print(guestObject)

    registration_token = guestObject['firebaseToken'].replace(" ", "")
    custom_data = {
        'title': hostObject["userName"] + " sizi arıyor",
        'body': "Hadi konuma başlasın!",
        'hostUserId': hostObject["userId"],
        'callId': callId,
        'channelId': channelId,
        'agoraChannelName': channelObject["agoraChannelName"],
        'agoraToken': channelObject["agoraToken"],
        'notificationType': "userCall"
    }

    send_data_only_message(registration_token, custom_data)


    return {"users": custom_data}     
 
