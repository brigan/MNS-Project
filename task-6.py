"""Project task 6: Simulate the model with inputs consisting of bursts
of action potentials. To this end, take that the inputs are silent
except for isolated events represented by bursts of spikes with a
Poisson distribution at 100 Hz for 20 ms. The inputs arrive at each
synapse with random latencies drawn from Gaussian distribution (mean
0, standard deviation 15 ms). Plot a response to the same of burst of
spikes at the beginning and at the end of the simulation. Plot the
weights of synapses as a function of the relative latencies of
incoming spike bursts (Song et al., 2000, Figure 4).
"""

import numpy.random as rand
import pylab as plt
from neuron import *

# simulation parameters
SIM_DURATION = 10000 # ms
DELTA_T      = 0.001 # ms

# pre-synaptic events occur every EVENT_PERIOD
EVENT_PERIOD = 250 # ms

# parameters for single spike burst (poisson)
BURST_DURATION = 20  # ms
BURST_FREQ     = 100 # Hertz

# create axons
a = [Axon(0.1, 0) for i in range(1000)]  # Excitatory. 
b = [Axon(0.1, -70) for i in range(200)] # Inhibitory. 
a = a + b

# assign latency to synapses (gaussian: mean 0, std. derivation 15ms)
a_latencies = [int(i) for i in rand.normal(0, 15, len(a))]

# generate spike bursts for axons
a_spike_map = [[] for i in a]
spike_prob = BURST_FREQ * DELTA_T
for i in range(int(SIM_DURATION / EVENT_PERIOD)):
    t = i * EVENT_PERIOD
    for j in range(len(a)):
        for k in range(int(BURST_DURATION / (DELTA_T * 1000))):
            if rand.random() < spike_prob:
                a_spike_map[j].append(t + k + a_latencies[0])

# plot spike events
# plt.figure()
# t_values = range(SIM_DURATION)
# for i in range(len(a)):
#     plt.plot(t_values, [i+.5 if t in a_spike_map[i] else 0 for t in t_values], '.')
# plt.show()

# creating a dendrite to which the axons before are attached.
dendrite = Dendrite(a)

# Run the loop: 
t = 0
g = [[] for axon in a]
steps = int(SIM_DURATION / DELTA_T)
for tt in range(steps):
    t += tt * DELTA_T

    # Update status: 
    for i in range(len(a)):
        a[i].updateStatus(tt)
        g[i] += [a[i].g]
    dendrite.updateStatus()

t = 0
g = [[] for axon in a]
steps = int(SIM_DURATION / DELTA_T)
for tt in range(steps):
    t += tt * DELTA_T

    # Update status: 
    for i in range(len(a)):
        a[i].updateStatus(tt)
        g[i] += [a[i].g]
    dendrite.updateStatus()

    #Storing variables to be plotted: 
#    V = V + [dendrite1.V]
#    M = M + [dendrite1.M]
#    P0 = P0 + [a[0].P]
#    g_boost0 = g_boost0 + [a[0].g_boost]
