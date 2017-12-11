from socket import socket, AF_INET, SOCK_STREAM
import time
from threading import Thread
import re

class DouyuDM(object):
    def __init__(self,roomid, modelset=False):
        self.roomid = roomid
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.model = modelset
        self.level_find=re.compile(b'level@=(.+?)/sahf@')
        self.id_find = re.compile(b'nn@=(.+?)/txt@')
        self.danmu_find = re.compile(b'txt@=(.+?)/cid@')
        self.connect_msg = 'type@=loginreq/roomid@={0}/\0'.format(self.roomid)
        self.group_msg = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(self.roomid)
        print("开始连接弹幕服务器...")
        try:
            self.sock.connect(('openbarrage.douyutv.com',8601))
            self.send_msg(self.connect_msg)
            self.send_msg(self.group_msg)
            print("成功连接服务器！")
        except Exception as e:
            print("连接服务器失败，请重试")
            exit()

    def Start(self):
       while True:
            # 服务端返回的数据 recieve data from the server
            data = self.sock.recv(4096)
            self.handle(data)



    def send_msg(self, msgstr):
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
        保持心跳，15秒心跳请求一次 send request every 15 seconds to keep the heart beating
         '''

        while True:

            try:
                msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
                self.send_msg(msg)

                time.sleep(15)
            except Exception as e:
                pass

    def handle(self, data):
        danmu_username = self.id_find.findall(data)
        danmu_content = self.danmu_find.findall(data)
        level=self.level_find.findall(data)
        if not data:
            pass

        else:
            for i in range(0, len(danmu_content)):
                try:
                    # 输出信息 output the message
                    print('[{}][等级:{}]:{}'.format(danmu_username[i].decode(
                        'utf8'),level[i].decode("utf8"), danmu_content[i].decode(encoding='utf8')))

                except:
                    continue


