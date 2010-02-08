"""This module provides some helper functions."""

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
                --> tau: eigentime of the decay.
                --> resting_value: value to which the variable tend based upon the decay.
    """
    tau = param[0]
    resting_value = param[1]
    return -(x-resting_value)/tau
