"""Project task 5: For the initial excitatory peak conductances take g_exc = g_max . Simulate the 
model with N = 1000 excitatory and M = 200 inhibitory synapses both of 
which receive independent Poisson spike trains (10 Hz for inhibitory, 10 – 40 Hz 
for excitatory). Plot the ﬁnal weight distribution for diﬀerent excitatory ﬁring 
rates. Plot the output ﬁring rate and coeﬃcient of variation as a function of the 
input ﬁring rate. 

"""

import random as rand
import pylab as plt
from neuron import *