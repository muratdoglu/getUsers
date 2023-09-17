from appwrite.client import Client
import os
import json
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

# This is your Appwrite function
# It's executed each time we get a request
def main(context):
   
  print("Context verileri: %s", context)
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

    # online olanlar

  allUsers = []

  print(1)
  print("123")
  allUsers.clear()
    # hiç aranmamışlar
    
     # son 30 dakikada online olanlar
  current_time2= datetime.now()
  two_days_ago2 = current_time2 - timedelta(2)
  filters52 = [Query.greater_than('lastOnline', two_days_ago2),
                Query.equal('gender', gender),
                  Query.equal('isOnline', True),
                   Query.equal('live', True)
                ]
  data52 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters52)
  documents52 = data52['documents']
  allUsers += documents52 # Append documents2 to allUsers
  
    # son 30 dakikada online olanlar
  current_time1= datetime.now()
  two_days_ago1 = current_time1 - timedelta(2)
  filters51 = [Query.greater_than('lastOnline', two_days_ago1),
                Query.equal('gender', gender),
                  Query.equal('isOnline', True)
                ]
  data51 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters51)
  documents51 = data51['documents']
  allUsers += documents51 # Append documents2 to allUsers
  
  
  filters2 = [Query.equal('callGuestCount', 0),
                Query.equal('gender', gender),
                 Query.equal('isOnline', True)]
  data2 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters2)
  documents2 = data2['documents']

  allUsers += documents2  # Append documents2 to allUsers
  print(allUsers)

    #  arama alma ve cevaplama oranı +5 olanlar
  filters3 = [Query.greater_than('callGuestAnsweredPoint', 5),
                Query.equal('gender', gender),
                  Query.equal('isOnline', True)]
  data3 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters3)
  documents3 = data3['documents']

  allUsers += documents3  # Append documents2 to allUsers
  print(allUsers)

    #  aktif arama yapanlar
  filters4 = [Query.greater_than('callHostCount', 40),
                Query.greater_than('callGuestAnsweredPoint', -5),
                Query.equal('gender', gender),
                  Query.equal('isOnline', True)]
  data4 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters4)
  documents4 = data4['documents']
  allUsers += documents4  # Append documents2 to allUsers

  print(allUsers)

    # son 2 günde online olanlar
  current_time = datetime.now()
  two_days_ago = current_time - timedelta(2)
  filters5 = [Query.greater_than('lastOnline', two_days_ago),
                Query.equal('gender', gender),
                  Query.equal('isOnline', True)
                ]
  data5 = database.list_documents('6506087581ce0a10ef2a', "6506088f22805d12b4fe", filters5)
  documents5 = data5['documents']
  allUsers += documents5  # Append documents2 to allUserssource myenv/bin/activate

  
  print("kemal")
  for user in allUsers:
    del user["$collectionId"]
    del user["$createdAt"]
    del user["$databaseId"]
    del user["$id"]
    del user["$permissions"]
    del user["$updatedAt"]
    del user["createdDate"]
    del user["lastOnline"]

  print(allUsers)   
  return context.res.json({
    "users": allUsers,
  })
