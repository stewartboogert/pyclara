import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
import numpy as np
import h5py
from scipy.constants import c, e, m_e
from scipy.stats import binned_statistic_2d

def All(hdf5file,species): 

    plt.figure()
    
    plt.subplot(2, 3, 1)
    X(hdf5file,species)

    plt.subplot(2, 3, 2)
    Y(hdf5file,species)

    plt.subplot(2, 3, 3)
    Z(hdf5file,species)

    plt.subplot(2, 3, 4)
    Px(hdf5file,species)

    plt.subplot(2, 3, 5)
    Py(hdf5file,species)

    plt.subplot(2, 3, 6)
    Pz(hdf5file,species)

    plt.tight_layout()

def X(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        x = f[f"/data/{iteration}/particles/{species}/position/x"][:]
        plt.hist(x * 1e3, bins=100)
        plt.xlabel("x position (mm)")
        plt.ylabel("No. of macroparticles")

def Y(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        y = f[f"/data/{iteration}/particles/{species}/position/y"][:]
        plt.hist(y * 1e3, bins=100)
        plt.xlabel("y position (mm)")
        plt.ylabel("No. of macroparticles")

def Z(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        z = f[f"/data/{iteration}/particles/{species}/position/z"][:]
        plt.hist((z - np.mean(z)) * 1e3, bins=100)
        plt.xlabel("z position (mm)")
        plt.ylabel("No. of macroparticles")

def Px(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        px = f[f"/data/{iteration}/particles/{species}/momentum/x"][:]
        plt.hist(px, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_x$ (β·γ)")
        plt.ylabel("No. of macroparticles")

def Py(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        py = f[f"/data/{iteration}/particles/{species}/momentum/y"][:]
        plt.hist(py, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_y$ (β·γ)")
        plt.ylabel("No. of macroparticles")

def Pz(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        pz = f[f"/data/{iteration}/particles/{species}/momentum/z"][:]
        plt.hist(pz, bins=100)
        plt.yscale("log")
        plt.xlabel("$u_z$ (β·γ)")
        plt.ylabel("No. of macroparticles")

def Wakefield_Ez(hdf5file,plotname = "Wakefield_Ez", species = 'beam'):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        attrs = f[f'data/{iteration}/fields/E'].attrs
        dr, dz = attrs['gridSpacing']
        r0, z0 = attrs['gridGlobalOffset']
        Ez = f[f"/data/{iteration}/fields/E/z"][:]
        Ez = Ez[0] + 2 * Ez[1]
        Nr, Nz = Ez.shape
        z = (z0 + np.arange(Nz) * dz) * 1e6  # µm
        r = (r0 + np.arange(Nr) * dr) * 1e6  # µm
        Ez_full = np.vstack([Ez[::-1], Ez])
        r_full = np.concatenate([-r[::-1], r])
        v = np.percentile(np.abs(Ez_full / 1e9), 99)
        plt.figure(figsize=(10, 4))
        scale = np.max(np.abs(Ez[0])) / (r_full[-1] * 0.8)
        plt.plot(z, Ez[0, :] / scale, color='black', lw=1.5)
        plt.imshow(Ez_full / 1e9, origin='lower', aspect='auto', cmap='RdBu_r',
                   vmin=-v, vmax=v, extent=[z[0], z[-1], r_full[0], r_full[-1]])
        plt.colorbar(label='GV/m', pad=0.10)
        plt.xlabel('z (µm)');
        plt.ylabel('r (µm)');
        plt.title(f'{plotname}', fontsize=18)
        original_ylim = plt.ylim()
        ax2 = plt.twinx()
        ax2.set_ylim(np.array(original_ylim) * scale / 1e9)
        ax2.set_ylabel('Ez at r=0 (GV/m)')
        ax2.tick_params(axis='y')
        plt.tight_layout()
        plt.show()

def rho (hdf5file,plotname = "Electron Density", species = 'electrons'):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        attrs = f[f'data/{iteration}/fields/E'].attrs
        dr, dz = attrs['gridSpacing']
        r0, z0 = attrs['gridGlobalOffset']
        w = f[f"/data/{iteration}/particles/electrons/weighting"][:]
        mean_w = np.mean(w)
        rho = f[f'data/{iteration}/fields/rho'][:]
        rho = rho[0] + 2 * rho[1]
        Nr, Nz = rho.shape
        z = (z0 + np.arange(Nz) * dz) * 1e6
        r = (r0 + np.arange(Nr) * dr) * 1e6
        rho_full = np.vstack([rho[::-1], rho]) / -e / 1e6 * mean_w
        r_full = np.concatenate([-r[::-1], r])
        v = np.percentile(np.abs(rho_full), 99)
        plt.figure(figsize=(10, 4))
        plt.imshow(rho_full, origin='lower', aspect='auto', cmap='Blues',
                   vmin=-v, vmax=v, extent=[z[0], z[-1], r_full[0], r_full[-1]])
        plt.colorbar(label='C/cm³')
        plt.xlabel('z (µm)');
        plt.ylabel('r (µm)');
        plt.title(f'{plotname}', fontsize=18)
        plt.tight_layout()
        plt.show()

def plot_beam(hdf5file,plot_name = "Beam Density", species = 'beam'):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f['data'].keys())[0]
        p = f[f'data/{iteration}/particles/{species}']
        x = p['position/x'][:]   # m
        y = p['position/y'][:]   # m
        z = p['position/z'][:]   # m
        w = p['weighting'][:]    # physical particles per macroparticle
        print(max(w), min(w), np.mean(w))

        # rho field: openPMD thetaMode (m=0, m=1) -> components [mode0, m1_real, m1_imag]
        rho_ds = f[f'data/{iteration}/fields/rho']
        rho_modes = rho_ds[:]                         # (3, Nr, Nz)
        dr, dz_f   = rho_ds.attrs['gridSpacing']
        r0, z0     = rho_ds.attrs['gridGlobalOffset']
        pos_r, pos_z = rho_ds.attrs['position']       # cell-centering (0.5, 0.5)
        gunit      = rho_ds.attrs['gridUnitSI']
        unitSI     = rho_ds.attrs['unitSI']
        Nr, Nz = rho_modes.shape[1], rho_modes.shape[2]

    mode0    = rho_modes[0]   # (Nr, Nz)
    m1_real  = rho_modes[1]   # (Nr, Nz)

    # Reconstruct rho in the x-z plane (y=0): theta=0 for x>0, theta=pi for x<0.
    # The sin(theta) (imaginary) terms vanish on this plane, so only m1_real matters.
    rho_xpos = (mode0 + m1_real) * unitSI   # x = +r
    rho_xneg = (mode0 - m1_real) * unitSI   # x = -r

    # radial / longitudinal cell-centered axes (m)
    r_axis = (r0 + (np.arange(Nr) + pos_r) * dr) * gunit
    z_axis = (z0 + (np.arange(Nz) + pos_z) * dz_f) * gunit

    # build a full x axis from -r_max..+r_max and stack the field accordingly
    x_field = np.concatenate([-r_axis[::-1], r_axis]) * 1e6          # µm
    rho_field_xz = np.concatenate([rho_xneg[::-1, :], rho_xpos], axis=0)
    z_field = z_axis * 1e6                                            # µm

    # 2D weighted histogram in x-z (particle number density)
    Nbins = 300
    H, zedges, xedges = np.histogram2d(z, x, bins=Nbins, weights=w)

    # bin volumes: dx * dz * Ly(x,z), local y-thickness per bin
    dz = zedges[1] - zedges[0]
    dx = xedges[1] - xedges[0]

    # local y-extent in each (z,x) bin = max(y) - min(y) of the particles there
    ymax, _, _, _ = binned_statistic_2d(z, x, y, statistic='max', bins=[zedges, xedges])
    ymin, _, _, _ = binned_statistic_2d(z, x, y, statistic='min', bins=[zedges, xedges])
    Ly_local = ymax - ymin        # m, NaN for empty bins, 0 for single-particle bins

    bin_volume = dx * dz * Ly_local   # m³
    good = np.isfinite(Ly_local) & (Ly_local > 0)

    # number density [m^-3]
    n = np.zeros_like(H)
    n[good] = H[good] / bin_volume[good]
    rho_cm3 = n / 1e6           # cm^-3

    # Particles (lab frame) and the rho field grid (moving-window frame) can sit at
    # very different absolute z at later iterations, so center each on its OWN z.
    zc_um = np.average(z, weights=w) * 1e6
    z_centers = 0.5 * (zedges[:-1] + zedges[1:]) * 1e6 - zc_um
    x_centers = 0.5 * (xedges[:-1] + xedges[1:]) * 1e6

    # field z centroid weighted by |charge| projected onto z
    rho_proj = np.nansum(np.abs(rho_field_xz), axis=0)
    zc_field = np.average(z_field, weights=rho_proj)
    z_field = z_field - zc_field

    fig, axes = plt.subplots(1, 2, figsize=(18, 4))

    # log color scale anchored to where most of the density actually is:
    # use percentiles of the populated bins so a few hot outliers don't eat the range
    purple_red_yellow = LinearSegmentedColormap.from_list('black_purple_red_yellow', ['black', 'purple', 'red', 'yellow'])
    pos = rho_cm3[np.isfinite(rho_cm3) & (rho_cm3 > 0)]
    vmin0 = np.percentile(pos, 1)
    vmax0 = np.percentile(pos, 99)
    norm0 = LogNorm(vmin=vmin0, vmax=vmax0)
    im0 = axes[0].pcolormesh(z_centers, x_centers, rho_cm3.T, cmap=purple_red_yellow, shading='auto', norm=norm0)
    cb0 = fig.colorbar(im0, ax=axes[0], label=r'$n$ (cm$^{-3}$)')
    cb0.set_label(r'$n$ (cm$^{-3}$)', fontsize=16)
    cb0.ax.tick_params(labelsize=13)
    axes[0].set_xlabel('z (µm)', fontsize=16)
    axes[0].set_ylabel('x (µm)', fontsize=16)
    axes[0].set_title(f'{plot_name}', fontsize=18)
    axes[0].tick_params(labelsize=13)

    # rho from HDF5 field, reconstructed in x-z, in C/cm³ (log scale)
    rho_field_cm3 = rho_field_xz / 1e6 / -e
    pos1 = rho_field_cm3[np.isfinite(rho_field_cm3) & (rho_field_cm3 > 0)]
    vmin1 = np.percentile(pos1, 50)
    vmax1 = np.percentile(pos1, 99)
    norm1 = LogNorm(vmin=vmin1, vmax=vmax1)
    im1 = axes[1].pcolormesh(z_field, x_field, rho_field_cm3, cmap='Reds', shading='auto', norm=norm1)
    cb1 = fig.colorbar(im1, ax=axes[1], label='n (cm$^{-3}$)')
    cb1.set_label('n (cm$^{-3}$)', fontsize=16)
    cb1.ax.tick_params(labelsize=13)
    axes[1].set_xlabel('z (µm)', fontsize=16)
    axes[1].set_ylabel('x (µm)', fontsize=16)
    axes[1].set_title('Electron density', fontsize=18)
    axes[1].tick_params(labelsize=13)


    plt.tight_layout()
    plt.show()

def phase_space(hdf5file,species):
    MeV = 1e6 * e
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        beam = f[f'data/{iteration}/particles/{species}']
        px = beam['momentum/x'][:]
        py = beam['momentum/y'][:]
        pz = beam['momentum/z'][:]
        x = beam['position/x'][:] * 1e6
        y = beam['position/y'][:] * 1e6
        z = beam['position/z'][:] * 1e6
        w = beam['weighting'][:]

    p_norm = np.sqrt(px ** 2 + py ** 2 + pz ** 2) / (m_e * c)
    gamma = np.sqrt(1 + p_norm ** 2)
    energy = (gamma - 1) * m_e * c ** 2 / MeV

    px_norm = px / (m_e * c)
    py_norm = py / (m_e * c)

    # --- x-px ---
    plt.figure(figsize=(6, 4))
    plt.scatter(x, px_norm, s=0.5, c='steelblue', alpha=0.3)
    plt.xlabel('x (µm)');
    plt.ylabel('$p_x / m_e c$')
    plt.title('x-px phase space')
    plt.tight_layout()

    # --- y-py ---
    plt.figure(figsize=(6, 4))
    plt.scatter(y, py_norm, s=0.5, c='steelblue', alpha=0.3)
    plt.xlabel('y (µm)');
    plt.ylabel('$p_y / m_e c$')
    plt.title('y-py phase space')
    plt.tight_layout()

    # --- z-energy ---
    plt.figure(figsize=(6, 4))
    plt.scatter(z, energy, s=0.5, c='steelblue', alpha=0.3)
    plt.xlabel('z (µm)');
    plt.ylabel('Energy (MeV)')
    plt.title('z-Energy phase space')
    plt.tight_layout()

    plt.show()

def divergence(hdf5file,species):
    with h5py.File(hdf5file, 'r') as f:
        iteration = list(f["data"].keys())[0]
        beam = f[f'data/{iteration}/particles/{species}']
        px = beam['momentum/x'][:]
        py = beam['momentum/y'][:]
        pz = beam['momentum/z'][:]
        x = beam['position/x'][:] * 1e6
        y = beam['position/y'][:] * 1e6
        xp = px / pz * 1e3  # mrad
        yp = py / pz * 1e3  # mrad
        # --- x-x' ---
        plt.figure(figsize=(6, 4))
        plt.scatter(x, xp, s=0.5, c='steelblue', alpha=0.3)
        plt.xlabel('x (µm)');
        plt.ylabel("x' (mrad)")
        plt.title("x-x' divergence")
        plt.tight_layout()

        # --- y-y' ---
        plt.figure(figsize=(6, 4))
        plt.scatter(y, yp, s=0.5, c='steelblue', alpha=0.3)
        plt.xlabel('y (µm)');
        plt.ylabel("y' (mrad)")
        plt.title("y-y' divergence")
        plt.tight_layout()

        plt.show()
