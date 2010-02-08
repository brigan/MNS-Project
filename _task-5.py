

import numpy as np
import random as rand
import pylab as plt
from neuron import *


# Function to plot: 

def plotDist(time,listExc): 
    print 'Hallo'
    g = []
    for axon in listExc:
        g = g + [axon.g_boost/axon.g_max]
        
    title = 'Time = '+str(time)+'ms'
    plt.figure()
    plt.title(title)
    plt.xlabel('g/g_max')
    plt.ylabel('Number of connections')
    plt.hist(g,20)
    plt.show()
    



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
fInh = 0.01
	# Eiji rangeExc = [0.04] #np.arange(0.01,0.04,0.005) 	# Unitites = [ms]
fExc = 0.01
deltaT = 0.1
pInh = fInh*deltaT
	# Eiji pExc = [elem*deltaT for elem in rangeExc]
pExc = fExc*deltaT
gg = 0.015

listInh = [Axon(p_spike=pInh, E=-70, g_boost=0.05) for ii in range(nInh)]
	# Eiji listsExc = [[Axon(p, E=0, g_boost=gg, g_max=gg) for ii in range(nExc)] for p in pExc]
listExc = [Axon(p_spike=pExc, E=0, g_boost=gg, g_max=gg) for ii in range(nExc)]
dendrite = Dendrite(listInh+listExc)	# Eiji [Dendrite(listInh+axonList) for axonList in listsExc]


# Variables to plot: 
t = 0
n = 0
time = []				# Eiji [[] for ii in range(len(dendrite))]
V = []					# Eiji [[] for ii in range(len(dendrite))]
bufferG = [10 for axon in listExc]						# Eiji bufferG = [[0 for axon in axonList] for axonList in listsExc]
spikeCount = 0 			# Eiji [0 for dd in dendrite]

# Run the loop: 
flagEnd = False
while True: 
    t = t + 1
    n = n + 1
    time = time + [t*deltaT] 
						# Eiji    for ii in range(len(dendrite)):        
						# Eiji        time[ii] = time[ii] + [t*deltaT]
						
    for axon in listInh:
        axon.updateStatus(deltaT)
						# Eiji    for jj in range(len(listsExc[ii])):
						# Eiji            listsExc[ii][jj].updateStatus(t*deltaT)
    for axon in listExc: 
        axon.updateStatus(deltaT)
    dendrite.updateStatus()
    if dendrite.spike:
        spikeCount = spikeCount + 1
						# Eiji        dendrite[ii].updateStatus()
						# Eiji        if dendrite[ii].spike:
						# Eiji            spikeCount[ii] = spikeCount[ii] + 1
    
    #Store Variables:
    V = V + [dendrite.V]
						# Eiji        V[ii] = V[ii] + [dendrite[ii].V]
     
    if n == 10000: 
        n=0
        g = []
        for axon in listExc:
            g = g + [axon.g_boost/axon.g_max]
        
        title = 'Time = '+str(t*deltaT)+'ms'
        plt.figure()
        plt.title(title)
        plt.xlabel('g/g_max')
        plt.ylabel('Number of connections')
        plt.hist(g,20)
        plt.show()
        flagEnd = True
        for ii in range(len(listExc)): 
            if abs(bufferG[ii]-listExc[ii].g) > stopThres:
                flagEnd = False
                print ii, abs(bufferG[ii]-listExc[ii].g)
                break
        for ii in range(len(listExc)): 
            bufferG[ii] = listExc[ii].g
    if flagEnd:
        break

#    if t*deltaT > 10000: 					# (t*deltaT > 10 and flagEnd) or
#        break

# Calculating 'a posteriori' variables to be plotted: 
fr = spikeCount/(t*deltaT)
print fr
						# Eiji fr = [0 for den in dendrite]
						# Eiji for ii in range(len(dendrite)):
						# Eiji     fr[ii] = spikeCount[ii]/(t*deltaT)

						# Eiji g = [[] for axonList in listsExc]
g = []
for axon in listExc:
    g = g + [axon.g_boost/axon.g_max]
						# Eiji     for axon in listsExc[ii]:
						# Eiji         g[ii] = g[ii] + [axon.g_boost/gg]


# Some histograms: 
plt.figure()
# for ggg in g:
plt.title('10 ms')
plt.xlabel('')
plt.hist(g,20)


# Firing rate: 
# Eiji plt.figure()
# Eiji plt.plot(rangeExc,fr,'*-')



plt.show()











