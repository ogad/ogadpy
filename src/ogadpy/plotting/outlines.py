# from https://stackoverflow.com/questions/24539296/outline-a-region-in-a-graph


def outline_binary(mapimg, extent=None, ax=None, **kwargs):
    import numpy as np
    import matplotlib.pyplot as plt

    if not mapimg.any():
        return

    if ax is None:
        ax = plt.gca()

    if extent is None:
        try:
            extent = ax.images[0].get_extent()
        except IndexError:
            extent = (-0.5, mapimg.shape[1] - 0.5, -0.5, mapimg.shape[0] - 0.5)
    x0, x1, y0, y1 = extent

    # a vertical line segment is needed, when the pixels next to each other horizontally
    #   belong to diffferent groups (one is part of the mask, the other isn't)
    # after this ver_seg has two arrays, one for row coordinates, the other for column coordinates
    ver_seg = np.where(mapimg[:, 1:] != mapimg[:, :-1])

    # the same is repeated for horizontal segments
    hor_seg = np.where(mapimg[1:, :] != mapimg[:-1, :])

    # if we have a horizontal segment at 7,2, it means that it must be drawn between pixels
    #   (2,7) and (2,8), i.e. from (2,8)..(3,8)
    # in order to draw a discountinuous line, we add Nones in between segments
    l = []
    for p in zip(*hor_seg):
        l.append((p[1], p[0] + 1))
        l.append((p[1] + 1, p[0] + 1))
        l.append((np.nan, np.nan))

    # and the same for vertical segments
    for p in zip(*ver_seg):
        l.append((p[1] + 1, p[0]))
        l.append((p[1] + 1, p[0] + 1))
        l.append((np.nan, np.nan))

    # now we transform the list into a numpy array of Nx2 shape
    segments = np.array(l)

    # now we need to know something about the image which is shown
    #   at this point let's assume it has extents (x0, y0)..(x1,y1) on the axis
    #   drawn with origin='lower'
    # with this information we can rescale our points
    segments[:, 0] = x0 + (x1 - x0) * segments[:, 0] / mapimg.shape[1]
    segments[:, 1] = y0 + (y1 - y0) * segments[:, 1] / mapimg.shape[0]

    # and now there isn't anything else to do than plot it
    if "color" not in kwargs:
        kwargs["color"] = (1, 0, 0, 0.5)
    if "linewidth" not in kwargs:
        kwargs["linewidth"] = 3
    ax.plot(segments[:, 0], segments[:, 1], **kwargs)
