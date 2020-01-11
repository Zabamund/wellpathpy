from hypothesis import given
from hypothesis.strategies import composite
from hypothesis.strategies import floats
from hypothesis.strategies import integers
from hypothesis.strategies import lists
import numpy as np

@composite
def same_len_lists(draw, min_value = None, max_value = None):
    """Draw random arrays of equal lengths

    One precondition of the list version of spherical() is that its inputs must
    be of equal length.
    """
    n = draw(integers(min_value = 0, max_value = 50))
    fixlen = lists(
        floats(
            min_value = min_value,
            max_value = max_value,
            allow_nan = False,
            allow_infinity = False
        ),
        min_size = n,
        max_size = n,
    )
    fixnp = fixlen.map(np.array)
    return (draw(fixnp), draw(fixnp), draw(fixnp))
