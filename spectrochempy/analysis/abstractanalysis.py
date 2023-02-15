# -*- coding: utf-8 -*-
# ======================================================================================
# Copyright (©) 2015-2023 LCS - Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory.
# ======================================================================================
"""
This module implements the base abstract class to define estimators such as PCA, ...
"""

import logging
import warnings
from functools import partial

import numpy as np
import traitlets as tr
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter
from traittypes import Array

from spectrochempy.core import app, set_loglevel
from spectrochempy.core.common.meta import Meta
from spectrochempy.core.dataset.coord import Coord
from spectrochempy.core.dataset.nddataset import NDDataset
from spectrochempy.utils import MASKED, NOMASK, exceptions
from spectrochempy.utils.traits import MetaConfigurable


class _set_output(object):
    # A decorator to transform np.ndarray output from models to NDDataset
    # according to the X input

    def __init__(
        self, method, *args, keepunits=True, keeptitle=True, typex=None, typey=None
    ):
        self.method = method
        self.keepunits = keepunits
        self.keeptitle = keeptitle
        self.typex = typex
        self.typey = typey

    def __repr__(self):
        """Return the method's docstring."""
        return self.method.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)

    def __call__(self, obj, *args, **kwargs):

        # determine the input X dataset
        X = obj.X
        # get the sklearn data output
        data = self.method(obj, *args, **kwargs)
        # make a new dataset with this data
        X_transf = NDDataset(data)
        # Now set the NDDataset attributes
        if self.keepunits:
            X_transf.units = X.units
        X_transf.name = f"{X.name}_{obj.name}.{self.method.__name__}"
        X_transf.history = f"Created by method {obj.name}.{self.method.__name__}"
        if self.keeptitle:
            X_transf.title = X.title
        # make coordset
        M, N = X.shape
        if X_transf.shape == X.shape:
            X_transf.set_coordset(y=X.y, x=X.x)
        elif self.typey == "components":
            X_transf.set_coordset(
                y=Coord(
                    None,
                    labels=["#%d" % (i + 1) for i in range(X_transf.shape[0])],
                    title="components",
                ),
                x=X.x,
            )
        elif self.typex == "components":
            X_transf.set_coordset(
                y=X.y,
                x=Coord(
                    None,
                    labels=["#%d" % (i + 1) for i in range(X_transf.shape[1])],
                    title="components",
                ),
            )
        return X_transf


# wrap _set_output to allow for deferred calling
def _wrap_ndarray_output_to_nddataset(
    method=None, keepunits=True, keeptitle=True, typex=None, typey=None
):
    if method:
        # case of the decorator without argument
        return _set_output(method)
    else:
        # and with argument
        def wrapper(method):
            return _set_output(
                method,
                keepunits=keepunits,
                keeptitle=keeptitle,
                typex=typex,
                typey=typey,
            )

        return wrapper


