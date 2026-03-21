import sdds as _sdds
import matplotlib.pyplot as _plt
import numpy as _np

def All(elegant_twi, start_element = None, end_element = None) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    _plt.subplot(5,1,1)
    Beta(elegant_twi, start_element=start_element, end_element=end_element, vertical_stack=True)

    _plt.subplot(5,1,2)
    Alpha(elegant_twi, start_element=start_element, end_element=end_element, vertical_stack=True)

    _plt.subplot(5,1,3)
    Psi(elegant_twi, start_element=start_element, end_element=end_element, vertical_stack=True)

    _plt.subplot(5,1,4)
    Eta(elegant_twi, start_element=start_element, end_element=end_element, vertical_stack=True)

    _plt.subplot(5,1,5)
    Energy(elegant_twi, start_element=start_element, end_element=end_element, vertical_stack=True)


def _getRangeIndices(names, start_element, end_element) :
    if start_element is not None and start_element != "" :
        i_start = _np.where(names == start_element)[0][0]
    else :
        i_start = 0

    if end_element is not None and end_element != "" :
        i_end = _np.where(names == end_element)[0][0]
    else :
        i_end = len(names)

    return i_start, i_end

def Machine(elegant_ele, vertical_stack = False) :
    pass

def Beta(elegant_twi, start_element = None, end_element = None, vertical_stack = False) :

    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    names = _np.array(elegant_twi.getColumnValueList('ElementName'))
    betax = _np.array(elegant_twi.getColumnValueList('betax'))
    betay = _np.array(elegant_twi.getColumnValueList('betay'))

    # find indicies
    i_start, i_end = _getRangeIndices(names, start_element, end_element)

    # remove any offset in s
    s = s - s[i_start]

    _plt.plot(s[i_start:i_end],betax[i_start:i_end], label=r'Elegant $\beta_x$')
    _plt.plot(s[i_start:i_end],betay[i_start:i_end], label=r'Elegant $\beta_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")
    _plt.ylabel(r'$\beta_{x,y}$ [m]')
    _plt.legend()

def Alpha(elegant_twi, start_element = None, end_element = None, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    names = _np.array(elegant_twi.getColumnValueList('ElementName'))
    alphax = _np.array(elegant_twi.getColumnValueList('alphax'))
    alphay = _np.array(elegant_twi.getColumnValueList('alphay'))

    # find indicies
    i_start, i_end = _getRangeIndices(names, start_element, end_element)

    _plt.plot(s[i_start:i_end],alphax[i_start:i_end], label=r'Elegant $\alpha_x$')
    _plt.plot(s[i_start:i_end],alphay[i_start:i_end], label=r'Elegant $\alpha_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\beta_{x,y}$ [m]')
    _plt.legend()

def Psi(elegant_twi, start_element = None, end_element = None, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    names = _np.array(elegant_twi.getColumnValueList('ElementName'))
    psix = _np.array(elegant_twi.getColumnValueList('psix'))/_np.pi
    psiy = _np.array(elegant_twi.getColumnValueList('psiy'))/_np.pi

    # find indicies
    i_start, i_end = _getRangeIndices(names, start_element, end_element)

    _plt.plot(s[i_start:i_end],psix[i_start:i_end], label=r'Elegant $\psi_x [\pi]$')
    _plt.plot(s[i_start:i_end],psiy[i_start:i_end], label=r'Elegant $\psi_y [\pi]$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")
    _plt.ylabel(r'$\psi_{x,y} [\pi]$ ')
    _plt.legend()

def Eta(elegant_twi, start_element = None, end_element = None, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    names = _np.array(elegant_twi.getColumnValueList('ElementName'))
    etax = _np.array(elegant_twi.getColumnValueList('etax'))
    etay = _np.array(elegant_twi.getColumnValueList('etay'))

    # find indicies
    i_start, i_end = _getRangeIndices(names, start_element, end_element)

    _plt.plot(s[i_start:i_end],etax[i_start:i_end], label=r'Elegant $\eta_x$')
    _plt.plot(s[i_start:i_end],etay[i_start:i_end], label=r'Elegant $\eta_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\eta_{x,y}$ [m]')
    _plt.legend()

def Energy(elegant_twi, start_element = None, end_element = None, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    names = _np.array(elegant_twi.getColumnValueList('ElementName'))
    pCentral0 = _np.array(elegant_twi.getColumnValueList('pCentral0'))

    # find indicies
    i_start, i_end = _getRangeIndices(names, start_element, end_element)

    _plt.plot(s[i_start:i_end],pCentral0[i_start:i_end], label=r'$p_0$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r"Elegant $\beta\gamma$")
    _plt.legend()