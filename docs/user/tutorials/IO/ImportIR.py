# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"pycharm": {"is_executing": false, "name": "#%% md\n"}}
# # Import IR Data
#
# This tutorial shows the specifics related to infrared data import in Spectrochempy. As prerequisite, the user is
# expected to have read the [Import Tutorial](Import.ipynb).
#
# Let's first import spectrochempy:

# %% {"jupyter": {"outputs_hidden": false}, "pycharm": {"name": "#%%\n"}}
import spectrochempy as scp
import os as os

# %% [markdown]
# # 1. Supported fileformats
#
# At the time of writing of this tutorial (Scpy v.0.1.18), spectrochempy has the following readers which are specific to IR
# data:
#
# - `read_omnic()` to open omnic (spa and spg) files
# - `read_bruker_opus()` to open Opus (*.0, ...) files
# - `read_jdx()` to open an IR JCAMP-DX datafile
#
# General purpose data exchange formats such as  \*.csv or \*.mat can also be read using:
#
# - `read_csv()` to open csv files
# - `read_matlab()` to open .mat files
#
# # 1.1. Import of OMNIC files
#
# [Thermo Scientific OMNIC](https://www.thermofisher.com/search/browse/category/us/fr/602580/FTIR%2C+NIR+%26amp%3B+Raman+Software+%26amp%3B+Libraries)
# software have two proprietary binary file formats:
# - .spa files that handle single spectra
# - .spg files which contain a group of spectra
#
# Both have been reverse engineered, hence allowing extracting key data. The Omnic reader of
#  Spectrochempy (`read_omnic()`) has been developed based on posts in open forums on the .spa
#  file format and extended to .spg file formats.
#  
# ## a) import spg file
#
# Let's import an .spg file from the `datadir` (see [Import Tutorial](Import.ipynb)) and display
# its main attributes:

# %% {"pycharm": {"name": "#%%\n"}}
X = scp.read_omnic('irdata//CO@Mo_Al2O3.SPG')
X

# %% [markdown]
# The displayed attibutes are detailed in the following.
#
# - `name` is the name of the group of spectra as it appears in the .spg file. OMNIC sets this name to the .spg filename used at the creation of the group. In this example, the name ("Group sust Mo_Al2O3_base line.SPG") differs from the filemane ("CO@Mo_Al2O3.SPG") because the latter has been changed from outside OMNIC (directly in th OS).
#
# - `author` is that of the creator of the NDDataset (not of the .spg file, which, to our knowledge, does not have thus type of attribute). The string is composed of the username and of the machine name as given by the OS: usermane@machinename.
#
# - "created" is the creation date of the NDDataset (again not that of the .spg file). The actual name of the attribute is `date` and can be accessed (or even changed) using `X.date`  
#
# - `description` indicates the complete pathname of the .spg file. As the pathname is also given in the history (below), it can be a good practice to give a self explaining description of the group, for instance:  

# %%
X.description= 'CO adsorption on CoMo/Al2O3, difference spectra'

# %% [markdown]
# - `history` records changes made to the dataset. Here, right after its creation, it has been sorted by date (see below). 
#
# Then come the attributes related to the data themselves:
#
# - `title` (not to be confused with the `name` of the dataset) describes the nature of data (here absorbance)
#
# - "values" shows a sample of the first and last data and their units when they exist (here a.u. for absorbance units). The numerical values ar accessed through the`data` attibute and the units throut `units` attribute.

# %%
print(X.data)
print(X.units)

# %% [markdown]
# - `shape` is the same as the ndarray `shape` attribute and gives the shape of the data array, here 19 x 3112.
#
# Then come the attributes related to the dimensions of the dataset.  
#
# - the `x` dimension has one coordinate made of the 3112 the wavenumbers.  
#
# - the `y` dimension contains:
#
#     - one coordinate mede of the 19 acquisition timestamps 
#     
#     - two labels
#     
#         - the acquision date (UTC) of each spectrum
#         
#         - the name of each spectrum.
#         
# Note that the `x` and `y` dimensions are the second and first dimension respectively. Hence, `X[i,j]` will return the absorbance of the ith spetrum at the jth  wavenumber.
#
# ### Note: acquisition dates and `y` axis
#
# The acquisition timestamps are the *Unix times* of the acquisition, i.e. the time elapsed in seconds since the reference date of Jan 1st 1970, 00:00:00 UTC. In OMNIC, the acquisition time is that of the start of the acquisison. As such these may be not convenient to use directly (they are currently in the order of 1.5 billion...) With this respect, it can be convenient to shift the origin of time coordinate to that of the 1st spectrum, which has the index `0`: 

