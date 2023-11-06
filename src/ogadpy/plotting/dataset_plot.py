from abc import ABC, abstractmethod
from inspect import isgenerator
from itertools import product
import stat
from matplotlib.pylab import f
from numpy import fix
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from mpl_toolkits.axes_grid1 import make_axes_locatable


class DatasetPlot(ABC):
    def __init__(self, dataset: xr.Dataset, ax=None, **kwargs):
        self.dataset = dataset

    def plot(self, *dims, plot_var=None, **kwargs):
        plot_var = plot_var if plot_var is not None else self.default_var()

        dim_kwargs = {k: v for k, v in kwargs.items() if k in self.dataset.dims}
        to_plot = self.dataset[plot_var].sel(**dim_kwargs)

        remaining_dims = self.remaining_dims(dims)

        # If axis/axes are specified, use them by passing them to _plot as a generator
        ax = kwargs.pop("ax", None)
        if ax is not None:
            try:
                ax = iter(ax)
            except TypeError:
                ax = iter([ax])
            kwargs["ax"] = ax

        plot_points = list(
            product(*[self.dataset[dim].values for dim in remaining_dims])
        )
        if len(plot_points) > 1:
            logging.info(f"Plotting {len(plot_points)} plots")
        for point in plot_points:
            fixed_vars = {dim: val for dim, val in zip(remaining_dims, point)}
            plt.subplots()
            data_at_point = to_plot.sel(**fixed_vars)
            self._plot(*dims, data_at_point, **kwargs)
            self.set_title(fixed_vars)

    def default_var(self):
        var = [i for i in self.dataset.data_vars][0]

        if len(self.dataset.data_vars) > 1:
            logging.warning("plot_var not specified, using first data_var: %s", var)
        return var

    def remaining_dims(self, used_dims):
        dims = [dim for dim in self.dataset.dims if dim not in used_dims]
        if len(dims) > 0:
            logging.warning(
                f"Plotting a non-minimal dataset, may result in many plots; remaining dims: {dims}",
            )

        return dims

    def label_axes(self, x_var, y_var):
        ax = plt.gca()
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)

    def set_title(self, fixed_vars: dict):
        ax = plt.gca()
        title = ", ".join([f"{k}: {v}" for k, v in fixed_vars.items()])
        ax.set_title(title)


class DatasetPlot2D(DatasetPlot):
    """Wrapper for plt.pcolormesh"""

    def _plot(self, x_dim, y_dim, plot_data, **kwargs):
        ax = kwargs.pop("ax", plt.gca())

        if isgenerator(ax):
            ax = next(ax)

        im = ax.pcolormesh(
            self.dataset[x_dim],
            self.dataset[y_dim],
            plot_data.transpose(y_dim, x_dim),
            **kwargs,
        )

        self.label_axes(x_dim, y_dim)
        d = make_axes_locatable(ax)
        cax = d.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)
        cax.set_ylabel(plot_data.name)
        plt.axes(ax)
