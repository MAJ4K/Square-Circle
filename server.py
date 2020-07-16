####
####    Must make a player class tuples cant be changed
####
####
####
from random import randint
from splayer import Entity
import socket
import pickle
from _thread import *
import sys

server = "192.168.1.253"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen()
print("Server started")
serverup = True
    

def server_control():   # control C to stop the server
    pass

BLOCKS = [
    (325,225,150,150),
    (-100,575,450,300),
    (450,575,450,300),
    (-100,0,450,25),
    (450,0,450,25),
    (-10,400,310,50),
    (750,400,60,50),
    (575,100,75,400),
    (100,100,75,75),
    (300,100,75,75)
]

PLAYERSIZE = 10
values = {
    "xv" : 0.0,
    "yv" : 0.0,
    "xa" : 0.0,
    "ya" : 0.0,
    "xf" : 0.0,
    "yf" : 0.0,
    "jump" : False
}

players = []
bullets = []
pvels = {}
G = .03

edges = (-10,-10,810,610)

def collision(id):
    p = players[id]
    hp = p.size/2
    for X in BLOCKS:
        hwid = X[2]/2
        hhig = X[3]/2
        Xxc = X[0] + hwid - p.size
        Xyc = X[1] + hhig - p.size
        dx = p.x - Xxc
        dy = p.y - Xyc
        if abs(dx) < hwid:
            if p.y > Xyc - hhig - hp and p.y < Xyc + hhig + hp:
                p.y = Xyc + ((hhig + hp) * dy/abs(dy))
                pvels[id]["ya"] -= G
                if dy < 0:
                    pvels[id]["jump"] = True
        if abs(dy) < hhig:
            if p.x > Xxc - hwid - hp and p.x < Xxc + hwid + hp:
                p.x = Xxc + ((hwid + hp) * dx/abs(dx))
                pvels[id]["ya"] -= G

def controlP(Controls, id):
    p = players[id]
    up = Controls[0]
    down = Controls[2]
    left = Controls[1]
    right = Controls[3]
    shoot = Controls[4]

    K = .4
    decc = lambda a: a*K

    if up:
        if pvels[id]["jump"]:
            pvels[id]["jump"] = False
            pvels[id]["ya"] -= 1
        else:
            pvels[id]["ya"] -= 0.01
    if down:
        pvels[id]["ya"] += 0.01
    if right:
        pvels[id]["xa"] += 0.01
    if left:
        pvels[id]["xa"] -= 0.01

    pvels[id]["ya"] += G
    if pvels[id]["ya"] > 1:
        pvels[id]["ya"] = 1
    if pvels[id]["ya"] < -1.5:
        pvels[id]["ya"] = -1.5
    collision(id)
    pvels[id]["xa"] -= decc(pvels[id]["xa"])
    pvels[id]["ya"] -= decc(pvels[id]["ya"])
    K = 0.01
    pvels[id]["xv"] += pvels[id]["xa"] - decc(pvels[id]["xv"])
    pvels[id]["yv"] += pvels[id]["ya"] - decc(pvels[id]["yv"])

    p.x += pvels[id]["xv"]
    p.y += pvels[id]["yv"]

    if p.x > edges[2]:
        p.x = edges[0]
    if p.x < edges[0]:
        p.x = edges[2]
    if p.y > edges[3]:
        p.y = edges[1]
    if p.y < edges[1]:
        p.y = edges[3]

    

def client_thread(conn,id):
    reply = ""
    #data = pickle.loads(conn.recv(2048))
    ptype = "play"
    #if data == "spec":
    #    ptype = "spec"
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            reply = data
            if not data:
                break
            if ptype == "play":
                controlP(data,id)
                reply = (players,bullets)
            conn.send(pickle.dumps(reply))
        except:
            break
    print("Player ", id, "Disconnected")
    players[id] = None
    conn.close()
            
def assignId():
    x = randint(0,800)
    y = randint(0,600)
    color = (randint(0,255),randint(0,255),randint(0,255))
    d = Entity(x,y,color,PLAYERSIZE)

    assigned = False
    i = 0
    for i,X in enumerate(players):
        if not X:
            assigned = True
            break
        
    if assigned:
        players[i] = d
    else:
        i = len(players)
        players.append(d)
    
    pvels[i] = values.copy()

    return i

while serverup:
    conn, addy = s.accept()
    pid = assignId()
    print(addy, " has connected as player ", pid)
    conn.send(pickle.dumps(pid))
    start_new_thread(client_thread, (conn,pid))