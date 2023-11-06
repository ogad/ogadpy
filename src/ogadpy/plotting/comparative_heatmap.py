

def comparative_heatmap(data, x, y, ax=None, mask=None, **kwargs):
    from matplotlib import pyplot as plt
    from matplotlib.path import Path
    import numpy as np
    
    
    if ax is None:
        ax = plt.gca()

    segments = data.data_vars
    arc_angle = 360 / len(segments)
    
    if mask is not None:
        data = data.where(mask(data[x], data[y]))

    markers = [Path.arc(angle, angle+arc_angle, is_wedge=True) for angle in np.arange(arc_angle, 360+arc_angle, arc_angle)]
    for label, marker in zip(segments, markers):
        x_vals = data[x].values
        y_vals = data[y].values
        
        hdl = ax.scatter(
            *np.meshgrid(x_vals, y_vals), 
            s=500, 
            c=data[label].T, 
            marker=marker, 
            label=label,
            **kwargs
        )
    
    ax.set_xticks(x_vals)
    ax.set_yticks(y_vals)
    ax.set_aspect(1)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    
    return hdl