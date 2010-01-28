"""A neuron model that generates action potentials (based upon
Competitive Hebbian learning through spike-timing-dependent
synaptic plasticity; Song, Miller, Abbott, Nature Neuroscience
2000).
"""

import numpy.random as rand
from helper import *

###############################################################################
##
##                 Dendrite class.
##
class Dendrite:
    """Dendrite of an integrate-and-fire neuron:

    A dendrite, as we define it here, receives inputs from many
    presynaptic axons and sums up their contributions. If a threshold
    is reached, it should generate an action potential.

    Variables:
    ==> self: object of the class Dendrite.
    ==> V: potential of 'self'.
    ==> spike: boolean: True ==> spike, False ==> no spike.
    ==> inAxons: array of objects of the class Axon. These 'Axons' are attached to 'self' and interact after the corresponding model.
    ==> V_rest: value towards the potential of 'self' decays when no imput current comes from Axons in 'inAxon'.
    ==> tau: eigentime of the decay of V.
    ==> V_thr: when V>V_thr, 'self' fires an action potential increasing its voltage and triggering the rewarding of those Axons from 'inAxon' which provoked the spike.
    ==> V_peak: potential to which the voltage is set during spiking.
    ==> V_reset: potential to which the voltage is set after spiking.
    ==> M: potential penalization that presynaptic axons spiking out of time might get.
    ==> A_minus: increase of 'M' each time 'self' fires.
    ==> tau_minus: eigentime of the decay of the penalization.

    Methods:
    ==> __init__: __init__ function for objects of class Dendrite.
    ==> updateStatus: updates all the variables enclosed in objects of class Dendrite using the corresponding methods.
    ==> updateV: updates the voltage of objects of the class Dendrite afther the corresponding model and elicits any further action if necessary.
    ==> updateResting_value: updates the value to which the voltage tends at each time.
    ==> updateM: updates the function which controls the penalizations.
    """

    #########################################################
    ##
    ## __init__:
    def __init__(self, arrayAxons, V_rest=-70, tau=20, V_thr=-54, V_peak=60, V_reset=-60,
                 A_minus=0.00525, tauMinus=20):
        """__init__ function for the class Dendrite:

        This function initializes the objects of class Dendrite.

        Arguments:
        ==> self: object of the class Dendrite.
        ==> inAxons: array of objects of the class Axon. These 'Axons' are attached to 'self' and interact after the corresponding model.
        ==> V_rest: value towards the potential of 'self' decays when no imput current comes from Axons in 'inAxon'.
        ==> tau: eigentime of the decay of V.
        ==> V_thr: when V>V_thr, 'self' fires an action potential increasing its voltage and triggering the rewarding of those Axons from 'inAxon' which provoked the spike.
        ==> V_peak: potential to which the voltage is set during spiking.
        ==> V_reset: potential to which the voltage is set after spiking.
        ==> A_minus: increase of 'M' each time 'self' fires.
        ==> tau_minus: eigentime of the decay of the penalization.
        """
        self.inAxons = arrayAxons
        self.V_rest = V_rest
        self.tau = tau
        self.V_thr = V_thr
        self.V_peak = V_peak
        self.V_reset = V_reset
        self.A_minus = A_minus
        self.tauMinus = tauMinus

        # Some aditional parameters of objects of class Axon which are
        # not explicitly given but set here:
        self.V = V_rest
        self.spike = False
        self.M = 0
       
        # When initialized, info is given to the presynaptic axons of
        # which dendrite they are being attached to:
        for axon in self.inAxons:
            axon.outDendrite = self

    #########################################################
    ## updateStatus:
    def updateStatus(self):
        """updateStatus function:

          This function updates the status of objects of the class
          Dendrite by updating each of its important features.
        """
        self.updateResting_value()
        self.updateV()
        self.updateM()

    #########################################################
    ## updateV:

    def updateV(self):
        """updateV function:

            This function updates the voltage using the
            integrate-and-fire model.

            Since in this function is calculated whether the
            postsynaptic dendrite fires or not, this function also
            elicits those actions which are explicitly triggered by
            action potentials happening in postsynaptic
            dendrites. Thus, if a spike happens, this function calls
            the 'getReward()' function for each excitatory axon
            attached to 'self'.
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

            In the integrate-and-fire model, the voltage of a neuron
            behaves as an exponential decay whose resting value
            depends on many variables and parameters of the
            presynaptic connections. This function gets these
            variables and parameters at each time and calculate to
            which value is the voltage of the postsynaptice dendrite
            decaying. This value towards the voltage decays is stored
            in the variable 'resting_value' of an object of class
            Dendrite.
        """
        sum = 0
        for axon in self.inAxons:
            sum = sum + axon.g*(axon.E-self.V)

        self.resting_value = self.V_rest + sum

    #########################################################
    ## updateM:
    def updateM(self):
        """updateM function:

          This function updates the potential penalization that each
          and every presynaptic axon gets when fired out of
          time. Since the penalization is the same for all the axons
          which are presynaptic to the same dendrite, 'M' is a
          function of the dendrite.
        """
        if self.spike:
            self.M = self.M - self.A_minus
        else:
            self.M = euler(exponentialDecay, self.M, [self.tauMinus,0])

