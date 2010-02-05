

import numpy as np
import random as rand
import pylab as plt
from neuron import *

# Preparing some parameters of the experiment: 
# 	==> nExc: number of excitatory connections. 
# 	==> nInh: number of inhibitory connections. 
# 	==> fInh: frequency of inhibitory connections. 
# 	==> rangeExc: range of excitatory connections. Frequency of each single excitatory connection is to be drawn from here. 
# 	==> deltaT: time step of the simulation. 
# 		--> pInh = fInh*deltaT. 
# 		--> range_pExc = rangeExc*deltaT: range of probabilities for excitatory connections. 
# 			>>> pExc: list storing the probability of each excitatory connection to be built. 
# 	==> listConnections: list with objects of the class 'Axon'. Both excitatory and inhibitory are stored in the same list. 

nExc = 1000
nInh = 200
fInh = 10
rangeExc = np.arange(0.01,0.04,0.005) 	# Unitites = [ms]
deltaT = 0.005
pInh = fInh*deltaT
pExc = [elem*deltaT for elem in rangeExc]
gg = 0.015

listInh = [Axon(p_spike=pInh, E=-70, g_boost=0.05) for ii in range(nInh)]
listsExc = [[Axon(p, E=0, g_boost=gg, g_max=gg) for ii in range(nExc)] for p in pExc]
dendrite = [Dendrite(listInh+axonList) for axonList in listsExc]


# Variables to plot: 
t = 0
time = [[] for ii in range(len(dendrite))]
V = [[] for ii in range(len(dendrite))]

# Run the loop: 
while True: 
    for ii in range(len(dendrite)):
        t = t + 1
        time[ii] = time[ii] + [t*deltaT]
    
        for axon in listInh:
            axon.updateStatus(t*deltaT)
        for axon in listsExc[ii]:
            axon.updateStatus(t*deltaT)
        dendrite[ii].updateStatus()
    
        #Store Variables:
        V[ii] = V[ii] + [dendrite[ii].V]
#        g = g + [listAxon[0].g]
    
    if t*deltaT > 20:
        break
   
g = [[] for axonList in listsExc]
for ii in range(len(listsExc)):
    for axon in listsExc[ii]:
        g[ii] = g[ii] + [axon.g/gg]


 
    
plt.figure()
#plt.subplot(2,1,1)
for ii in range(len(V)):
    plt.plot(time[ii],V[ii]) 
#plt.subplot(2,1,1)
#for ggg in g:
#    plt.plot(ggg)
plt.show() 

plt.figure()
for ggg in g:
    plt.hist(ggg,20)
plt.show()











