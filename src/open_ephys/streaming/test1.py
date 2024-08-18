




import zmq
import json

url = "tcp://127.0.0.1:5557"

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(url)

for eventType in (b'ttl', b'spike'):
   socket.setsockopt(zmq.SUBSCRIBE, eventType)

def callback(info):
   #do something with the incoming data
   print(info)
   print("SPK")

while True:
    
   parts = socket.recv_multipart()
   print("SPK")

   event_info = json.loads(parts[1].decode('utf-8'))

   callback(event_info)