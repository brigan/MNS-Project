

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

stopThres = 0.01
nExc = 1000
nInh = 200
fInh = 0.1
rangeExc = np.arange(0.01,0.04,0.005) 	# Unitites = [ms]
						# Eiji fExc = 0.04
deltaT = 0.1
pInh = fInh*deltaT
pExc = [elem*deltaT for elem in rangeExc]
						# Eiji pExc = fExc*deltaT
gg = 0.015

listInh = [Axon(p_spike=pInh, E=-70, g_boost=0.05) for ii in range(nInh)]
listsExc = [[Axon(p, E=0, g_boost=gg, g_max=gg) for ii in range(nExc)] for p in pExc]
						# Eiji listExc = [Axon(p_spike=pExc, E=0, g_boost=gg, g_max=gg) for ii in range(nExc)]
dendrite = [Dendrite(listInh+axonList) for axonList in listsExc]
						# Eiji dendrite = Dendrite(listInh+listExc)	


# Variables to plot: 
t = 0
n = 0
time = []
V = [[] for ii in range(len(dendrite))]
bufferG = bufferG = [[0 for axon in axonList] for axonList in listsExc]
spikeCount = [0 for dd in dendrite]

# Run the loop: 
flagEnd = False
while True: 
    print t
    t = t + 1
    n = n + 1
    time = time + [t*deltaT]
    for axon in listInh:
        axon.updateStatus(deltaT)

    for ii in range(len(dendrite)):        
        for jj in range(len(listsExc[ii])):
            listsExc[ii][jj].updateStatus(deltaT)
        dendrite[ii].updateStatus()
        if dendrite[ii].spike:
            spikeCount[ii] = spikeCount[ii] + 1
    
        V[ii] = V[ii] + [dendrite[ii].V]
     
#    if n is 100: 
#        n=0
#        flagEnd = True
#        for ii in range(len(listExc)): 
#            if abs(bufferG[ii]-listExc[ii].g) > stopThres:
#                flagEnd = False
#                print ii, abs(bufferG[ii]-listExc[ii].g)
#                break
#        for ii in range(len(listExc)): 
#            bufferG[ii] = listExc[ii].g
#    if flagEnd:
#        break

    if t*deltaT > 100: 					# (t*deltaT > 10 and flagEnd) or
        break

# Calculating 'a posteriori' variables to be plotted: 
fr = [0 for den in dendrite]
for ii in range(len(dendrite)):
    fr[ii] = spikeCount[ii]/(t*deltaT)
    
plt.figure()
plt.plot(rangeExc,fr,'*-')
plt.show()

g = [[] for axonList in listsExc]
						# Eiji for axon in listExc:
						# Eiji    g = g + [axon.g_boost/axon.g_max]
for ii in range(len(listsExc)):
    for axon in listsExc[ii]:
        g[ii] = g[ii] + [axon.g_boost/gg]


# Some histograms: 
plt.figure()
# for ggg in g:
plt.hist(g[0],20)
plt.hist(g[-1],20)


# Firing rate: 
# Eiji plt.figure()
# Eiji plt.plot(rangeExc,fr,'*-')



plt.show()











