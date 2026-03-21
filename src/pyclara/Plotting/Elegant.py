import sdds as _sdds
import matplotlib.pyplot as _plt
import numpy as _np

def All(elegant_twi) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    _plt.subplot(5,1,1)
    Beta(elegant_twi, vertical_stack=True)

    _plt.subplot(5,1,2)
    Alpha(elegant_twi, vertical_stack=True)

    _plt.subplot(5,1,3)
    Psi(elegant_twi, vertical_stack=True)

    _plt.subplot(5,1,4)
    Eta(elegant_twi, vertical_stack=True)

    _plt.subplot(5,1,5)
    Energy(elegant_twi)


def Machine(elegant_ele, vertical_stack = False) :
    pass

def Beta(elegant_twi, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = _np.array(elegant_twi.getColumnValueList('s'))
    betax = _np.array(elegant_twi.getColumnValueList('betax'))
    betay = _np.array(elegant_twi.getColumnValueList('betay'))

    # remove any offset in s
    s = s - s[0]

    _plt.plot(s,betax, label=r'Elegant $\beta_x$')
    _plt.plot(s,betay, label=r'Elegant $\beta_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")
    _plt.ylabel(r'$\beta_{x,y}$ [m]')
    _plt.legend()

def Alpha(elegant_twi, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = elegant_twi.getColumnValueList('s')
    alphax = elegant_twi.getColumnValueList('alphax')
    alphay = elegant_twi.getColumnValueList('alphay')

    _plt.plot(s,alphax, label=r'Elegant $\alpha_x$')
    _plt.plot(s,alphay, label=r'Elegant $\alpha_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\beta_{x,y}$ [m]')
    _plt.legend()

def Psi(elegant_twi, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = elegant_twi.getColumnValueList('s')
    psix = _np.array(elegant_twi.getColumnValueList('psix'))/_np.pi
    psiy = _np.array(elegant_twi.getColumnValueList('psiy'))/_np.pi

    _plt.plot(s,psix, label=r'Elegant $\psi_x [\pi]$')
    _plt.plot(s,psiy, label=r'Elegant $\psi_y [\pi]$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")
    _plt.ylabel(r'$\psi_{x,y} [\pi]$ ')
    _plt.legend()

def Eta(elegant_twi, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = elegant_twi.getColumnValueList('s')
    etax = elegant_twi.getColumnValueList('etax')
    etay = elegant_twi.getColumnValueList('etay')

    _plt.plot(s,etax, label=r'Elegant $\eta_x$')
    _plt.plot(s,etay, label=r'Elegant $\eta_y$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\eta_{x,y}$ [m]')
    _plt.legend()

def Energy(elegant_twi, vertical_stack = False) :
    if isinstance(elegant_twi, str) :
        elegant_twi = _sdds.load(elegant_twi)

    s = elegant_twi.getColumnValueList('s')
    pCentral0 = elegant_twi.getColumnValueList('pCentral0')

    _plt.plot(s,pCentral0, label=r'$p_0$')

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")
        _plt.ylabel(r"Elegant $\beta\gamma$")
    _plt.legend()