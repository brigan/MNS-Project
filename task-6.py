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
SIM_DURATION           = 80    # ms
DELTA_T                = 0.5   # ms
STEADY_STATE_THRESHOLD = 5e-6

# pre-synaptic events occur every EVENT_PERIOD
EVENT_PERIOD   = 100   # ms
EVENT_ONSET    = 30    # ms (shift all events)

# parameters for single spike burst
BURST_DURATION = 20    # ms
BURST_FREQ     = 100   # Hz

# number of axons
EXC_NUM        = 120
INH_NUM        = 20

def plot_g_over_latencies(axons, latencies):
    """Plots g_peak/g_max over the axon's latencies."""
    plt.figure()
    plt.xlabel('Relative latency [ms]')
    plt.ylabel('g_peak/g_max')
    r_ = range(min(latencies), max(latencies) + 1)
    r  = []
    v  = []
    for i in range(len(r_)):
        num = 0
        g_peak_sum = 0.
        g_max_sum = 0.
        for j in range(len(axons)):
            if latencies[j] == r_[i]:
                num += 1
                g_peak_sum += axons[j].g_boost
                g_max_sum += axons[j].g_max
        if num != 0:
            g_peak_over_g_max = (g_peak_sum / num) / (g_max_sum / num)
            r.append(r_[i])
            v.append(g_peak_over_g_max)
    plt.plot(r, v, '.')

# assign latency to synapses (gaussian: mean 0, std. derivation 15ms)
total_axons = EXC_NUM + INH_NUM
a_latencies = [int(i) for i in rand.normal(0, 15, total_axons)]

# generate spike bursts for axons
steps = int(SIM_DURATION / DELTA_T)
a_spike_map = [[] for i in range(total_axons)]
spike_prob = BURST_FREQ * DELTA_T / 1000.

for i in range(SIM_DURATION / EVENT_PERIOD + 1): # every event
    t = i * EVENT_PERIOD
    for j in range(total_axons): # for every axon
        for k in range(int(BURST_DURATION / DELTA_T)): # for burst duration
            if rand.random() < spike_prob:
                a_spike_map[j].append(t + EVENT_ONSET / DELTA_T + k + a_latencies[j])

# create axons + dentrite
# excitatory
exc = [Axon(0.1, 0, g_boost=0.004, g_max=0.02, spike_map=a_spike_map.pop()) \
           for i in range(EXC_NUM)]
# inhibitory
inh = [Axon(0.1, -70, g_boost=0.004, g_max=0.02, spike_map=a_spike_map.pop()) \
           for i in range(INH_NUM)]
a = exc + inh
dendrite = Dendrite(a)

# plot g over latencies before simulation
plot_g_over_latencies(a, a_latencies)

# Run the simulation
g       = [[] for axon in a]
time    = []
V_first = []
V       = []
spikes  = []

steady_state = False
g_peak_over_g_max_prev = [axon.g_boost / axon.g_max for axon in a]
j = 0
while True:
    # set decaying values to 0 (equals waiting for long time without
    # post-synaptic spikes)
    dendrite.M = 0.
    dendrite.V = 0.
    for axon in a:
        axon.g = 0.
        axon.P = 0.

    V = []
    for tt in range(steps):
        # update status
        for i in range(len(a)):
            a[i].updateStatus(tt)
            g[i] += [a[i].g]
        dendrite.updateStatus()

        # storing variables to be plotted
        if j == 0:
            V_first.append(dendrite.V)
            time.append(tt * DELTA_T)
            spiking = 0
            for axon in a:
                if axon.spike:
                    spiking = 1
                    break
            spikes.append(spiking)
            V = V_first
        else:
            V.append(dendrite.V)

    # check if steady state reached
    one_changed = False
    for i in range(len(a)):
        if abs(a[i].g_boost / a[i].g_max - g_peak_over_g_max_prev[i]) > STEADY_STATE_THRESHOLD:
            one_changed = True
            break
    if one_changed == False:
        break
    g_peak_over_g_max_prev = [axon.g_boost / axon.g_max for axon in a]
    j += 1

print "cycles: ", j

# plot g over latencies after simulation
plot_g_over_latencies(a, a_latencies)

# plot axon's voltage over time
plt.figure()
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [mV]')
plt.plot(time, spikes, 'r.')
plt.plot(time, V_first, label='Voltage of postsynaptic dendrite (first run)')
plt.plot(time, V, label='Voltage of postsynaptic dendrite (last run)')
plt.legend()

plt.show()
