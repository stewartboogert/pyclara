from impactx import elements as _elements

import numpy as _np

def loadyaml(filename):
    import yaml
    with open(filename, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    return yaml_dict

def yaml2impactx(yaml_dict = None, start_element = "CLA-FEA-MAG-QUAD-13", end_element = "CLA-FED-SIM-DUMP-01-START"):

    yaml_elements = yaml_dict['elements']

    d = _elements.Drift(name="line", ds=200)
    q = _elements.Quad(name="q1", ds=1, k=5)

    ix_line = []

    converting = False
    first = True
    old_pos = [0,0,0]

    s_delta = []

    for k in yaml_elements.keys():

        e = yaml_elements[k]
        t = e['type']
        l = e['length']

        if k == start_element:
            converting = True

        if k == end_element:
            converting = False

        if not converting:
            continue

        if first :
            first = False
            old_pos = e['centre']

        if t == 'drift':
            ix_e = _elements.Drift(name=k, ds=l)
            ix_line.append(ix_e)
        elif t == 'quadrupole':
            ix_e = _elements.Quad(name=k, ds=l, k=e['k1l']/l)
            ix_line.append(ix_e)
        else :
            pass

        ds = (_np.array(e['centre'])-_np.array(old_pos))[2]
        print(ds)

        s_delta.append((_np.array(e['centre'])-_np.array(old_pos))[2])

        old_pos = e['centre']





