# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_photo_to_kmz.ui'
#
# Created: Sun Aug 12 16:41:44 2018
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_photo_to_kmz(object):
    def setupUi(self, photo_to_kmz):
        photo_to_kmz.setObjectName(_fromUtf8("photo_to_kmz"))
        photo_to_kmz.setEnabled(True)
        photo_to_kmz.resize(534, 170)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(photo_to_kmz.sizePolicy().hasHeightForWidth())
        photo_to_kmz.setSizePolicy(sizePolicy)
        self.buttonBox = QtGui.QDialogButtonBox(photo_to_kmz)
        self.buttonBox.setGeometry(QtCore.QRect(80, 120, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(photo_to_kmz)
        self.label.setGeometry(QtCore.QRect(40, 70, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.textPath = QtGui.QTextBrowser(photo_to_kmz)
        self.textPath.setGeometry(QtCore.QRect(40, 20, 381, 31))
        self.textPath.setObjectName(_fromUtf8("textPath"))
        self.browseButton = QtGui.QPushButton(photo_to_kmz)
        self.browseButton.setGeometry(QtCore.QRect(434, 20, 81, 31))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.checkBox = QtGui.QCheckBox(photo_to_kmz)
        self.checkBox.setGeometry(QtCore.QRect(440, 80, 75, 16))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.textEdit = QtGui.QLineEdit(photo_to_kmz)
        self.textEdit.setGeometry(QtCore.QRect(260, 70, 161, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(photo_to_kmz)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), photo_to_kmz.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), photo_to_kmz.reject)
        QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL("clicked()"), self.OpenBrowse)

    def retranslateUi(self, photo_to_kmz):
        photo_to_kmz.setWindowTitle(_translate("photo_to_kmz", "photo_to_kmz", None))
        self.label.setText(_translate("photo_to_kmz", "<html><head/><body><p>Save as File Name (only alpabetic)</p><p>not include .kml or .kmz</p></body></html>", None))
        self.textPath.setHtml(_translate("photo_to_kmz", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS UI Gothic\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>", None))
        self.browseButton.setText(_translate("photo_to_kmz", "Select Folder", None))
        self.checkBox.setText(_translate("photo_to_kmz", "kml output", None))

