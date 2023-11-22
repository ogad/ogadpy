import numpy as np
from itertools import product
import xarray as xr

from ogadpy.plotting.dataset_plot import DatasetPlot2D


class Dataset:
    def __init__(self, data: xr.Dataset | xr.DataArray):
        self.data = data

    @classmethod
    def from_getter(cls, x_var, x_vals, y_var, y_vals, getter, name=None, **kwargs):
        data_values = cls._apply_getter(x_vals, y_vals, getter, **kwargs)
        data = xr.DataArray(
            data_values, coords=[y_vals, x_vals], dims=[y_var, x_var], name=name
        )

        return cls(data)

    @staticmethod
    def _apply_getter(x_vals, y_vals, getter, **kwargs):
        X, Y = np.meshgrid(x_vals, y_vals)
        data = np.zeros_like(X)
        for i, j in product(range(len(x_vals)), range(len(y_vals))):
            data[j, i] = getter(
                x_vals[i],
                y_vals[j],
                **kwargs,
            )
        return data

    def plot_2d(self, x_var, y_var, **kwargs):
        plotter = DatasetPlot2D(self.data)
        return plotter.plot(x_var, y_var, **kwargs)