###############################################################################
##
##                 Axon class.
##   
class Axon:
    """Presynaptic axon:

        Objects of the class Axon have an internal current which they
        inject into the postsynaptic neuron if a connection is
        stablished. It is done by means of the conductivity 'self.g'
        of the axon which is modified after next rules:

        self.g(t) --> self.g(t) + g_Increase ==> If an action potential arrives to 'self'.
        exponential decay of self.g(t) to zero otherwise.

        Axons might be inhibitory or excitatory. This is stated
        through the internal variables 'self.E' and 'self.g_Increase',
        passed to the object when it is created and thus defining its
        function. I finally decided not to create an special class for
        inhibitory synapses since the behavior is not so
        different. The only point is not to reward or penalize
        inhibitory synapses, which is easily done: 'if self.E==0
        --excitatory-- : penalize or reward; otherwise: do not!'.

    Variables:
      ==> self: object of the class Axon.
      ==> outDendrite: object of the class Dendrite to which 'self' is attached.
      ==> g: conductivity of the synapse linking 'self' with 'outDendrite'.
      ==> spike: boolean: True ==> spike, False ==> no spike.
      ==> p_spike: probability that an action potential would arrive to 'self' in each time step.
      ==> E: inversion potential for 'self'. In general: E=0 ==> excitatory synapse, E=-70 ==> inhibitory synapse.
      ==> g_boost: increase of the conectivity each time an action potential arrives to 'self'.
      ==> g_max: max g_boost, to be reached through rewarding after the model.
      ==> g_min: min g_boost, to be reached through penalization after the model.
      ==> tau: eigentime of the decay of the conectivity after an action potential has arrived to 'self'.
      ==> P: potential reward that 'self' might get spiking at the proper time.
      ==> A_plus: increase of 'P' each time 'self' fires.
      ==> tau_plus: eigentime of the decay of the reward.

    Methods:
      ==> __init__: __init__ function for objects of class Axon.
      ==> updateStatus: updates all the variables enclosed in objects of class Axon using the corresponding methods.
      ==> updateG: updates the conductivity of the synapse.
      ==> updateP: updates the potential reward the synapse might get if the firing of the presynaptic axon is synchronized to that of the postsynaptic dendrite.
      ==> getReward: gets the current reward for the synapse.
      ==> gegPenalization: gets the current penalization for the synapse.
    """

    #########################################################
    ## __init__:
    def __init__(self, p_spike, E, g_boost=0.015, g_max=0.015, g_min=0, tau=5, A_plus=0.005,
                 tauPlus=20, outDendrite=None):
        """__init__ function of the Axon class:

           Sets many initial values for the axon, which determine its
           behavior.

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
        self.A_plus = A_plus
        self.tauPlus = tauPlus
        self.outDendrite = outDendrite

        # Some aditional parameters of objects of class Axon which are
        # not explicitly given but set here:
        self.spike = False
        self.P = 0

    #########################################################
    ## updateG:
    def updateStatus(self):
        """updateStatus function:

          This function updates the status of objects of the class
          Axon by updating each of its important features.
        """
        self.updateG()
        self.updateP()

    #########################################################
    ## updateG:
    def updateG(self):
        """UpdateG function:

            This method updates the connectivity of the axon
            increasing 'g' in a quantity 'g_boost' if an action
            potential arrives to 'self' or letting 'g' decay
            exponentially otherwise.
        """
        self.spike = False
        if rand.random() < self.p_spike:
            self.spike = True
            self.g = self.g + self.g_boost
            if self.E == 0:
                self.getPenalization()

        self.g = euler(exponentialDecay, self.g, [self.tau,0])

    #########################################################
    ## updateP:
    def updateP(self):
        """updateP function:

          This method updates the 'P' function which encodes the
          reward that synapse recives if the postsynaptic dendrite
          fires at the proper time after 'self' did. Since the reward
          each presynaptic axon gets deppends on the time it fires,
          'P' belongs to each presynaptic axon and not to the
          postsynaptic dendrite as 'M' does.
        """
        if self.spike:
            self.P = self.P + self.A_plus
        else:
            self.P = euler(exponentialDecay, self.P, [self.tauPlus,0])

    #########################################################
    ## getReward:
    def getReward(self):
        """getReward function:

          This method gives the synapse a reward which deppends on how
          synchronized were the presynaptic and the postsynaptic
          spikes.
        """
        self.g_boost = self.g_boost + self.P*self.g_max
        if self.g_boost > self.g_max:
            self.g_boost = self.g_max

    #########################################################
    ## getPenalization:
    def getPenalization(self):
        """getPenalization function:

          This method gives the synapse a penalization which deppends
          on how synchronized were the presynaptic and the
          postsynaptic spikes.
        """
        self.g_boost = self.g_boost + self.outDendrite.M*self.g_max
        if self.g_boost < self.g_min:
            self.g_boost = self.g_min
