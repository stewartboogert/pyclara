import matplotlib.pyplot as _plt
import numpy as _np

def All(xsuite_twiss) :

    _plt.subplot(5,1,1)
    Beta(xsuite_twiss, vertical_stack=True)

    _plt.subplot(5,1,2)
    Eta(xsuite_twiss, vertical_stack=False)


def Beta(xsuite_twiss, linestyle = "-", marker=None, s0offset = 0, vertical_stack = False) :
    s = _np.array(xsuite_twiss['s'])
    betax = _np.array(xsuite_twiss['betx'])
    betay = _np.array(xsuite_twiss['bety'])

    # remove any offset in s
    s = s - s[0]
    s = s + s0offset

    _plt.plot(s,betax, label=r'XSuite $\beta_x$', linestyle = linestyle, marker = marker)
    _plt.plot(s,betay, label=r'XSuite $\beta_y$', linestyle = linestyle, marker = marker)

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\beta_{x,y}$ [m]')
    _plt.legend()

def Eta(xsuite_twiss, linestyle = "-", marker=None, s0offset = 0, vertical_stack = False) :
    s = _np.array(xsuite_twiss['s'])
    etax = _np.array(xsuite_twiss['dx'])
    etay = _np.array(xsuite_twiss['dy'])

    s = s + s0offset

    _plt.plot(s,etax, label=r'XSuite $\eta_x$', linestyle = linestyle, marker = marker)
    _plt.plot(s,etay, label=r'XSuite $\eta_y$', linestyle = linestyle, marker = marker)

    if vertical_stack :
        _plt.xlabel('')
        _plt.gca().xaxis.set_visible(False)
    else :
        _plt.xlabel("s [m]")

    _plt.ylabel(r'$\eta_{x,y}$ [m]')
    _plt.legend()