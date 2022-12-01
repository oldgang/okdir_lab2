import socket
import sys
import time

MCAST_GRP = "239.0.0.3"
MCAST_PORT = 3000
HOST_IP = '192.168.0.68'
messages = ["C2","C1","C3"]

def check(buffer, counter):
    # print(f"CHECK({buffer})")
    # buffer is empty, return False
    if len(buffer) == 0:
        return False
    # get the order of collected messages
    order = list()
    for message in buffer:
        order.append(int(message[1:]))
    # sort the collected messages and check if they are all in order
    # print(f"counter: {counter}")
    order.sort()
    orderCorrect = [x for x in range(counter, counter+len(order))]
    # print(f"order.sort(): {order}")
    # print(f"orderCorrect: {orderCorrect}\n\n")
    if order == orderCorrect:
        return True
    else:
        return False

def receiveMessages(data, server):
    host = server[0]
    #A
    if '.70' in host:
        buffers[0].append(data)
    #B
    elif '.69' in host:
        buffers[1].append(data)
    #C
    elif '.68' in host:
        buffers[2].append(data)
    
    for i in range(3):
        if(check(buffers[i], counters[i])):
            buffers[i].sort()
            print(buffers[i])
            counters[i] += len(buffers[i])
            buffers[i].clear()
        else:
            continue

def recv():
    try:
        timeEnd = time.time() + 3
        while time.time() < timeEnd:
            data, server = sock.recvfrom(1024)
            receiveMessages(data.decode(), server)
    except socket.timeout:
        print("Socket timeout, returning to main loop")
        return

def snd():
    for message in messages:
        sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))
        print(f"Message {message} sent!")
        if sys.stdin.readline().strip() is not None:
            continue
    print("Finished sending data")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 3000))
mreq = socket.inet_aton(MCAST_GRP) + socket.inet_aton(HOST_IP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.settimeout(3)

buffers = [list(), list(), list()]
counters = [1, 1, 1]

while True:
    key = sys.stdin.readline().strip()
    
    # receive messages -> R
    if key == 'r':
        buffers = [list(), list(), list()]
        counters = [1, 1, 1]
        recv()
 
    # send message -> S
    if key == 's':
        snd()
 
    # leave multicast group and exit -> Q
    if key == 'q':
        print("Leaving group and exiting")
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        sock.close()
        break