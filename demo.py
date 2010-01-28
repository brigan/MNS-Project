"""Script to show the neuron module's functionality."""

import pylab as plt
from neuron import *

# Creating an array of Axon ready to be attached to an object of class
# Dendrite:
a = [Axon(0.1, 0) for i in range(5)]    # Excitatory. 
b = [Axon(0.1, -70) for i in range(5)]  # Inhibitory. 
a = a+b

# Creating a Dendrite to which the Axons before are attached.
dendrite1 = Dendrite(a)

# Creating variables to run a loop and store info to be plotted later.
DeltaT = 0.001
t = []
V = []
M = []
P0 = []
g_boost0 = []
g = [[] for axon in a]

# Run the loop: 
for tt in range(1000):
    t = t + [tt*DeltaT]
    
    # Update status: 
    for ii in range(len(a)):
        a[ii].updateStatus()
        g[ii] = g[ii] + [a[ii].g]
    dendrite1.updateStatus()
    
    #Storing variables to be plotted: 
    V = V + [dendrite1.V]
    M = M + [dendrite1.M]
    P0 = P0 + [a[0].P]
    g_boost0 = g_boost0 + [a[0].g_boost]


# Figure 1: spikes of all presynaptic axons:
plt.figure()
plt.title('Spikes of presynaptic axos')
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
for ll in g:
    plt.plot(t,ll)
plt.show()

# Figure 2: evolution of the potential reward 'P' when a presynaptic
# axon spikes.
plt.figure()
plt.subplot(2,1,1)
plt.title('Spikes of presynaptic axon[0]')
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
plt.plot(t,g[0])
plt.subplot(2,1,2)
plt.title('Potential reward of axon[0]')
plt.xlabel('Time [s]')
plt.ylabel('P [#]')
plt.plot(t,P0)
plt.show()


# Figure 3: evolution of the potential penalization 'M' when a
# postsynaptic dendrite spikes.
plt.figure()
plt.subplot(2,1,1)
plt.title('Voltage of postsynaptic dendrite')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [mV]')
plt.plot(t,V)
plt.subplot(2,1,2)
plt.title('Potential penalization for all axons')
plt.xlabel('Time [s]')
plt.ylabel('M [#]')
plt.plot(t,M)
plt.show()


# Figure 4: acquisition of reward of penalization. 
plt.figure()
plt.subplot(3,1,1)
plt.title('Spikes of dendrite')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [mV]')
plt.plot(t,V)
plt.subplot(3,1,2)
plt.title('Spikes of axon[0]')
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
plt.plot(t,g[0])
plt.subplot(3,1,3)
plt.title('Modification of g_boost')
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
plt.plot(t,g_boost0)
plt.show()
