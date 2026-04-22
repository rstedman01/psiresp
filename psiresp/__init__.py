"""
psiresp
A RESP plugin for Psi4
"""

from .qm import QMEnergyOptions, QMGeometryOptimizationOptions
from .conformer import Conformer, ConformerGenerationOptions
from .orientation import Orientation
from .molecule import Molecule
from .job import Job
from .charge import ChargeConstraintOptions
from .resp import RespOptions, RespCharges
from .grid import GridOptions
from .configs import *

try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("psiresp")
    except PackageNotFoundError:
        __version__ = "unknown"
except ImportError:
    __version__ = "unknown"
