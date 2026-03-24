import matplotlib.pyplot as plt
import numpy as np 
import h5py

def All(hdf5file): 

    plt.figure()
    
    plt.subplot(2, 3, 1)
    X(hdf5file)

    plt.subplot(2, 3, 2)
    Y(hdf5file)

    plt.subplot(2, 3, 3)
    Z(hdf5file)

    plt.subplot(2, 3, 4)
    Px(hdf5file)

    plt.subplot(2, 3, 5)
    Py(hdf5file)

    plt.subplot(2, 3, 6)
    Pz(hdf5file)

    plt.tight_layout()

def X(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        x = f[f"/data/{iteration}/particles/electrons/position/x"][:]
        plt.hist(x * 1e3, bins=100)
        plt.xlabel("x position (mm)")
        plt.ylabel("No. of macroparticles")

def Y(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        y = f[f"/data/{iteration}/particles/electrons/position/y"][:]
        plt.hist(y * 1e3, bins=100)
        plt.xlabel("y position (mm)")
        plt.ylabel("No. of macroparticles")

def Z(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        z = f[f"/data/{iteration}/particles/electrons/position/z"][:]
        plt.hist((z - np.mean(z)) * 1e3, bins=100)
        plt.xlabel("x position (mm)")
        plt.ylabel("No. of macroparticles")

def Px(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        px = f[f"/data/{iteration}/particles/electrons/momentum/x"][:]
        plt.hist(px, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_x$ (β·γ)")
        plt.ylabel("No. of macroparticles")

def Py(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        py = f[f"/data/{iteration}/particles/electrons/momentum/y"][:]
        plt.hist(py, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_y$ (β·γ)")
        plt.ylabel("No. of macroparticles")

def Pz(hdf5file):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        pz = f[f"/data/{iteration}/particles/electrons/momentum/z"][:]
        plt.hist(pz, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_z$ (β·γ)")
        plt.ylabel("No. of macroparticles")


