import sdds as _sdds
from ._elegant import elegant_lte_loader as _elegant_lte_loader

try :
    import pybdsim
except ImportError :
    print("pybdsim not found, cannot convert elegant to bdsim line")

def elegant2bdsim_gmad(elegant_file,
                       line_name="FEBE",
                       start_element="CLA-FEA-MAG-QUAD-13",
                       end_element="CLA-FED-SIM-DUMP-01-START",
                       elegant_twi=None,
                       elegant_ps=None):

    # load elegant lattice file
    lte = _elegant_lte_loader(elegant_file)

    # load elegant twiss file if provided
    if elegant_twi is not None :
        if isinstance(elegant_twi, str) :
            elegant_twi = _sdds.load(elegant_twi)

    # create bdsim machine


def elegant2bdsim_memory() :
    pass

def elegant2bdsim_particles() :
    pass