class AnalysisConfigurable(MetaConfigurable):
    """
    Abstract class to write analysis estimators.

    Subclass this to get a minimal structure
    """

    name = tr.Unicode()
    description = tr.Unicode()

    # ----------------------------------------------------------------------------------
    # Runtime Parameters
    # ----------------------------------------------------------------------------------
    _warm_start = tr.Bool(False, help="If True previous execution state " "is reused")
    _fitted = tr.Bool(False, help="False if the model was not yet fitted")
    _masked_rc = tr.Tuple(allow_none=True, help="List of masked rows and columns")

    _X = tr.Instance(NDDataset, allow_none=True, help="Data to fit an estimate")
    _X_mask = Array(allow_none=True, help="mask information of the " "input data")
    _X_preprocessed = Array(help="preprocessed X")
    _shape = tr.Tuple(help="original shape of the data, before any transformation")
    _outfit = tr.Any(help="the output of the _fit method")

    # ----------------------------------------------------------------------------------
    # Configuration parameters (depends on the estimator)
    # ----------------------------------------------------------------------------------

    copy = tr.Bool(default_value=True, help="If True passed X data are copied").tag(
        config=True
    )

    # write traits like e.g.,  A = Unicode("A", help='description").tag(config=True)

    # ----------------------------------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------------------------------
    def __init__(
        self,
        *,
        log_level=logging.WARNING,
        config=None,
        warm_start=False,
        **kwargs,
    ):

        # call the super class for initialisation
        super().__init__(section=self.name, config=config, parent=app)

        # set log_level of the console report
        set_loglevel(log_level)

        # initial configuration
        # reset to default if not warm_start
        defaults = self.parameters(default=True)
        configkw = {} if warm_start else defaults
        # eventually take parameters form kwargs
        configkw.update(kwargs)

        for k, v in configkw.items():
            if k in defaults.keys():
                setattr(self, k, v)
            else:
                raise KeyError(
                    f"'{k}' is not a valid configuration parameters. "
                    f"Use the method `parameters()` to check the current "
                    f"allowed parameters and their current value."
                )

        # if warm start we can use the previous fit as starting profiles.
        self._warm_start = warm_start
        if not warm_start:
            # We should not be able to use any methods requiring fit results
            # until the fit method has been executed
            self._fitted = False

    # ----------------------------------------------------------------------------------
    # Data
    # ----------------------------------------------------------------------------------
    def _get_masked_rc(self, mask):
        if np.any(mask):
            masked_columns = np.all(mask, axis=-2)
            masked_rows = np.all(mask, axis=-1)
        else:
            masked_columns = np.zeros(self._shape[-1], dtype=bool)
            masked_rows = np.zeros(self._shape[-2], dtype=bool)
        return masked_rows, masked_columns

    def _remove_masked_data(self, X):

        # Retains only valid rows and columns
        # -----------------------------------
        # unfortunately, the implementation of linalg library
        # doesn't support numpy masked arrays as input. So we will have to
        # remove the masked values ourselves

        # the following however assumes that entire rows or columns are masked,
        # not only some individual data (if this is what you wanted, this
        # will fail)

        if not hasattr(X, "mask"):
            return X

        # store the mask because it will be destroyed
        self._X_mask = X._mask

        # remove masked rows and columns
        masked_rows, masked_columns = self._get_masked_rc(X._mask)

        data = X.data[:, ~masked_columns]
        data = data[~masked_rows]

        # destroy the mask
        X._mask = NOMASK

        # return the modified X dataset
        X.data = data
        return X

    def _restore_masked_data(self, D, axis=-1):
        # by default we restore columns, put axis=0 to restore rows instead
        # Note that it is very important to use here the ma version of zeros
        # array constructor or both if both axis should be restored
        if self._X_mask is None:
            # return it inchanged as wa had no mask originally
            return D

        rowsize, colsize = self._shape
        masked_rows, masked_columns = self._get_masked_rc(self._X_mask)
        M, N = D.shape

        Dtemp = None
        # Put back masked columns in D
        # ----------------------------
        if axis == -1 or axis == 1 or axis == "both":  # and D.shape[0] == rowsize:
            if np.any(masked_columns):
                Dtemp = np.ma.zeros((M, colsize))  # note np.ma, not np.
                Dtemp[:, ~masked_columns] = D
                Dtemp[:, masked_columns] = MASKED
                D = Dtemp

        # Put back masked rows in D
        # -------------------------
        if axis == -2 or axis == 0 or axis == "both":  # and D.shape[1] == colsize:
            if np.any(masked_rows):
                Dtemp = np.ma.zeros((rowsize, N))
                Dtemp[~masked_rows] = D
                Dtemp[masked_rows] = MASKED
                D = Dtemp

        # if Dtemp is None and np.any(self._X_mask):
        #     raise IndexError("Can not restore mask. Please check the given index")

        # return the D array with restored masked data
        return D

    @property
    def X(self):
        """
        Return the X input dataset (eventually modified by the model)
        """
        # We use X property only to show this information to the end user. Internally
        # we use _X attribute to refer to the input data
        X = self._X.copy()
        if self._X_mask is not None:
            # restore masked row and column if necessary
            X.data = self._restore_masked_data(X.data, axis="both")
        return X

    @tr.validate("_X")
    def _X_validate(self, proposal):
        X = proposal.value

        # we need a dataset with eventually  a copy of the original data (default being
        # to copy them)
        if not isinstance(X, NDDataset):
            X = NDDataset(X, copy=self.copy)
        elif self.copy:
            X = X.copy()

        # as in fit methods we often use np.linalg library, we cannot handle directly
        # masked data (so we remove them here and they will be restored at the end of
        # the process during transform or inverse transform methods

        # store the original shape as it will be eventually modified
        self._shape = X.shape

        # remove masked data and return modified dataset
        X = self._remove_masked_data(X)
        return X

    def _X_is_missing(self):
        if self._X is None:
            warnings.warn(
                "Sorry, but the X dataset must be defined "
                f"before you can use {self.name} methods."
            )
            return True

    # ....

    @tr.default("name")
    def _name_default(self):
        raise NameError("The name of the object was not defined.")

    # ----------------------------------------------------------------------------------
    # Private methods that should be most of the time overloaded in subclass
    # ----------------------------------------------------------------------------------
    @tr.observe("_X")
    def _preprocess_as_X_changed(self, change):
        # to be optionally replaced by user defined function (with the same name)
        X = self.X

        # .... preprocessing as scaling, centering, ...

        # return a np.ndarray
        self._X_preprocessed = X.data

    def _fit(self, X, y=None):
        #  Intended to be replaced in the subclasses by user defined function
        #  (with the same name)
        raise NotImplementedError("fit method has not yet been implemented")

    def _reduce(self, *args, **kwargs):
        """
        Intended to be replaced in the subclasses
        """
        raise NotImplementedError("transform has not yet been implemented")

    def _reconstruct(self, *args, **kwargs):
        """
        Intended to be replaced in the subclasses
        """
        raise NotImplementedError("inverse_transform has not yet been implemented")

    # ----------------------------------------------------------------------------------
    # Public methods
    # ----------------------------------------------------------------------------------
    def fit(self, X, y=None, **kwargs):
        """Fit the model with X.

        Parameters
        ----------
        X : array-like of shape (n_observations, n_features)
            Training data, where `n_observations` is the number of observations
            and `n_features` is the number of features.

        y : array_like, optional

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        self._fitted = False  # reiniit this flag

        # fire the X validation and preprocessing.
        self._X = X

        # _X_preprocessed has been computed when X was set
        newX = self._X_preprocessed

        # call to the actual _fit method (overloaded in the subclass)
        # _fit must take X.data not X as argument
        self._fit(newX)

        self._fitted = True
        return self

    @_wrap_ndarray_output_to_nddataset
    def reconstruct(self, X_reduced=None, n_components=None, **kwargs):
        """
        Transform data back to its original space.

        In other words, return an input `X_original` whose reduce/transform would be X.

        Parameters
        ----------
        X_reduced : array-like of shape (n_observations, n_components)
            Reduced X data, where `n_observations` is the number of observations
            and `n_components` is the number of components.

        Returns
        -------
        NDDataset(n_observations, n_features)
            Data with the original X shape
            eventually filtered by the reduce/transform operation.
        """
        if not self._fitted:
            raise exceptions.NotFittedError(
                "The fit method must be used before using reconstruct method"
            )

        if "n_pc" in kwargs:
            warnings.warn("n_pc argument is deprecated, use n_components instead")

        # self.n_components_ is the value calculated during fit
        n_components = kwargs.pop(
            "n_components", kwargs.pop("n_pc", self.n_components_)
        )
        if n_components > self.n_components_:
            warnings.warn(
                "The number of components required for reconstruction "
                "cannot be greater than the fitted model components : "
                f"{self.n_components_}. We then use this latter value."
            )

        if isinstance(X_reduced, NDDataset):
            X_reduced = X_reduced.data

        if n_components < self.n_components_:
            X_reduced = X_reduced[:, :n_components]

        X = self._reconstruct(X_reduced)

        # restore eventually masked rows and columns
        X = self._restore_masked_data(X, axis="both")

        return X

    @_wrap_ndarray_output_to_nddataset(
        keepunits=False, keeptitle=False, typex="components"
    )
    def reduce(self, X=None, n_components=None, **kwargs):
        """Apply dimensionality reduction to X.

        X is projected on the first principal components previously extracted
        from a training set.

        Parameters
        ----------
        X : array-like of shape (n_observations, n_features), optional
            New data, where `n_observations` is the number of observations
            and `n_features` is the number of features.
            if not provided, the input dataset of the fit method will be used.

        Returns
        -------
        NDDataset(n_observations, n_components)
            Projection of X in the first principal components, where `n_observations`
            is the number of observations and `n_components` is the number of the components.
        """
        if not self._fitted:
            raise exceptions.NotFittedError(
                "The fit method must be used before using reduce method"
            )
        if "n_pc" in kwargs:
            warnings.warn("n_pc argument is deprecated, use n_components instead")

        # self.n_components_ is the value calculated during fit
        n_components = kwargs.pop(
            "n_components", kwargs.pop("n_pc", self.n_components_)
        )
        if n_components > self.n_components_:
            warnings.warn(
                "The number of components required for reduction "
                "cannot be greater than the fitted model components : "
                f"{self.n_components_}. We then use this latter value."
            )

        if X is not None:
            # fire the validation and preprocessing
            self._X = X

        # get the processed ndarray data
        newX = self._X_preprocessed
        X_reduced = self._reduce(newX, **kwargs)

        # slice according to n_components
        if n_components < self.n_components_:
            X_reduced = X_reduced[:, :n_components]

        self.n_components = n_components

        # restore eventually masked rows
        X_reduced = self._restore_masked_data(X_reduced, axis=0)

        return X_reduced

    def fit_reduce(self, X, y=None, **kwargs):
        """
        Fit the model with X and apply the dimensionality reduction on X.

        Parameters
        ----------
        X : NDDataset
            Input dataset of shape (n_observation, n_feature) to fit
        **kwargs : Additional optional keywords parameters

        Returns
        -------
        NDDataset(n_observations, n_components)
        """
        self.fit(X, y=None, **kwargs)
        X_reduced = self.reduce(X, **kwargs)
        return X_reduced

    # Alias To be able to use functions with the same terminology as sklearn
    transform = reduce
    transform.__doc__ = reduce.__doc__
    inverse_Transform = reconstruct
    inverse_Transform.__doc__ = reconstruct.__doc__
    fit_transform = fit_reduce
    fit_transform.__doc__ = fit_reduce.__doc__

    @_wrap_ndarray_output_to_nddataset(
        keepunits=None, keeptitle=False, typey="components"
    )
    def get_components(self, n_components=None):
        # also known as loadings
        # self.n_components_ is the value calculated during fit
        if n_components is None or n_components > self.n_components_:
            n_components = self.n_components_
        components = self.components_[:n_components]

        # restore eventually masked columns
        components = self._restore_masked_data(components, axis=1)
        assert components.shape[-1] == self._shape[-1]
        return components

    # ----------------------------------------------------------------------------------
    # Plot methods
    # ----------------------------------------------------------------------------------
    def scoreplot(
        self, scores, *pcs, colormap="viridis", color_mapping="index", **kwargs
    ):
        """
        2D or 3D scoreplot of observations.

        Parameters
        ----------
        *pcs : a series of int argument or a list/tuple
            Must contain 2 or 3 elements.
        colormap : str
            A matplotlib colormap.
        color_mapping : 'index' or 'labels'
            If 'index', then the colors of each n_scores is mapped sequentially
            on the colormap. If labels, the labels of the n_observation are
            used for color mapping.
        """
        self.prefs = self.X.preferences

        if isinstance(pcs[0], (list, tuple, set)):
            pcs = pcs[0]

        # transform to internal index of component's index (1->0 etc...)
        pcs = np.array(pcs) - 1

        # colors
        if color_mapping == "index":

            if np.any(scores.y.data):
                colors = scores.y.data
            else:
                colors = np.array(range(scores.shape[0]))

        elif color_mapping == "labels":

            labels = list(set(scores.y.labels))
            colors = [labels.index(lab) for lab in scores.y.labels]

        if len(pcs) == 2:
            # bidimensional score plot

            fig = plt.figure(**kwargs)
            ax = fig.add_subplot(111)
            ax.set_title("Score plot")

            # ax.set_xlabel(
            #     "PC# {} ({:.3f}%)".format(pcs[0] + 1, self.ev_ratio.data[pcs[0]])
            # )
            # ax.set_ylabel(
            #     "PC# {} ({:.3f}%)".format(pcs[1] + 1, self.ev_ratio.data[pcs[1]])
            # )
            axsc = ax.scatter(
                scores.masked_data[:, pcs[0]],
                scores.masked_data[:, pcs[1]],
                s=30,
                c=colors,
                cmap=colormap,
            )

            number_x_labels = self.prefs.number_of_x_labels  # get from config
            number_y_labels = self.prefs.number_of_y_labels
            # the next two line are to avoid multipliers in axis scale
            y_formatter = ScalarFormatter(useOffset=False)
            ax.yaxis.set_major_formatter(y_formatter)
            ax.xaxis.set_major_locator(MaxNLocator(number_x_labels))
            ax.yaxis.set_major_locator(MaxNLocator(number_y_labels))
            ax.xaxis.set_ticks_position("bottom")
            ax.yaxis.set_ticks_position("left")

        if len(pcs) == 3:
            # tridimensional score plot
            plt.figure(**kwargs)
            ax = plt.axes(projection="3d")
            ax.set_title("Score plot")
            ax.set_xlabel(
                "PC# {} ({:.3f}%)".format(pcs[0] + 1, self.ev_ratio.data[pcs[0]])
            )
            ax.set_ylabel(
                "PC# {} ({:.3f}%)".format(pcs[1] + 1, self.ev_ratio.data[pcs[1]])
            )
            ax.set_zlabel(
                "PC# {} ({:.3f}%)".format(pcs[2] + 1, self.ev_ratio.data[pcs[2]])
            )
            axsc = ax.scatter(
                scores.masked_data[:, pcs[0]],
                scores.masked_data[:, pcs[1]],
                scores.masked_data[:, pcs[2]],
                zdir="z",
                s=30,
                c=colors,
                cmap=colormap,
                depthshade=True,
            )

        if color_mapping == "labels":
            import matplotlib.patches as mpatches

            leg = []
            for lab in labels:
                i = labels.index(lab)
                c = axsc.get_cmap().colors[int(255 / (len(labels) - 1) * i)]
                leg.append(mpatches.Patch(color=c, label=lab))

            ax.legend(handles=leg, loc="best")

        return ax

    def plotmerit(self, X, X_hat, **kwargs):
        """
        Plots the input dataset, reconstructed dataset and residuals.

        Parameters
        ----------
        **kwargs
            optional "colors" argument: tuple or array of 3 colors
            for :math:`X`, :math:`\hat X` and :math:`E`.

        Returns
        -------
        ax
            subplot.
        """
        if not self._fitted:
            raise exceptions.NotFittedError(
                "The fit method must be used " "before using this method"
            )

        colX, colXhat, colRes = kwargs.pop("colors", ["blue", "green", "red"])

        res = X - X_hat
        ax = X.plot()
        ma = X.max()
        if X.x is not None:
            ax.plot(X.x.data, X_hat.T.masked_data - ma, color=colXhat)
            ax.plot(X.x.data, res.T.masked_data - 1.2 * ma, color=colRes)
        else:
            ax.plot(X_hat.T.masked_data, color=colXhat)
            ax.plot(res.T.masked_data, color=colRes)
        ax.autoscale(enable=True, axis="y")
        ax.set_title(f"{self.name} merit plot")
        ax.yaxis.set_visible(False)
        return ax

    # ----------------------------------------------------------------------------------
    # Utility functions
    # ----------------------------------------------------------------------------------
    def parameters(self, default=False):
        """
        Return current or default configuration values

        Parameters
        ----------
        default : Bool, optional, default: False
            If 'default' is True, the default parameters are returned,
            else the current values.

        Returns
        -------
        dict
        """
        d = Meta()
        if not default:
            d.update(self.trait_values(config=True))
        else:
            d.update(self.trait_defaults(config=True))
        return d

    def reset(self):
        """
        Reset configuration to default
        """
        for k, v in self.parameters(default=True).items():
            setattr(self, k, v)

    @classmethod
    @property
    def help(cls):
        """
        Return a description of all configuration parameters with their default value
        """
        return cls.class_config_rst_doc()

    @property
    def log(self):
        """
        Logs output.
        """
        # A string handler (#2) is defined for the Spectrochempy logger,
        # thus we will return it's content
        return app.log.handlers[2].stream.getvalue().rstrip()

    @property
    @exceptions.deprecated(
        "Use log instead. This attribute will be removed in future version"
    )
    def logs(self):
        """
        Logs output.
        """
        return self.log
