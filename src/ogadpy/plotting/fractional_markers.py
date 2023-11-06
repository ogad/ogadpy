def marker_arc(angle, rotation=0.):
    """Return a marker path for a given angle"""
    import numpy as np
    from matplotlib.path import Path
    from matplotlib.transforms import Affine2D
    
    if angle <= np.pi/24:
        verts = np.concatenate([
            bezier_ref_points(0, angle),
            np.array([[0,0]]),
            np.array([[0,0]]),
        ])
    else:
        verts = np.concatenate(
            [bezier_ref_points(i*np.pi/24, (i+1)*np.pi/24) for i in range(int(angle//(np.pi/24)))] 
            + [bezier_ref_points((angle//(np.pi/24))*np.pi/24, angle)] 
            + [np.array([[0,0],[0,0]])]
        )
        
    codes = [1] + [4]*(len(verts)-3) + [2,79]
    return Path(verts,codes).transformed(Affine2D().rotate_deg(rotation))


def bezier_ref_points(phi_start, phi_end):
    import numpy as np
    angle = phi_end - phi_start
    L = 4/3 * np.arctan(angle/4)
    
    start_point = np.array([[np.cos(phi_start), np.sin(phi_start)]])
    end_point = np.array([[np.cos(phi_end), np.sin(phi_end)]])
    
    start_tangent = np.array([[-np.sin(phi_start), np.cos(phi_start)]])
    end_tangent = np.array([[-np.sin(phi_end), np.cos(phi_end)]])
    
    ref_points = np.concatenate([
        start_point,
        start_point + L*start_tangent,
        end_point - L*end_tangent,
        end_point,
    ])
    
    return ref_points