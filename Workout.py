#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from workout import *
from gear import *
from ironman import *
import sys


class WorkoutModel (QSqlRelationalTableModel):
	[ID,SPORT, LOGTIME,MIN,MILES,TERRID,GEARID] = range(7)
	def __init__(self, parent=None):
		super(WorkoutModel,self).__init__(parent)
		self.setTable("workouts")
		self.setRelation(WorkoutModel.TERRID, QSqlRelation("terrains","id","name"))
		self.setRelation(WorkoutModel.GEARID, QSqlRelation("gear","id","model"))
		self.setHeaderData(WorkoutModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(WorkoutModel.LOGTIME, Qt.Horizontal, QVariant("Date"))
		self.setHeaderData(WorkoutModel.MIN, Qt.Horizontal, QVariant("Minutes"))
		self.setHeaderData(WorkoutModel.MILES, Qt.Horizontal, QVariant("Miles"))
		self.setHeaderData(WorkoutModel.SPORT, Qt.Horizontal, QVariant("Sport"))

class GearModel (QSqlRelationalTableModel):
	[ID,SPORT,BRAND, MODEL,DATE] = range(5)
	def __init__(self, parent=None):
		super(GearModel,self).__init__(parent)
		self.setTable("gear")
		self.setHeaderData(GearModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(GearModel.SPORT, Qt.Horizontal, QVariant("Sport"))
		self.setHeaderData(GearModel.BRAND, Qt.Horizontal, QVariant("Brand"))
		self.setHeaderData(GearModel.MODEL, Qt.Horizontal, QVariant("Model"))
		self.setHeaderData(GearModel.DATE, Qt.Horizontal, QVariant("Purchased"))

class TerrainModel (QSqlRelationalTableModel):
	[ID,SPORT,NAME, QUANTUM] = range(4)
	def __init__(self, parent=None):
		super(TerrainModel,self).__init__(parent)
		self.setTable("terrains")

		self.setHeaderData(TerrainModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(TerrainModel.SPORT, Qt.Horizontal, QVariant("Sport"))
		self.setHeaderData(TerrainModel.NAME, Qt.Horizontal, QVariant("Name"))
		self.setHeaderData(TerrainModel.QUANTUM, Qt.Horizontal, QVariant("Unit"))

class WorkoutView (QTableView):
	def __init__(self, parent=None):
		super(WorkoutView,self).__init__(parent)
		self.setItemDelegate(QSqlRelationalDelegate(self))

class GearView (QTableView):
	def __init__(self, parent=None):
		super(GearView,self).__init__(parent)

class WorkoutDialog (QDialog, Ui_Workout):
	def __init__(self, parent, model):
		super(WorkoutDialog,self).__init__(parent)
		self.setupUi(self)
		self.mapper=QDataWidgetMapper(self)
		self.mapper.setItemDelegate(QSqlRelationalDelegate(self))
		self.model = model 
		self.mapper.setModel(self.model)
		self.mapper.addMapping(self.dateEdit, WorkoutModel.LOGTIME)
		self.mapper.addMapping(self.minutesLine, WorkoutModel.MIN)
		self.mapper.addMapping(self.milesLine, WorkoutModel.MILES)
		self.mapper.addMapping(self.sportCombo, WorkoutModel.SPORT)

		rel=TerrainModel(self)
		rel.select()
		rel=self.terrainCombo.setModel(rel)
		self.terrainCombo.setModelColumn(TerrainModel.NAME)
		self.mapper.addMapping(self.terrainCombo, WorkoutModel.TERRID)

		rel=GearModel(self)
		rel.select()
		rel=self.gearCombo.setModel(rel)
		self.gearCombo.setModelColumn(GearModel.MODEL)
		self.mapper.addMapping(self.gearCombo, WorkoutModel.GEARID)

		self.model.select()
		self.mapper.toFirst()
		print self.model.rowCount()

	def accept(self):
		super(WorkoutDialog,self).accept()
		self.mapper.submit()

class IronmanWindow(QMainWindow, Ui_Ironman):
	def __init__(self, parent=None):
		super(IronmanWindow,self).__init__(parent)
		self.setupUi(self)
		self.workoutModel = WorkoutModel(self)	
		self.tableView.setItemDelegate(QSqlRelationalDelegate(self))
		self.tableView.setModel(self.workoutModel)
		self.workoutModel.select()

		self.workoutDialog=WorkoutDialog(self, self.workoutModel)
		QObject.connect(self.addButton, SIGNAL("clicked()"), self.add)
		QObject.connect(self.editButton, SIGNAL("clicked()"), self.edit)
		QObject.connect(self.deleteButton, SIGNAL("clicked()"), self.delete)
		QObject.connect(self.workoutDialog, SIGNAL("accepted()"), self.tableView.update)

	def add(self):
		rows=self.workoutModel.rowCount()
		self.workoutModel.insertRow(rows)
		index=self.workoutModel.index(rows,0)
		self.workoutDialog.mapper.setCurrentModelIndex(index)
		self.workoutDialog.show()
		print "Add"
	def edit(self):
		print "Edit"
	def delete(self):
		print "Delete"


	
if __name__ == "__main__":
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app=QApplication(sys.argv);
	db = QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("workout.sqlite")
	main=IronmanWindow()
	main.show()
	app.exec_()

