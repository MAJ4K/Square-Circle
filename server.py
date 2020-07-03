import socket
from _thread import *
import sys
import pickle
from data import Data
from random import randint

server = "192.168.1.253"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

cList = []

s.listen()
print("Server started")

cData = []

Walls = [(300,400,100,100),
(125,25,250,100),(475,25,250,100),(125,775,250,100),(475,775,250,100),
(525,450,250,50),(75,350,250,50),(10,450,50,50),(590,350,50,50),
(300,150,50,50),(150,200,50,50),(450,200,50,50),(0,250,50,50),
(600,250,50,50),(300,558,200,50),(50,667,200,50)]

pSize = 10

def colide(wall,obj):
    hwid = wall[2]/2
    hhig = wall[3]/2
    dx = obj.x - wall[0]
    dy = obj.y - wall[1]
    if abs(dy) < hhig:
        if obj.x > wall[0] - hwid - 5 and obj.x < wall[0] + hwid + 5:
            obj.x = wall[0] + ((hwid + 5) * dx/abs(dx))
    if abs(dx) < hwid:
        if obj.y > wall[1] - hhig - 5 and obj.y < wall[1] + hhig + 5:
            obj.y = wall[1] + ((hhig + 5) * dy/abs(dy))

def game_update(dataObj):
    if dataObj.x > 610:
        dataObj.x = -10
    if dataObj.x < -10:
        dataObj.x = 610
    if dataObj.y > 810:
        dataObj.y = -10
    if dataObj.y < -10:
        dataObj.y = 810
    for X in Walls:
        colide(X,dataObj)

def thread_start(conn,id):
    usertype = "player"
    conn.send(pickle.dumps(cData[id]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = data
            if not data:
                break
            elif data == "spec":
                usertype = "spectator"
                cData[id] = None
            if usertype == "spectator":
                reply = cData
            if usertype == "player":
                nearP = []
                try:
                    cData[id].x += data.x
                    cData[id].y += data.y
                    nearP.append(Data(cData[id].x, cData[id].y, cData[id].color))
                    game_update(cData[id])
                    for X in cData:
                        if X:
                            if (X.x - cData[id].x + cData[id].y - X.y) < 100: 
                                nearP.append(Data(X.x,X.y,X.color))
                    reply = nearP
                except:
                    pass
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Disconnected")
    cList[id] = False
    cData[id] = None
    conn.close()

def assignId():
    num = -1
    d = Data(randint(0,600),randint(0,800),(randint(0,255),randint(0,255),randint(0,255)))
    assigned = False
    for X in cList:
        if not X:
            assigned = True
            num = cList.index(X)
            X = True
            cData[num] = d
            break
    if not assigned:
        num = len(cList)
        cList.append(True)
        cData.append(d)
    return num


while True:
    conn, addy = s.accept()
    print(addy, " has connected")

    start_new_thread(thread_start, (conn,assignId(),))