# %%
X.y = X.y - X[0].y     
X.y

# %% [markdown]
# It is also possible tu use the ability of Scpy to handle utnit changes:

# %%
X.y = X.y.to("minute")   
X.y

# %% [markdown]
# Note that the valued that are displayed are rounded, not the values stored internally. Hence, the relative time in minutes of the last spectrum is: 

# %%
X[-1].y.data[0]  # the last items of a table can be refered by negative indexes
                 # the values of the Coord object are accessed through the `data` attribute 
                 # whiche is a ndarray, hence the final [0] to have the value:

# %% [markdown]
# which gives the exact time in seconds:

# %%
_ * 60            # the underscore _ recalls the last output.

# %% [markdown]
# Finally, if the time axis needs to be shifted by 2 minutes for instance, it is also very easy to do so:

# %%
X.y = X.y + 2
X.y

# %% [markdown]
# ### Note: The order of spectra
#
# The order of spectra in OMNIC .spg files depends depends on the order in which the spectra were included in the OMNIC window before the group was saved. By default, sepctrochempy reorders the spectra by acquisistion date but the original OMNIC order can be kept using the `order=True` at the function call. For instance:

# %%
X2 = scp.read_omnic('irdata//CO@Mo_Al2O3.SPG', order=False)

# %% [markdown]
# In the present case this will not change nothing because the spectra in the OMNIC file wre already ordered by increasing data. 
#
# Finally, it is worth mentioning that the NDDatasets can generally be manipulated as numpy ndarray. Hence, for instance, the following will inverse the order of the first dimension:  

# %%
X = X[::-1,:]  # reorders the NDDataset along the first dimension going backward
X.y            # displays the `y` dimension

# %% [markdown]
# ### Note: Case of groups with different wavenumbers
#
# An OMNIC .spg file can contain spectra having different wavenumber axes (e.g. different spacings or wavenumber ranges). In its current implementation, the spg reader will purposedly return an error because such spectra *cannot* be included in a single NDdataset which, by definition, contains items that share common axes or dimensions ! Future releases might include an option to deal with such a case and return a list of NDDasets. Let us know if you are interested in such a feature, see [Bug reports and enhancement requests](https://www.spectrochempy.fr/dev/dev/issues.html). 
#

# %% [markdown]
# ### b) Import of .spa files
#
# The import of a single follows exactly the same rules as that of the import of a group, except that the history of the spectrum is also put in the description, and of course, the length of the `y` dimension is one:

# %%
Y = scp.read_omnic('irdata//subdir//7_CZ0-100 Pd_101.spa')
Y

# %% [markdown]
# The omnic reader can also import several spa files together, providing that they share a common axis for the wavenumbers. Tis is the case of the following files in the irdata/subdir directory: "7_CZ0-100 Pd_101.spa", ..., "7_CZ0-100 Pd_104.spa". It is possible to import them in a single NDDataset by using the list of filenames in the function call:

# %%
list_files = ["7_CZ0-100 Pd_101.spa", "7_CZ0-100 Pd_102.spa", "7_CZ0-100 Pd_103.spa", "7_CZ0-100 Pd_104.spa"]
directory = os.path.join(scp.general_preferences.datadir, "irdata\\subdir")
X = scp.read_omnic(list_files, directory=directory)
print(X)

# %% [markdown]
# In such a case ase these .spa files are alone in the directory, a very convenient is the read_dir() method that will gather the .spa files together:

# %%
X = scp.read_dir(directory, recursive=False)
print(X)

# %% [markdown] {"pycharm": {"name": "#%% md\n"}}
# # 1.2. Import of Bruker OPUS files
#
# [Bruker OPUS](https://www.bruker.com/products/infrared-near-infrared-and-raman-spectroscopy/opus-spectroscopy-software.html) files have also a proprietary file format. The Opus reader (`read_bruker_opus()`) of spectrochempy is essentially a wrapper of the python module  and
# [brukeropusreader](https://github.com/qedsoftware/brukeropusreader) developed by QED.
#
#  
# (to be completed...)

# %% [markdown]
# # 1.3. Import of JCAMP-DX files
#
# [JCAMP-DX](http://www.jcamp-dx.org/) is an open format initially developped for IR data and extended to other spectroscopies. At present, the JCAMP-DX reader implemented in Spectrochempy is limited to IR data and AFFN encoding (see R. S. McDonald and Paul A. Wilks, JCAMP-DX: A Standard Form for Exchange of Infrared Spectra in Computer Readable Form, Appl. Spec., 1988, 1, 151–162. doi:10.1366/0003702884428734) fo details.  
#
# (to be completed...)