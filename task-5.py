

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
fInh = 0.01
rangeExc = [0.01] #np.arange(0.01,0.04,0.005) 	# Unitites = [ms]
deltaT = 1
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
bufferG = [[0 for axon in axonList] for axonList in listsExc]
spikeCount = [0 for dd in dendrite]

# Run the loop: 
while True: 
    print t
    t = t + 1
    for ii in range(len(dendrite)):
        
        time[ii] = time[ii] + [t*deltaT]
    
        for axon in listInh:
            axon.updateStatus(t)
        for jj in range(len(listsExc[ii])):
            bufferG[ii][jj] = listsExc[ii][jj].g
            listsExc[ii][jj].updateStatus(t*deltaT)
        dendrite[ii].updateStatus()
        if dendrite[ii].spike:
            spikeCount[ii] = spikeCount[ii] + 1
    
        #Store Variables:
        V[ii] = V[ii] + [dendrite[ii].V]
           
#    flagEnd = True
#    for ii in range(len(listsExc)): 
#        r = 0
#        for jj in range(len(listsExc[ii])): 
#            r = r + np.sqrt((bufferG[ii][jj]-listsExc[ii][jj].g)**2)
#        if r > 0.1:
#            flagEnd = False
#            break
    if t*deltaT > 100000: 					# (t*deltaT > 10 and flagEnd) or
        break

# Calculating 'a posteriori' variables to be plotted: 
fr = [0 for den in dendrite]
for ii in range(len(dendrite)):
    fr[ii] = spikeCount[ii]/(t*deltaT)

g = [[] for axonList in listsExc]
for ii in range(len(listsExc)):
    for axon in listsExc[ii]:
        g[ii] = g[ii] + [axon.g_boost/gg]


# Some histograms: 
plt.figure()
# for ggg in g:
plt.hist(g[0],20)

plt.figure()
plt.hist(g[-1],20)


# Firing rate: 
plt.figure()
plt.plot(rangeExc,fr,'*-')



plt.show()











