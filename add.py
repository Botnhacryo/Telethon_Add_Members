from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time


api_id = xxxx
api_hash = 'xxxx'
phone = 'xxxx'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Nhập mã: '))
    
input_file = 'files/bin.csv'
users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        #user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('Chọn một nhóm để thêm thành viên:')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Nhập một số: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    
mode = int(input("Nhập 1 để thêm theo tên người dùng hoặc 2 để thêm theo ID: "))
n=0
for user in users:
    if  n==99 :
        print("Ngủ trong 900 giây")
        time.sleep(900) 
        n=n+1
    try:
        print ("Thêm {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Đã chọn chế độ không hợp lệ. Vui lòng thử lại.")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
        print("Waiting 700 Seconds...")
        n=n+1
        time.sleep(700)
        
    except PeerFloodError:
        print("Nhận lỗi lũ lụt từ điện tín. Tập lệnh hiện đang dừng. Vui lòng thử lại sau một thời gian.")
        sys.exit("Chương trình kết thúc")
    except UserPrivacyRestrictedError:
        print("Cài đặt quyền riêng tư của người dùng không cho phép bạn làm điều này. Bỏ qua.")
        time.sleep(100)
    except:
        traceback.print_exc()
        print("Lỗi không mong đợi")
        continue
