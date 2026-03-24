
import matplotlib.pyplot as plt
import numpy as np 
from scipy import constants

def All(fbpic_dict): 

    plt.figure()
    
    plt.subplot(2, 3, 1)
    X(fbpic_dict)

    plt.subplot(2, 3, 2)
    Y(fbpic_dict)

    plt.subplot(2, 3, 3)
    Z(fbpic_dict)

    plt.subplot(2, 3, 4)
    Px(fbpic_dict)

    plt.subplot(2, 3, 5)
    Py(fbpic_dict)

    plt.subplot(2, 3, 6)
    P(fbpic_dict)

    plt.tight_layout()



def X(fbpic_dict):
    plt.hist(fbpic_dict["x"] * 1e3, bins=100)
    plt.xlabel("x position (mm)")
    plt.ylabel("No. of macroparticles")

def Y(fbpic_dict):
    plt.hist(fbpic_dict["y"] * 1e3, bins=100)
    plt.xlabel("y position (mm)")
    plt.ylabel("No. of macroparticles")

def Z(fbpic_dict): 
    plt.hist((fbpic_dict["dt"] - np.mean(fbpic_dict["dt"])) * constants.c * 1e3, bins=100)
    plt.xlabel("z position (mm)")
    plt.ylabel("No. of macroparticles")

def Px(fbpic_dict): 
    plt.hist(fbpic_dict["px"], bins=100)
    plt.xlabel("$u_x$ (β·γ)")
    plt.ylabel("No. of macroparticles")

def Py(fbpic_dict): 
    plt.hist(fbpic_dict["py"], bins=100)
    plt.xlabel("$u_y$ (β·γ)")
    plt.ylabel("No. of macroparticles")

def P(fbpic_dict): 
    plt.hist(fbpic_dict["p"], bins=100)
    plt.xlabel("$p$ (β·γ)")
    plt.ylabel("No. of macroparticles")
