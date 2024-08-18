

import zmq
import json
import matplotlib.pyplot as plt
import numpy as np


spike_count = 0  ;
event_count = 0;
event_t = [];
spike_t_ch = [];

def default_spike_callback(info):
    
    global spike_count 
    
    spike_count += 1  # Increment spike count for each received spike
    print(f"Total received spikes: {spike_count}")  # Print the current spike count
    print(f"Received spike event: {info}")  # Print the info dictionary for inspection
    
    # Attempt to extract the timestamp if it exists
    sample_number = info.get('sample_number')
    electrode = info.get('electrode')
    electrode_number = int(electrode[-3:])
 
    
    if sample_number:
        spike_t_ch.append([sample_number electrode_number])
        
            else:
        print("No 'timestamp' key found in spike event.")
        
    

def default_ttl_callback(info):

    
 global event_count
 event_count += 1  # Increment spike count for each received spike
 print(f"Total received event: {event_count}")  # Print the current spike count
 
 print(f"Received event event: {info}")  # Print the info dictionary for inspection
 
 # Attempt to extract the timestamp if it exists
 sample_number = info.get('sample_number')
 event_t.append(sample_number)

     






class EventListener:

   

    def __init__(self, ip='127.0.0.1', port=5557):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{ip}:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

        self.callbacks = {
            'spike': default_spike_callback,
            'ttl': default_ttl_callback
        }

    def register_callback(self, event_type, callback):
        if event_type in self.callbacks:
            self.callbacks[event_type] = callback
        else:
            print(f"Event type {event_type} not recognized.")

    def listen(self):
        print("Listening for events...")
        
        try:
            while True:
                message = self.socket.recv()
                try:
                    info = json.loads(message)
                    event_type = info.get('event_type')
                    if event_type in self.callbacks:
                        self.callbacks[event_type](info)
                except json.JSONDecodeError:
                    # print("Received invalid JSON message, skipping...")
                    1
        except KeyboardInterrupt:
            pass
        input("Press Enter to stop listening...")

    def stop(self):
        self.socket.close()
        self.context.term()
        print("Listener stopped.")




# Example usage
if __name__ == '__main__':
    stream = EventListener()
    stream.register_callback('spike', default_spike_callback)
    stream.register_callback('ttl', default_ttl_callback)
    stream.listen()
    stream.stop()
  

















 # """
 # A class that communicates with the Open Ephys Event Broadcaster plugin.
 
 # See: https://open-ephys.github.io/gui-docs/User-Manual/Plugins/Event-Broadcaster.html
 # for more info.
 
 # It can be used to receive TTL events and spike times over a network connection.

 # IMPORTANT: The Event Broadcaster must be configured to send events in "JSON" format.
 
 # To use, first create an EventListener object:
     
 #     >> stream = EventListener()
     
 # Then, define a callback function for TTL events, spikes, or both:
 
 #     >> stream.register_callback('spike', your_spike_callback)
 #     >> stream.register_callback('ttl', your_ttl_callback)
     
 # Finally, start listening for events:
 
 #     >> stream.listen()
     
 # To stop listening:
 
 #     >> stream.stop()
     
 # The program will automatically exit after stop() is called.
 # """











