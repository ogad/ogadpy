def get_btd(gran, ch1, ch2):
    gran.download(ch1)
    gran.download(ch2)
    
    if gran.get_resolution(ch1) != gran.get_resolution(ch2):
        raise ValueError("Channels must be the same resolution")
    
    btd = gran.get_band_bt(ch1) - gran.get_band_bt(ch2)
    
    return btd

def get_contrail_rgb(gran):
    """As defined in Chevellier et al. 2023
    
    Red (OD): 15 - 13; Green (phase): 14 - 11; Blue (temp): 14
    """
    import xarray as xr
    
    red = get_btd(gran, 15, 13)
    green = get_btd(gran, 14, 11)
    blue = gran.get_band_bt(14)
    
    return xr.Dataset({'red': red, 'green': green, 'blue': blue})