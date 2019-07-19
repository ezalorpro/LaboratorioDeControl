# Libraries that we make use of
import scipy as sp              # SciPy library (used all over)
import numpy as np              # NumPy library
from scipy.signal.ltisys import _default_response_times
import warnings
from control.lti import LTI     # base class of StateSpace, TransferFunction
from control.statesp import _convertToStateSpace, _mimo2simo, _mimo2siso
from control.lti import isdtime, isctime

# Helper function for checking array-like parameters
def _check_convert_array(in_obj, legal_shapes, err_msg_start, squeeze=False,
                         transpose=False):
    """
    Helper function for checking array-like parameters.

    * Check type and shape of ``in_obj``.
    * Convert ``in_obj`` to an array if necessary.
    * Change shape of ``in_obj`` according to parameter ``squeeze``.
    * If ``in_obj`` is a scalar (number) it is converted to an array with
      a legal shape, that is filled with the scalar value.

    The function raises an exception when it detects an error.

    Parameters
    ----------
    in_obj: array like object
        The array or matrix which is checked.

    legal_shapes: list of tuple
        A list of shapes that in_obj can legally have.
        The special value "any" means that there can be any
        number of elements in a certain dimension.

        * ``(2, 3)`` describes an array with 2 rows and 3 columns
        * ``(2, "any")`` describes an array with 2 rows and any number of
          columns

    err_msg_start: str
        String that is prepended to the error messages, when this function
        raises an exception. It should be used to identify the argument which
        is currently checked.

    squeeze: bool
        If True, all dimensions with only one element are removed from the
        array. If False the array's shape is unmodified.

        For example:
        ``array([[1,2,3]])`` is converted to ``array([1, 2, 3])``

   transpose: bool
        If True, assume that input arrays are transposed for the standard
        format.  Used to convert MATLAB-style inputs to our format.

    Returns:

    out_array: array
        The checked and converted contents of ``in_obj``.
    """
    # convert nearly everything to an array.
    out_array = np.asarray(in_obj)
    if (transpose):
        out_array = np.transpose(out_array)

    # Test element data type, elements must be numbers
    legal_kinds = set(("i", "f", "c"))  # integer, float, complex
    if out_array.dtype.kind not in legal_kinds:
        err_msg = "Wrong element data type: '{d}'. Array elements " \
                  "must be numbers.".format(d=str(out_array.dtype))
        raise TypeError(err_msg_start + err_msg)

    # If array is zero dimensional (in_obj is scalar):
    # create array with legal shape filled with the original value.
    if out_array.ndim == 0:
        for s_legal in legal_shapes:
            # search for shape that does not contain the special symbol any.
            if "any" in s_legal:
                continue
            the_val = out_array[()]
            out_array = np.empty(s_legal, 'd')
            out_array.fill(the_val)
            break

    # Test shape
    def shape_matches(s_legal, s_actual):
        """Test if two shape tuples match"""
        # Array must have required number of dimensions
        if len(s_legal) != len(s_actual):
            return False
        # All dimensions must contain required number of elements. Joker: "all"
        for n_legal, n_actual in zip(s_legal, s_actual):
            if n_legal == "any":
                continue
            if n_legal != n_actual:
                return False
        return True

    # Iterate over legal shapes, and see if any matches out_array's shape.
    for s_legal in legal_shapes:
        if shape_matches(s_legal, out_array.shape):
            break
    else:
        legal_shape_str = " or ".join([str(s) for s in legal_shapes])
        err_msg = "Wrong shape (rows, columns): {a}. Expected: {e}." \
                  .format(e=legal_shape_str, a=str(out_array.shape))
        raise ValueError(err_msg_start + err_msg)

    # Convert shape
    if squeeze:
        out_array = np.squeeze(out_array)
        # We don't want zero dimensional arrays
        if out_array.shape == tuple():
            out_array = out_array.reshape((1,))

    return out_array

def forced_response(sys, T=None, U=0., X0=0., transpose=False,
                    interpolate=True):
    """Simulate the output of a linear system.

    As a convenience for parameters `U`, `X0`:
    Numbers (scalars) are converted to constant arrays with the correct shape.
    The correct shape is inferred from arguments `sys` and `T`.

    For information on the **shape** of parameters `U`, `T`, `X0` and
    return values `T`, `yout`, `xout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys: LTI (StateSpace, or TransferFunction)
        LTI system to simulate

    T: array-like
        Time steps at which the input is defined; values must be evenly spaced.

    U: array-like or number, optional
        Input array giving input at each time `T` (default = 0).

        If `U` is ``None`` or ``0``, a special algorithm is used. This special
        algorithm is faster than the general algorithm, which is used otherwise.

    X0: array-like or number, optional
        Initial condition (default = 0).

    transpose: bool
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and scipy.signal.lsim)

    interpolate:bool
        If True and system is a discrete time system, the input will
        be interpolated between the given time steps and the output
        will be given at system sampling rate.  Otherwise, only return
        the output at the times given in `T`.  No effect on continuous
        time simulations (default = False).

    Returns
    -------
    T: array
        Time values of the output.
    yout: array
        Response of the system.
    xout: array
        Time evolution of the state vector.

    See Also
    --------
    step_response, initial_response, impulse_response

    Examples
    --------
    >>> T, yout, xout = forced_response(sys, T, u, X0)

    See :ref:`time-series-convention`.
    """
    if not isinstance(sys, LTI):
        raise TypeError('Parameter ``sys``: must be a ``LTI`` object. '
                        '(For example ``StateSpace`` or ``TransferFunction``)')
    sys = _convertToStateSpace(sys)
    A, B, C, D = np.asarray(sys.A), np.asarray(sys.B), np.asarray(sys.C), \
        np.asarray(sys.D)
