import sdds as _sdds
from ._elegant import elegant_lte_loader as _elegant_lte_loader

try:
    import ocelot
except ImportError:
    print("ocelot not found, cannot convert yaml to ocelot line")

def elegant2ocelot(elegant_file,
                   line_name = "FEBE",
                   start_element="CLA-FEA-MAG-QUAD-13",
                   end_element="CLA-FED-SIM-DUMP-01-START",
                   elegant_twi = None) :

    # load elegant lattice file
    lte = _elegant_lte_loader(elegant_file)


