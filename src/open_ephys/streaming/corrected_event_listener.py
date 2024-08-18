
import zmq
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

def default_spike_callback(info):
    """
    Callback to handle spike events and plot them in a raster plot.

    Parameters
    ----------
    info - dict 
        Dictionary containing event information, including 'sample_number' and 'electrode'.
    """
    channel = info['electrode']  # Assuming 'electrode' is the channel number
    sample_number = info['sample_number']

    spike_data[channel].append(sample_number)  # Store the sample number for this channel

def default_ttl_callback(info):
    """
    Default callback for TTL events.

    Parameters
    ----------
    info - dict 
    """
    return

# Store spike times for each channel
spike_data = defaultdict(list)

# Initialize the figure and axis for raster plot
fig, ax = plt.subplots()

def animate(i):
    ax.clear()  # Clear previous plot
    for channel, samples in spike_data.items():
        ax.scatter(samples, [channel] * len(samples), marker='|')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Channel')
    ax.set_title('Real-Time Spiking Raster Plot')
    ax.set_ylim(-1, max(spike_data.keys()) + 1)

class EventListener:

    """
    A class that communicates with the Open Ephys Event Broadcaster plugin.
    """

    def __init__(self, ip_address='127.0.0.1', port=5557):
        self.url = f"tcp://{ip_address}:{port}"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(self.url)
        self.socket.setsockopt(zmq.SUBSCRIBE, b'')
        print("Initialized EventListener at " + self.url)

    def start(self, ttl_callback=default_ttl_callback, spike_callback=default_spike_callback):
        """
        Starts the listening process, with separate callbacks for TTL events and spikes.
        """
        print("Starting EventListener")
        while True:
            try:
                parts = self.socket.recv_multipart()
                if len(parts) == 2:
                    info = json.loads(parts[1].decode('utf-8'))
                    if info['event_type'] == 'spike':
                        spike_callback(info)
                    else:
                        ttl_callback(info)
            except KeyboardInterrupt:
                print()  # Add final newline
                break

# Initialize and start the event listener
stream = EventListener()
ani = animation.FuncAnimation(fig, animate, interval=1000)  # Update plot every second
stream.start()

plt.show()
