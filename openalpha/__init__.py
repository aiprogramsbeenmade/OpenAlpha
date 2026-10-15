"""
Pacchetto delle operazioni matematiche di OpenAlpha.
"""

from __future__ import annotations

from openalpha.operations.algebra import expand as _expand  # noqa: F401
from openalpha.operations.algebra import factor as _factor  # noqa: F401
from openalpha.operations.algebra import simplify as _simplify  # noqa: F401
from openalpha.operations.calculus.diff import diff as _diff  # noqa: F401
from openalpha.operations.calculus.integrate import integrate as _integrate  # noqa: F401
from openalpha.operations.calculus.limit import limit as _limit  # noqa: F401
from openalpha.operations.equations import solve as _solve  # noqa: F401
from openalpha.operations.numeric.nintegrate import nintegrate as _nintegrate  # noqa: F401
from openalpha.operations.numeric.nsolve import nsolve as _nsolve  # noqa: F401
from openalpha.operations.visualization.plot import plot as _plot  # noqa: F401
