# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-
#
# =============================================================================
# Copyright (©) 2015-2018 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
#
# This software is a computer program whose purpose is to [describe
# functionalities and technical features of your software].
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# =============================================================================

from copy import copy, deepcopy

import numpy as np
import pytest
from traitlets import TraitError
from datetime import datetime

from pint import DimensionalityError
from spectrochempy.api import NDArray
from spectrochempy.api import ur
from tests.utils import (raises)
from spectrochempy.core.units import ur
from spectrochempy.utils import SpectroChemPyWarning
from tests.utils import (assert_equal, assert_array_equal,
                         assert_array_almost_equal, assert_equal_units,
                         raises)
from tests.utils import NumpyRNGContext
from spectrochempy.utils.traittypes import HasTraits, Range


def test_range():

    class MyClass(HasTraits):
        r = Range()  # Initialized with some default values

    c = MyClass()
    c.r = [10, 5]
    assert c.r == [5,10]
    with raises(TraitError):
        c.r = [10, 5, 1]