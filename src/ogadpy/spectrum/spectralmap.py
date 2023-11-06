# From https://stackoverflow.com/questions/44959955/matplotlib-color-under-curve-based-on-spectral-color


def wavelength_to_rgb(wavelength, gamma=0.8):
    ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    Additionally alpha value set to 0.5 outside range
    '''
    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 750:
        A = 1.
    else:
        A = 0.5
    if wavelength < 380:
        wavelength = 380.
    if wavelength > 750:
        wavelength = 750.
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return (R, G, B, A)

# Wavelength limits (nm).
clim = (279, 751) 
#TODO: frequency limits 

def get_norm():
    import matplotlib.pyplot as plt
    return plt.Normalize(*clim)


def spectralmap(): # TODO: frequency map
    # Define a spectral colourmap
    import matplotlib.pyplot as plt
    import numpy as np
    norm = get_norm()
    wl = np.arange(clim[0], clim[1] + 1, 2)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
    return plt.cm.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)


def plot_spectrum(wvls=None, ax=None, yvals=None, frac_yaxis=0.1, n_cols=100, units=1e-9, **kwargs):
    """Plot a spectral patch in the current axis."""# TODO: frequency plot
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    norm = get_norm()
    
    if ax is None:
        ax = plt.gca()
        
    if wvls is None:
        wvls = np.linspace(*ax.get_xlim(), n_cols)
        
    ylims = ax.get_ylim()
    if yvals is None:
        yvals = ylims[-1], ax.transData.inverted().transform(ax.transAxes.transform((1,1+frac_yaxis)))[1] 
    
            
    X=np.meshgrid(1e-9/units * np.linspace(np.min(wvls), np.max(wvls), 500), np.linspace(*yvals, 2))[0]
    extent = (np.min(wvls), np.max(wvls), *yvals)
    
    plt.autoscale(False)
    plt.imshow(X, extent=extent, aspect='auto', norm=norm, cmap=spectralmap)
    plt.autoscale(True)