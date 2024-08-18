import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.animation as animation

# Define a structure to store spike data
spike_data = defaultdict(list)  # {channel_number: [list of sample numbers]}

def default_spike_callback(info):
    """
    Code to run when a spike event is received.
    
    Parameters
    ----------
    info - dict
        Spike event information including 'sample_number' and 'electrode'
    """
    sample_number = info['sample_number']
    electrode_number = info['electrode']
    
    # Store spike data
    spike_data[electrode_number].append(sample_number)
    
    # Update the raster plot
    update_raster_plot(electrode_number, sample_number)

# Initialize the plot
fig, ax = plt.subplots()

# Update function for the animation
def update_raster_plot(electrode_number, sample_number):
    ax.plot(sample_number, electrode_number, 'k.', markersize=2)
    ax.set_xlim(left=max(0, sample_number - 1000), right=sample_number + 1000)
    ax.set_ylim(bottom=min(spike_data.keys()), top=max(spike_data.keys()))
    plt.draw()

# To set up real-time updating, use matplotlib animation
def animate(i):
    ax.clear()
    for electrode, samples in spike_data.items():
        ax.plot(samples, [electrode] * len(samples), 'k.', markersize=2)

    ax.set_xlim(left=max(0, max(max(samples) for samples in spike_data.values()) - 1000), 
                right=max(max(samples) for samples in spike_data.values()) + 1000)
    ax.set_ylim(bottom=min(spike_data.keys()), top=max(spike_data.keys()))
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Electrode Number')
    ax.set_title('Real-Time Raster Plot')

ani = animation.FuncAnimation(fig, animate, interval=100)

# Show the plot in real-time
plt.show()
