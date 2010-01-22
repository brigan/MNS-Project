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
##                 Euler function.
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
##                 Exponential function.
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
##                 Dendrite class.
##    

class Dendrite:
    """Dendrite of an integrate-and-fire neuron:
   
        A dendrite, as we define it here, receives inputs from many presynaptic axons and sums up their contributions. If a threshold is reached, it should generate an action potential.
    """
   
   
    #########################################################
    ## __init__:
   
    def __init__(self, arrayAxons, V_rest=-70, tau=20, V_threshold=-54, V_peak=60, V_reset=-60, 
                 Aminus=0.00525, tauMinus=20):
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
        self.V_thr = V_threshold
        self.V_peak = V_peak
        self.V_reset = V_reset
        self.Aminus = Aminus
        self.tauMinus = tauMinus
       
        # Some aditional parameters of objects of class Axon which are not explicitly given but set here:
        
        self.V = V_rest
        self.spike = False
        self.M = 0
        
        # When initialized, info is given to the presynaptic axons of which dendrite they are being attached to: 
        
        for axon in self.inAxons:
            axon.outDendrite = self


    #########################################################
    ## updateStatus:
    
    def updateStatus(self):
        """updateStatus function: 
        
        	This function updates the status of objects of the class 'dendrite' by updating each of its important features. 
        
        """
        
        self.updateResting_value()
        self.updateV()
        self.updateM()
       
    
    #########################################################
    ## updateV:
   
    def updateV(self):
        """updateV function:
       
            This function updates the voltage using the integrate-and-fire model. 
            
            Since in this function is calculated whether the postsynaptic dendrite fires or not, this function also elicits those actions which are explicitly triggered by action potentials in postsynaptic dendrites. Thus, if a spike happens, this function calls the 'getReward()' function for each excitatory axon. 
            
        """
        
        if self.spike:
            self.V = self.V_reset
            for axon in self.inAxons:
                if axon.E == 0:
                    axon.getReward()
            self.spike = False
        else:
            if self.V < self.V_thr: 
                self.V = euler(exponentialDecay, self.V, [self.tau,self.resting_value])
            else: 
                self.V = self.V_peak
                self.spike = True
                
            
   
   
    #########################################################
    ## updateResting_value:
    
    def updateResting_value(self):
        """updateResting_value function:
       
            This functions update the resting value of the dendrite to which its voltage decays within the paradigm of integrate-and-fire neurons. This value depends on the current injected from all the presynaptic axons.
            
        """
       
        sum = 0
        for axon in self.inAxons:
            sum = sum + axon.g*(axon.E-self.V)
           
        self.resting_value = self.V_rest + sum
        
        
    #########################################################
    ## updateM:
    
    def updateM(self): 
        """updateM function: 
        
        	This function updates the penalization that each and every presynaptic axon gets when fired out of time. Since the penalization is common to all the axons which are presynaptic to the same dendrite, 'M' is a function of the dendrite. 
        
        """
        
        if self.spike: 
            self.M = self.M - self.Aminus
        else:
            self.M = euler(exponentialDecay, self.M, [self.tauMinus,0])
   
   
   
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
## 
##                 Axon class.
##    

