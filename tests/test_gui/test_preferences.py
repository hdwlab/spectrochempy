# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2019 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory
# =============================================================================

from spectrochempy.gui.preferences import (DialogPreferences,
                                           GeneralPreferencePageWidget,
                                           ProjectPreferencePageWidget,)

from spectrochempy.extern.pyqtgraph import mkQApp

guiapp = mkQApp()

class testPreferences():

    def __init__(self):

        self.dlg_preference_pages = [GeneralPreferencePageWidget,
                                     ProjectPreferencePageWidget,]

        self.dlg_preferences = dlg = DialogPreferences(self)

        for Page in self.dlg_preference_pages:
            page = Page(dlg)
            page.initialize()
            dlg.add_page(page)

        dlg.resize(1000, 400)
        dlg.exec_()

#tp = testPreferences()

if __name__ == '__main__':
    pass
