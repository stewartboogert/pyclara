import numpy as _np
from scipy import constants as _constants

m_e_eV = _constants.m_e*_constants.c**2/_constants.electron_volt

import sdds as _sdds
from ._elegant import elegant_lte_loader as _elegant_lte_loader

try :
    import xsuite as _xsuite
    import xobjects as _xobject
    import xtrack as _xtrack
except ImportError:
    print("xsuite not found, cannot convert yaml to xsuite line")

def elegant2xsuite(elegant_file,
                   line_name = "FEBE",
                   start_element="CLA-FEA-MAG-QUAD-13",
                   end_element="CLA-FED-SIM-DUMP-01-START",
                   elegant_twi = None,
                   elegant_ps = None) :

    # load elegant lattice file
    lte = _elegant_lte_loader(elegant_file)

    # load elegant twiss file if provided
    if elegant_twi is not None :
        if isinstance(elegant_twi, str) :
            elegant_twi = _sdds.load(elegant_twi)

    # create xsuite environment
    env = _xtrack.Environment()

    for k in lte :
        ee = lte[k] # elegant element
        if ee['TYPE'].upper() == "LINE":
            continue

        xe = None
        if ee['TYPE'] == 'CHARGE' :
            env.elements[ee['NAME']] = _xtrack.Marker()
        elif ee['TYPE'] == 'DRIFT':
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == 'CSRDRIFT':
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == 'LSCDRIFT':
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == "CSRCSBEND" or ee['TYPE'] == "CSBEND" :
            env.elements[ee['NAME']] = _xtrack.Bend(length=ee['L'],
                                                    angle=ee['ANGLE'],
                                                    edge_entry_model="full")
        elif ee['TYPE'] == 'KQUAD':
            env.elements[ee['NAME']] = _xtrack.Quadrupole(length=ee['L'],
                                                          k1=ee['K1'])
        elif ee['TYPE'] == "KSEXT":
            env.elements[ee['NAME']] = _xtrack.Sextupole(length=ee['L'],
                                                         k2=ee['K2'])
        elif ee['TYPE'] == "KICKER":
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == "ECOL":
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == "MAXAMP" :
            env.elements[ee['NAME']] = _xtrack.Marker()
        elif ee['TYPE'] == 'WATCH':
            env.elements[ee['NAME']] = _xtrack.ParticlesMonitor(num_particles = 1,
                                                                start_at_turn=0,
                                                                stop_at_turn=2)
        elif ee['TYPE'] == 'MONI' :
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        elif ee['TYPE'] == "RFCW" :
            env.elements[ee['NAME']] = _xtrack.Cavity(length=ee['L'], voltage=ee['VOLT'],
                                                      frequency=ee['FREQ'], lag=ee['PHASE'])
        elif ee['TYPE'] == "RFDF" :
            env.elements[ee['NAME']] = _xtrack.Drift(length=ee['L'])
        else :
            print("element type ", ee['TYPE'], " not recognised, skipping")

    # need to be uppercase
    line_component_names = [e.upper() for e in lte[line_name]['LINE']]

    if start_element is None or start_element == "":
        start_element = line_component_names[0]
    if end_element is None or end_element == "":
        end_element = line_component_names[-1]

    # select components
    subline_component_names = []

    adding = False
    istart = -1

    for i, e in enumerate(line_component_names) :
        if e == start_element :
            adding = True
            istart = i

        if adding :
            subline_component_names.append(e)

        if e == end_element :
            adding = False

    # create line
    xtrack_line = env.new_line(name = line_name,
                               components = subline_component_names)
    xtrack_twiss0 = None
    xtrack_twiss = None
    xtrack_particles = None

    # add twiss to environment if provided
    if elegant_twi is not None and elegant_ps is None:
        s = elegant_twi.getColumnValueList('s')[istart]
        p0 = elegant_twi.getColumnValueList('pCentral0')[istart]
        betax = elegant_twi.getColumnValueList('betax')[istart]
        alphax = elegant_twi.getColumnValueList('alphax')[istart]
        etax = elegant_twi.getColumnValueList('etax')[istart]
        etaxp = elegant_twi.getColumnValueList('etaxp')[istart]

        betay = elegant_twi.getColumnValueList('betay')[istart]
        alphay = elegant_twi.getColumnValueList('alphay')[istart]
        etay = elegant_twi.getColumnValueList('etay')[istart]
        etayp = elegant_twi.getColumnValueList('etayp')[istart]

        xtrack_twiss0 = _xtrack.TwissInit(betx = betax,
                                          alfx = alphax,
                                          dx = etax,
                                          dpx = etaxp,
                                          bety = betay,
                                          alfy = alphay,
                                          dy = etay,
                                          dpy = etayp)

        xtrack_line.set_particle_ref(pdg_id_0=11,
                                     p0c = m_e_eV*p0,
                                     s=s)

        xtrack_twiss = xtrack_line.twiss(method="4d",
                                     init=xtrack_twiss0)

    if elegant_ps is not None and elegant_twi is None:
        xtrack_particles = elegant2xsuite_particles(elegant_ps, xtrack_line)
        xtrack_line.track(xtrack_particles)

    return {"env":env,
            "xtrack_twiss0":xtrack_twiss0,
            "xtrack_twiss":xtrack_twiss,
            "xtrack_particles":xtrack_particles}

def elegant2xsuite_particles(elegant_ps, xtrack_line) :
    if isinstance(elegant_ps, str):
        elegant_ps = _sdds.load(elegant_ps)

    x = _np.array(elegant_ps.getColumnValueList('x'))
    y = _np.array(elegant_ps.getColumnValueList('y'))
    xp = _np.array(elegant_ps.getColumnValueList('xp'))
    yp = _np.array(elegant_ps.getColumnValueList('yp'))
    t = _np.array(elegant_ps.getColumnValueList('t'))
    p = _np.array(elegant_ps.getColumnValueList('p'))


    xtrack_line.set_particle_ref(pdg_id_0=11,
                                 p0c=m_e_eV*p.mean())

    zeta = (t-t.mean())*_constants.c*xtrack_line.particle_ref.beta0[0]

    delta = (p-p.mean())/p.mean()

    particles = xtrack_line.build_particles(x=x,
                                            xp=xp,
                                            y=y,
                                            yp=yp,
                                            zeta=zeta,
                                            delta=delta)

    return particles

def xsuite2fbpic(particles) :
    '''Convert xsuite particles to fbpic dict of arrays'''
    pass

def fbpic2xsuite(fbpic_dict) :
    '''Convert fbpic dict of particle arrays to xsuite'''
    pass
