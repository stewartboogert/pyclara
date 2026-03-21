import sdds as _sdds
from ._elegantloader import elegant_lte_loader as _elegant_lte_loader

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
                   elegant_twi = None) :

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
                                                    angle=ee['ANGLE'])
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
    xt_line = env.new_line(name = line_name,
                           components = subline_component_names)

    # add twiss to environment if provided
    if elegant_twi is not None :
        p0 = elegant_twi.getColumnValueList('pCentral0')[istart]
        betax = elegant_twi.getColumnValueList('betax')[istart]
        alphax = elegant_twi.getColumnValueList('alphax')[istart]
        etax = elegant_twi.getColumnValueList('etax')[istart]
        etaxp = elegant_twi.getColumnValueList('etaxp')[istart]

        betay = elegant_twi.getColumnValueList('betay')[istart]
        alphay = elegant_twi.getColumnValueList('alphay')[istart]
        etay = elegant_twi.getColumnValueList('etay')[istart]
        etayp = elegant_twi.getColumnValueList('etayp')[istart]


        print("Twiss init x : ",betax, alphax, etax, etaxp)
        print("Twiss init y : ",betay, alphay, etay, etayp)
        xtrack_twiss0 = _xtrack.TwissInit(betx = betax,
                                          alfx = alphax,
                                          dx = etax,
                                          dpx = etaxp,
                                          bety = betay,
                                          alfy = alphay,
                                          dy = etay,
                                          dpy = etayp)

        xt_line.set_particle_ref(pdg_id_0=11,
                                 p0c = 0.51099895069*p0)

        xtrack_twiss = xt_line.twiss(method="4d",
                                     init=xtrack_twiss0)

        xtrack_track = xt_line.track

    return env, xtrack_twiss0, xtrack_twiss

