#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from swim import *
import sys


class SwimModel (QSqlRelationalTableModel):
	[ID,LOGTIME,MIN,YARDS,TERRID,SUITID] = range(6)
	def __init__(self, parent=None):
		super(SwimModel,self).__init__(parent)
		self.setTable("swims")
		self.setRelation(SwimModel.TERRID, QSqlRelation("terrains","id","name"))
		self.setRelation(SwimModel.SUITID, QSqlRelation("suits","id","model"))
		self.setHeaderData(SwimModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(SwimModel.LOGTIME, Qt.Horizontal, QVariant("Date"))
		self.setHeaderData(SwimModel.MIN, Qt.Horizontal, QVariant("Minutes"))
		self.setHeaderData(SwimModel.YARDS, Qt.Horizontal, QVariant("Yards"))

class SwimDialog (QDialog, Ui_Swims):
	def __init__(self, parent=None):
		super(SwimDialog,self).__init__(parent)
		self.setupUi(self)
		self.mapper=QDataWidgetMapper(self)
		self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
		self.model = SwimModel(self)
		self.mapper.setModel(self.model)
		self.mapper.addMapping(self.dateEdit, SwimModel.LOGTIME)
		self.mapper.addMapping(self.minutesLine, SwimModel.MIN)
		self.mapper.addMapping(self.yardsLine, SwimModel.YARDS)

		rel = self.model.relationModel(SwimModel.TERRID)
		self.siteCombo.setModel(rel)
		self.siteCombo.setModelColumn(rel.fieldIndex("name"))
		self.mapper.addMapping(self.siteCombo, SwimModel.TERRID)

		rel = self.model.relationModel(SwimModel.SUITID)
		self.suitCombo.setModel(rel)
		self.suitCombo.setModelColumn(rel.fieldIndex("model"))
		self.mapper.addMapping(self.suitCombo, SwimModel.SUITID)

		self.model.select()
		self.mapper.toFirst()
		print self.model.rowCount()
		print rel.rowCount()

	def accept(self):
		super(SwimDialog,self).accept()
		self.mapper.submit()

	
if __name__ == "__main__":
	app=QApplication(sys.argv);
	db = QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("workout.sqlite")
	swim=SwimDialog()
	swim.show()
	app.exec_()

