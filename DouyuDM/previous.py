from socket import socket,AF_INET,SOCK_STREAM
import time
from threading import Thread
import re
from queue import Queue

class DouyuDM(object):
    def __init__(self,q,roomid,modelset=False):
        self.roomid=roomid
        self.sock=socket(AF_INET,SOCK_STREAM)
        self.model=modelset
        self.queue=q
        self.id_find = re.compile(b'nn@=(.+?)/txt@')
        self.danmu_find = re.compile(b'txt@=(.+?)/cid@')



    def Start(self):
        roomid=self.roomid
        modelset=self.model
        host='openbarrage.douyutv.com'
        port=8601
        connect_msg='type@=loginreq/roomid@={0}/\0'.format(roomid)
        group_msg='type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
        print("开始连接弹幕服务器...")
        try:
            self.sock.connect((host,port))
            self.send_msg(connect_msg)
            self.send_msg(group_msg)
            print("连接成功")
        except Exception as e:
            print("连接服务器失败，请重试")
        while True:
            # 服务端返回的数据
            data = self.sock.recv(4096)
            self.handle(data)



     #   if modelset:
     #       pass
     #   else:
      #      pass

    def send_msg(self,msgstr):
        msg = msgstr.encode('utf-8')
        data_length = len(msg) + 8
        code = 689

        # 构造协议头 build the head of the protocol
        msgHead = int.to_bytes(data_length, 4, 'little') \
                  + int.to_bytes(data_length, 4, 'little') + \
                  int.to_bytes(code, 4, 'little')
        self.sock.send(msgHead)
        sent = 0

        # 保证信息全部发送 Make sure all the messages are successfully sent
        while sent < len(msg):
            tn = self.sock.send(msg[sent:])
            sent = sent + tn

    def keeplive(self):
        '''
        保持心跳，15秒心跳请求一次
         '''
       # print('准备连接服务器')
        #print('准备发送心跳包')
        while True:

            try:
                msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
                self.send_msg(msg)

                time.sleep(15)
            except Exception as e:
                pass
    def handle(self,data):
        danmu_username = self.id_find.findall(data)
        danmu_content = self.danmu_find.findall(data)
        if not data:
            pass

        else:
            for i in range(0, len(danmu_content)):
                try:
                    # 输出信息
                    print('[{}]:{}'.format(danmu_username[i].decode(
                        'utf8'), danmu_content[i].decode(encoding='utf8')))
                except:
                    continue


q=Queue()
Client=DouyuDM(q,2267291,False)
p1 = Thread(target=Client.Start)
p2 = Thread(target=Client.keeplive)
#p3=Thread(target=Client.handle)
p1.start()
time.sleep(2)
p2.start()
#p3.start()

