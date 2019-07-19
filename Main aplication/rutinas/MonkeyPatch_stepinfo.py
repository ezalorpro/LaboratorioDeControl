""" Funcion para obtener la informacion step de un sistema discreto """
import scipy as sp              # SciPy library (used all over)
import numpy as np
from control.statesp import _convertToStateSpace, _mimo2simo, _mimo2siso
from control.lti import isctime, isdtime
import control
from rutinas.MokeyPatch_forceresponse import forced_response
control.forced_response = forced_response

def _get_ss_simo(sys, input=None, output=None):
    """Return a SISO or SIMO state-space version of sys

    If input is not specified, select first input and issue warning
    """
    sys_ss = _convertToStateSpace(sys)
    if sys_ss.issiso():
        return sys_ss
    warn = False
    if input is None:
        # issue warning if input is not given
        warn = True
        input = 0
    if output is None:
        return _mimo2simo(sys_ss, input, warn_conversion=warn)
    else:
        return _mimo2siso(sys_ss, input, output, warn_conversion=warn)

def step_info(sys, T=None, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1,0.9)):
    '''
    Step response characteristics (Rise time, Settling Time, Peak and others).

    Parameters
    ----------
    sys: StateSpace, or TransferFunction
        LTI system to simulate

    T: array-like object, optional
        Time vector (argument is autocomputed if not given)

    SettlingTimeThreshold: float value, optional
        Defines the error to compute settling time (default = 0.02)

    RiseTimeLimits: tuple (lower_threshold, upper_theshold)
        Defines the lower and upper threshold for RiseTime computation

    Returns
    -------
    S: a dictionary containing:
        RiseTime: Time from 10% to 90% of the steady-state value.
        SettlingTime: Time to enter inside a default error of 2%
        SettlingMin: Minimum value after RiseTime
        SettlingMax: Maximum value after RiseTime
        Overshoot: Percentage of the Peak relative to steady value
        Undershoot: Percentage of undershoot
        Peak: Absolute peak value
        PeakTime: time of the Peak
        SteadyStateValue: Steady-state value


    See Also
    --------
    step, lsim, initial, impulse

    Examples
    --------
    >>> info = step_info(sys, T)
    '''
    sys = _get_ss_simo(sys)
    if T is None:
        if isctime(sys):
            T = _default_response_times(sys.A, 1000)
        else:
            # For discrete time, use integers
            tvec = _default_response_times(sys.A, 1000)
            T = range(int(np.ceil(max(tvec))))

    T, yout = control.step_response(sys, T)
    
    if isdtime(sys, strict=True):
        yout = yout[0]
    
    # Steady state value
    InfValue = yout[-1]

    # RiseTime
    tr_lower_index = (np.where(yout >= RiseTimeLimits[0] * InfValue)[0])[0]
    tr_upper_index = (np.where(yout >= RiseTimeLimits[1] * InfValue)[0])[0]
    RiseTime = T[tr_upper_index] - T[tr_lower_index]

    # SettlingTime
    sup_margin = (1. + SettlingTimeThreshold) * InfValue
    inf_margin = (1. - SettlingTimeThreshold) * InfValue
    # find Steady State looking for the first point out of specified limits
    for i in reversed(range(T.size-1)):
        if((yout[i] <= inf_margin) | (yout[i] >= sup_margin)):
            SettlingTime = T[i+1]
            break

    # Peak
    PeakIndex = np.abs(yout).argmax()
    PeakValue = yout[PeakIndex]
    PeakTime = T[PeakIndex]
    SettlingMax = (yout).max()
    SettlingMin = (yout[tr_upper_index:]).min()
    # I'm really not very confident about UnderShoot:
    UnderShoot = yout.min()
    OverShoot = 100. * (yout.max() - InfValue) / (InfValue - yout[0])

    # Return as a dictionary
    S = {
        'RiseTime': RiseTime,
        'SettlingTime': SettlingTime,
        'SettlingMin': SettlingMin,
        'SettlingMax': SettlingMax,
        'Overshoot': OverShoot,
        'Undershoot': UnderShoot,
        'Peak': PeakValue,
        'PeakTime': PeakTime,
        'SteadyStateValue': InfValue
    }

    return S