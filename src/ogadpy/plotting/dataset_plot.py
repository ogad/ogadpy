from abc import ABC, abstractmethod
from inspect import isgenerator
from itertools import product
from matplotlib.pylab import f
import xarray as xr
import matplotlib.pyplot as plt
import logging
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


class DatasetPlot(ABC):
    def __init__(self, dataset: xr.Dataset):
        self.dataset = dataset

    def plot(self, *dims, plot_var=None, **kwargs):
        dim_kwargs = {k: v for k, v in kwargs.items() if k in self.dataset.dims}
        kwargs = {k: v for k, v in kwargs.items() if k not in self.dataset.dims}

        if isinstance(self.dataset, xr.Dataset):
            plot_var = plot_var if plot_var is not None else self.default_var()
            try:
                to_plot = self.dataset[plot_var].sel(**dim_kwargs)
            except KeyError:
                to_plot = self.dataset[plot_var].sel(**dim_kwargs, method="nearest")
        else:
            to_plot = self.dataset.sel(**dim_kwargs)

        remaining_dims = self.remaining_dims(dims + tuple(dim_kwargs.keys()))

        # If axis/axes are specified, use them by passing them to _plot as a generator
        axes = kwargs.pop("ax", None)
        if axes is not None:
            try:
                axes = iter(axes)
            except TypeError:
                axes = iter([axes])
        else:
            axes = None

        plot_points = list(
            product(*[self.dataset[dim].values for dim in remaining_dims])
        )
        if len(plot_points) > 1:
            logging.info(f"Plotting {len(plot_points)} plots")

        plot_returns = []
        for point in plot_points:
            fixed_vars = {dim: val for dim, val in zip(remaining_dims, point)}
            if axes is None:
                _, ax = plt.subplots()
            else:
                ax = next(axes)
            try:
                data_at_point = to_plot.sel(**fixed_vars)
            except KeyError:
                data_at_point = to_plot.sel(**fixed_vars, method="nearest")
            plot_returns.append(self._plot(*dims, data_at_point, ax=ax, **kwargs))
            self.set_title(fixed_vars, ax)

        return_val = []
        for i in range(len(plot_returns[0])):
            return_val.append([plot_return[i] for plot_return in plot_returns])

        return tuple(return_val)

    @abstractmethod
    def _plot(self, *dims, plot_data, ax, **kwargs) -> tuple[plt.Axes, ...]: ...

    def default_var(self):
        if isinstance(self.dataset, xr.DataArray):
            return self.dataset.name

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

    def label_axes(self, x_var, y_var, ax):
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)

    def set_title(self, fixed_vars: dict, ax):
        title = ", ".join([f"{k}: {v}" for k, v in fixed_vars.items()])
        ax.set_title(title)


class DatasetPlot2D(DatasetPlot):
    """Wrapper for plt.pcolormesh"""

    def _plot(self, x_dim, y_dim, plot_data, ax, cb_kwargs={}, **kwargs):
        im = ax.pcolormesh(
            self.dataset[x_dim],
            self.dataset[y_dim],
            plot_data.transpose(y_dim, x_dim),
            **kwargs,
        )

        self.label_axes(x_dim, y_dim, ax)
        d = make_axes_locatable(ax)
        cax = d.append_axes("right", size="5%", pad=0.05)
        cb = plt.colorbar(im, cax=cax, **cb_kwargs)
        cax.set_ylabel(plot_data.name)

        return (ax, cax)
