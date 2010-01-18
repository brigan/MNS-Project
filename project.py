"""A neuron model that generates action potentials (based upon
Competitive Hebbian learning through spike-timing-dependent
synaptic plasticity; Song, Miller, Abbott, Nature Neuroscience
2000).
"""

import numpy as np
import pylab as plt
import random as rand


################################################################################
##
## 				Euler function.
##

def euler(function, x0, param, DeltaT=0.001):
    """General Euler method:
  
    This method integrates through the Euler method.
    	
    	Arguments:
    		==> function: time derivative we want to integrate.
    		==> x0: initial value of the integrand.
    		==> param: parameters for 'function'.
    		==> DeltaT: time step.
    """
    DeltaX = function(x0,param)*DeltaT
    return x0 + DeltaX
   
################################################################################
## 
## 				Exponential function.
##    

def exponentialDecay(x,param):
    """General exponential function:
   
    	This function reproduces an exponential decay when integrated.
    	
    	Arguments:
    		==> x: current value of the variable.
    		==> param: list of parameters. In this case: [tau,resting_value].
    """
    tau = param[0]
    resting_value = param[1]
    return -(x-resting_value)*tau





##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
## 
## 				Dendrite class.
##    

class Dendrite:
    """Dendrite of an integrate-and-fire neuron:
   
    	A dendrite, as we define it here, receives inputs from many presynaptic axons and sums up their contributions. If a threshold is reached, it should generate an action potential.
    """
   
   
    #########################################################
    ## __init__:
   
    def __init__(self, arrayAxons, V_rest=-70, tau=20, V_Threshold=-54):
        """__init__ function for the class Dendrite:
       
        	This function initializes the objects of class Dendrite.
        	
        	Arguments:
        	==> arrayAxons: array of incoming axons.
        	==> V_rest: Resting voltage of the dendrite.
        	==> tau: proper time for the integrate-and-fire procces.
        	==> V_Threshold: Threshold potential which would fire an action potential.
        """
       
        self.inAxons = arrayAxons
        self.V_rest = V_rest
        self.tau = tau
        self.V_Thr = V_Threshold
       
        # Some aditional parameters of objects of class Axon which are not explicitly given but set here:
       
        self.resting_value = V_rest
        self.V = V_rest
       
    
    #########################################################
    ## updateV:
   
    def updateV(self):
        """updateV function:
       
        	This function updates the voltage using the integrate-and-fire model.
        """
       
        for axon in self.inAxons:
            axon.updateG()
        self.resting_value = self.updateResting_value()
        self.V = euler(exponentialDecay, self.V, [self.tau,self.resting_value])
   
   
    #########################################################
    ## updateResting_value:
   
    def updateResting_value(self):
        """updateResting_value function:
       
        	This functions update the resting value of the dendrite to which its voltage decays within the paradigm of integrate-and-fire neurons. This value depends on the current injected from all the presynaptic axons.
        """
       
        sum = 0
        for axon in self.inAxons:
            sum = sum + axon.g*(axon.E-self.V)
           
        return self.V_rest + sum
   
   
   
   
   
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
## 
## 				Axon class.
##    

class Axon:
    """Presynaptic axon:
   
    	Objects of the class Axon have an internal current which they inject into the postsynaptic neuron if a connection is stablished. It is done by means of the conductivity 'self.g' of the axon which is modified after next rules:
    		self.g(t) --> self.g(t) + g_Increase 		==> If an action potential arrives to 'self'.
    		exponential decay of self.g(t) to zero otherwise.
    		
    	Axons might be inhibitory or excitatory. This is stated through the internal variables 'self.E' and 'self.g_Increase', passed to the object when it is created and thus defining its function.
    """
   
   
   
    #########################################################
    ## __init__:
   
    def __init__(self, E, g_boost, p_spike, tau=5):
        """__init__ function of the Axon class:
       
	       Sets many initial values for the axon, which determine its behavior.
	      
	       Arguments:
	       ==> E: resting potential for this axon. Together with 'g_boost' determines whether the axon is excitatory or inhibitory.
	       ==> g_boost: boost to the connectivity 'g' when an action potential arrives the axon.
	       ==> p_spike: probability of 'self' to spike.
        """
        self.g = 0
        self.E = E
        self.g_boost = g_boost
        self.p_spike = p_spike
        self.tau = tau
       
   
    #########################################################
    ## updateG:
       
    def updateG(self):
        """UpdateG function:
       
        	This method updates the connectivity of the axon by increasing it a quantity 'g_boost' if an action potential arrives to 'solf' and by letting it decay exponentially otherwise.
        """
        if rand.random() < self.p_spike:
            self.g = self.g + self.g_boost
           
        self.g = euler(exponentialDecay, self.g, [self.tau,0])





import numpy as np
import pylab as plt

a = [Axon(0,1,0.001) for i in range(5)]
b = [Axon(-70,1,0.001) for i in range(5)]
a = a+b
DeltaT = 0.001
t = []
g = []
for tt in range(10000):
    t = t + [tt*DeltaT]
    a[0].updateG()
    g = g + [a[0].g]
   
plt.figure()
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
plt.plot(t,g)
plt.show()
