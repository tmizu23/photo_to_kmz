# -*- coding: utf-8 -*-
"""
/***************************************************************************
 photo_to_kmzDialog
                                 A QGIS plugin
 get lat lng from photo to kmz file
                             -------------------
        begin                : 2015-02-04
        copyright            : (C) 2015 by surchai chantee/GIS HAII
        email                : surchai@haii.or.th
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_photo_to_kmz import Ui_photo_to_kmz
# create the dialog for zoom to point
from PyQt4.QtGui import QFileDialog
import os

class photo_to_kmzDialog(QtGui.QDialog, Ui_photo_to_kmz):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.ui = Ui_photo_to_kmz()
        self.setupUi(self)
        

    def OpenBrowse(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        filename1 = dialog.getExistingDirectory(self, 'Choose Directory', os.path.curdir)
        
        #filename1 = getDir()#QFileDialog.getOpenFileName()
        if filename1== None: return
        self.textPath.setText(filename1)
        