class Axon:
    """Presynaptic axon:
   
        Objects of the class Axon have an internal current which they inject into the postsynaptic neuron if a connection is stablished. It is done by means of the conductivity 'self.g' of the axon which is modified after next rules:
            self.g(t) --> self.g(t) + g_Increase         ==> If an action potential arrives to 'self'.
            exponential decay of self.g(t) to zero otherwise.
            
        Axons might be inhibitory or excitatory. This is stated through the internal variables 'self.E' and 'self.g_Increase', passed to the object when it is created and thus defining its function.
    """
   
   
   
    #########################################################
    ## __init__:
   
    def __init__(self, p_spike, E, g_boost=0.015, g_max=0.015, g_min=0, tau=5, Aplus=0.005, 
                 tauPlus=20, outDendrite=None):
        """__init__ function of the Axon class:
       
           Sets many initial values for the axon, which determine its behavior.
          
           Arguments:
           ==> E: resting potential for this axon. Together with 'g_boost' determines whether the axon is excitatory or inhibitory.
           ==> g_boost: boost to the connectivity 'g' when an action potential arrives the axon.
           ==> p_spike: probability of 'self' to spike.
        """
        
        self.p_spike = p_spike
        self.E = E
        self.g = 0
        self.g_max = g_max
        self.g_min = g_min
        self.g_boost = g_boost
        self.tau = tau
        self.Aplus = Aplus
        self.tauPlus = tauPlus
        self.outDendrite = outDendrite
        
        # Some aditional parameters of objects of class Axon which are not explicitly given but set here:
        
        self.spike = False
        self.P = 0
       
   
    #########################################################
    ## updateG:
       
    def updateG(self):
        """UpdateG function:
       
            This method updates the connectivity of the axon by increasing it a quantity 'g_boost' if an action potential arrives to 'solf' and by letting it decay exponentially otherwise.
            
        """
        
        self.spike = False
        if rand.random() < self.p_spike:
            self.spike = True
            self.g = self.g + self.g_boost
            if self.E == 0:
                self.getPenalization()
           
        self.g = euler(exponentialDecay, self.g, [self.tau,0])
        self.updateP()


    #########################################################
    ## updateP:
    
    def updateP(self):
        """updateP function: 
        
        	This method updates the 'P' function which encodes the reward each presynaptic connection recives if the postsynaptic dendrite fires at the proper time after 'self' did. Since the reward each presynaptic axon gets deppends on the time it fires, 'P' belongs to each presynaptic axon and not to the postsynaptic dendrite as 'M' does. 
        
        """
        
        if self.spike: 
            self.P = self.P + self.Aplus
        else:
            self.P = euler(exponentialDecay, self.P, [self.tauPlus,0])


    #########################################################
    ## getReward:
    
    def getReward(self):
        """getReward function: 
        
        	This method gives the presynaptic axon a reward which deppends on how synchronized were its spike and the dendrite's. 
        
        """
        
        self.g_boost = self.g_boost + self.P*self.g_max
        if self.g_boost > self.g_max:
            self.g_boost = self.g_max

    #########################################################
    ## getPenalization:
    
    def getPenalization(self): 
        """getPenalization function: 
        
        	This method gives the presynaptic axon a penalization which deppends on how synchronized were its spike and the dendrite's. 
        	
        	'M', which is a cornerstone of the penalization process, is a function stored in 'self.outDendrite'. 
        
        """
        
        self.g_boost = self.g_boost + self.outDendrite.M*self.g_max
        if self.g_boost < self.g_min:
            self.g_boost = self.g_min
        



a = [Axon(0.1,0) for i in range(5)]
b = [Axon(0.1,-70) for i in range(5)]
a = a+b
dendrite1 = Dendrite(a)
DeltaT = 0.001
t = []
V = []
M = []
P0 = []
g_boost0 = []
g = [[] for axon in a]
for tt in range(1000):
    t = t + [tt*DeltaT]
    for ii in range(len(a)):
        a[ii].updateG()
        g[ii] = g[ii] + [a[ii].g]
    dendrite1.updateStatus()
    V = V + [dendrite1.V]
    M = M + [dendrite1.M]
    P0 = P0 + [a[0].P]
    g_boost0 = g_boost0 + [a[0].g_boost]
    
plt.figure()
plt.title('Spikes')
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
for ll in g:
    plt.plot(t,ll)
plt.show()

plt.figure()
plt.title('Spikes of presynaptic axon [0]')
plt.subplot(2,1,1)
plt.xlabel('Time [s]')
plt.ylabel('Conductivity [S]')
plt.plot(t,g[0])
plt.subplot(2,1,2)
plt.xlabel('Time [s]')
plt.ylabel('P [#]')
plt.plot(t,P0)
plt.show()

plt.figure()
plt.subplot(2,1,1)
plt.xlabel('Time [s]')
plt.ylabel('Voltage [mV]')
plt.plot(t,V)
plt.subplot(2,1,2)
plt.xlabel('Time [s]')
plt.ylabel('M [#]')
plt.plot(t,M)
plt.show()

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









