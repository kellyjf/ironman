#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from swim import *
import sys


class SwimDialog (QDialog, Ui_Swims):
	def __init__(self, parent=None):
		super(SwimDialog,self).__init__(parent)
		self.setupUi(self)


if __name__ == "__main__":
	app=QApplication();
	swim=SwimDialog()
	swim.show()
	app.exec_()

