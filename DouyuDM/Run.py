from Danmu import DouyuDM
from threading import Thread

def main():
    roomId=input("请输入房间号:")
    Client = DouyuDM(roomId, False)

    p1 = Thread(target=Client.keeplive)
    p1.setDaemon(True)
    p1.start()
    Threads=[]
    for i in range(5):
        Threads.append(Thread(target=Client.Start))
    for p in Threads:
        p.start()
if __name__=="__main__":
    main()