#    d_type = A.dtype
    n_states = A.shape[0]
    n_inputs = B.shape[1]
    n_outputs = C.shape[0]

    # Set and/or check time vector in discrete time case
    if isdtime(sys, strict=True):
        if T is None:
            if U is None:
                raise ValueError('Parameters ``T`` and ``U`` can\'t both be'
                                 'zero for discrete-time simulation')
            # Set T to equally spaced samples with same length as U
            T = np.array(range(len(U))) * (1 if sys.dt == True else sys.dt)
        else:
            # Make sure the input vector and time vector have same length
            # TODO: allow interpolation of the input vector
            if len(U) != len(T):
                ValueError('Pamameter ``T`` must have same length as'
                           'input vector ``U``')

    # Test if T has shape (n,) or (1, n);
    # T must be array-like and values must be increasing.
    # The length of T determines the length of the input vector.
    if T is None:
        raise ValueError('Parameter ``T``: must be array-like, and contain '
                         '(strictly monotonic) increasing numbers.')
    T = _check_convert_array(T, [('any',), (1, 'any')],
                             'Parameter ``T``: ', squeeze=True,
                             transpose=transpose)
    dt = T[1] - T[0]
    if not np.allclose(T[1:] - T[:-1], dt):
        raise ValueError('Parameter ``T``: time values must be equally spaced.')
    n_steps = len(T)            # number of simulation steps

    # create X0 if not given, test if X0 has correct shape
    X0 = _check_convert_array(X0, [(n_states,), (n_states, 1)],
                              'Parameter ``X0``: ', squeeze=True)

    xout = np.zeros((n_states, n_steps))
    xout[:, 0] = X0
    yout = np.zeros((n_outputs, n_steps))

    # Separate out the discrete and continuous time cases
    if isctime(sys):
        # Solve the differential equation, copied from scipy.signal.ltisys.
        dot, squeeze, = np.dot, np.squeeze  # Faster and shorter code

        # Faster algorithm if U is zero
        if U is None or (isinstance(U, (int, float)) and U == 0):
            # Solve using matrix exponential
            expAdt = sp.linalg.expm(A * dt)
            for i in range(1, n_steps):
                xout[:, i] = dot(expAdt, xout[:, i-1])
            yout = dot(C, xout)

        # General algorithm that interpolates U in between output points
        else:
            # Test if U has correct shape and type
            legal_shapes = [(n_steps,), (1, n_steps)] if n_inputs == 1 else \
                           [(n_inputs, n_steps)]
            U = _check_convert_array(U, legal_shapes,
                                     'Parameter ``U``: ', squeeze=False,
                                     transpose=transpose)
            # convert 1D array to 2D array with only one row
            if len(U.shape) == 1:
                U = U.reshape(1, -1)  # pylint: disable=E1103

            # Algorithm: to integrate from time 0 to time dt, with linear
            # interpolation between inputs u(0) = u0 and u(dt) = u1, we solve
            #   xdot = A x + B u,        x(0) = x0
            #   udot = (u1 - u0) / dt,   u(0) = u0.
            #
            # Solution is
            #   [ x(dt) ]       [ A*dt  B*dt  0 ] [  x0   ]
            #   [ u(dt) ] = exp [  0     0    I ] [  u0   ]
            #   [u1 - u0]       [  0     0    0 ] [u1 - u0]

            M = np.bmat([[A * dt, B * dt, np.zeros((n_states, n_inputs))],
                         [np.zeros((n_inputs, n_states + n_inputs)),
                          np.identity(n_inputs)],
                         [np.zeros((n_inputs, n_states + 2 * n_inputs))]])
            expM = sp.linalg.expm(M)
            Ad = expM[:n_states, :n_states]
            Bd1 = expM[:n_states, n_states+n_inputs:]
            Bd0 = expM[:n_states, n_states:n_states + n_inputs] - Bd1

            for i in range(1, n_steps):
                xout[:, i] = (dot(Ad, xout[:, i-1]) + dot(Bd0, U[:, i-1]) +
                              dot(Bd1, U[:, i]))
            yout = dot(C, xout) + dot(D, U)

        tout = T
        yout = squeeze(yout)
        xout = squeeze(xout)

    else:
        # Discrete type system => use SciPy signal processing toolbox
        if (sys.dt != True):
            # Make sure that the time increment is a multiple of sampling time

            # First make sure that time increment is bigger than sampling time
            if dt < sys.dt:
                raise ValueError("Time steps ``T`` must match sampling time")

            # Now check to make sure it is a multiple (with check against
            # sys.dt because floating point mod can have small errors
            elif not (np.isclose(dt % sys.dt, 0) or
                      np.isclose(dt % sys.dt, sys.dt)):
                raise ValueError("Time steps ``T`` must be multiples of " \
                                 "sampling time")
        else:
            sys.dt = dt         # For unspecified sampling time, use time incr

        # Discrete time simulation using signal processing toolbox
        dsys = (A, B, C, D, sys.dt)

        # Use signal processing toolbox for the discrete time simulation
        # Transpose the input to match toolbox convention 
        tout, yout, xout = sp.signal.dlsim(dsys, np.transpose(U), T, X0)
        
        if not interpolate:
            # If dt is different from sys.dt, resample the output
            inc = int(round(dt / sys.dt))
            tout = T            # Return exact list of time steps
            yout = yout[::inc,:]
            xout = xout[::inc,:]

        # Transpose the output and state vectors to match local convention
        xout = sp.transpose(xout)
        yout = sp.transpose(yout)

    # See if we need to transpose the data back into MATLAB form
    if (transpose):
        tout = np.transpose(tout)
        yout = np.transpose(yout)
        xout = np.transpose(xout)

    return tout, yout, xout