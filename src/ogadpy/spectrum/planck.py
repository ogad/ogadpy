def planck_function(temperature, wavelength=None, frequency=None, wavenumber=None):
    '''Supply one of wavelength in m, frequency in Hz, wavenumber in m-1
    
    From https://github.com/EdGrrr/pyLRT/blob/master/pyLRT/misc.py'''
    import scipy.constants
    import numpy as np
    
    h = scipy.constants.h
    c = scipy.constants.c
    kb = scipy.constants.Boltzmann
    if wavelength is not None:
        return ((2*h*c**2)/(wavelength**5))*(1/(np.exp(h*c/(kb*temperature*wavelength))-1))
    elif frequency is not None:
        return ((2*h*frequency**3)/(c**2))*(1/(np.exp(h*frequency/(kb*temperature))-1))
    elif wavenumber is not None:
        return ((2*h*c**2*wavenumber**3))*(1/(np.exp(h*c*wavenumber/(kb*temperature))-1))


def planck_wvl_plot(t, wvl, add_text=True, ax=None, unit=1e-9, **kwargs):
    """Plot the Planck function for a given temperature and wavelength range."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    if ax is None:
        ax = plt.gca()
    radiances = 100 * (wvl*unit)**2 * planck_function(t, wavelength=wvl*unit)
    handle = ax.plot(wvl, radiances, **kwargs)
    
    if add_text:
        label_wvl = wvl[np.array(radiances).argmax()] if isinstance(add_text, bool) else add_text
        ax.text(
            label_wvl, 
            radiances.max(), 
            str(t)+'K',)
    
    return handle
