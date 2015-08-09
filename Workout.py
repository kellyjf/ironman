#! /usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from workout import *
from gear import *
from ironman import *
from summary import *
import sys


class WorkoutModel (QSqlRelationalTableModel):
	[ID,SPORT, DATE,MIN,DIST,TERRID,GEARID] = range(7)
	def __init__(self, parent=None):
		super(WorkoutModel,self).__init__(parent)
		self.setTable("workouts")
		self.setRelation(WorkoutModel.TERRID, QSqlRelation("terrains","id","name"))
		self.setRelation(WorkoutModel.GEARID, QSqlRelation("gear","id","model"))
		self.setHeaderData(WorkoutModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(WorkoutModel.DATE, Qt.Horizontal, QVariant("Date"))
		self.setHeaderData(WorkoutModel.MIN, Qt.Horizontal, QVariant("Minutes"))
		self.setHeaderData(WorkoutModel.DIST, Qt.Horizontal, QVariant("Distance"))
		self.setHeaderData(WorkoutModel.SPORT, Qt.Horizontal, QVariant("Sport"))
		self.setHeaderData(WorkoutModel.TERRID, Qt.Horizontal, QVariant("Site"))
		self.setHeaderData(WorkoutModel.GEARID, Qt.Horizontal, QVariant("Gear"))

class GearModel (QSqlQueryModel):
	[ID,SPORT,NAME,DATE] = range(4)
	def __init__(self, parent=None):
		super(GearModel,self).__init__(parent)
		self.filter=""
		self.setHeaderData(GearModel.ID, Qt.Horizontal, QVariant("ID"))
		self.setHeaderData(GearModel.SPORT, Qt.Horizontal, QVariant("Sport"))
		self.setHeaderData(GearModel.NAME, Qt.Horizontal, QVariant("Brand"))
		self.setHeaderData(GearModel.DATE, Qt.Horizontal, QVariant("Purchased"))
		self.refresh()

	def refresh(self):
		self.setQuery("select id, sport, brand||' '||model as name, purchase_date from gear %s"%(self.filter))

	def setFilter(self,filter):
		self.filter="where %s"%(filter)
		self.refresh()
	
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
		#self.mapper.addMapping(self.calendarWidget, WorkoutModel.DATE)
		self.mapper.addMapping(self.minutesLine, WorkoutModel.MIN)
		self.mapper.addMapping(self.distanceLine, WorkoutModel.DIST)
		self.mapper.addMapping(self.sportCombo, WorkoutModel.SPORT)

		self.terrain=TerrainModel(self)
		self.terrain.select()
		self.terrainCombo.setModel(self.terrain)
		self.terrainCombo.setModelColumn(TerrainModel.NAME)

		self.gear=GearModel(self)
		self.gearCombo.setModel(self.gear)
		self.gearCombo.setModelColumn(GearModel.NAME)

		self.model.select()
		self.mapper.toFirst()
	
		QObject.connect(self.sportCombo,SIGNAL("currentIndexChanged(int)"),self.setPicks)	

	def setPicks(self, row):
		sport=self.sportCombo.currentText()
		self.terrain.setFilter("sport='%s'"%(sport))
		self.gear.setFilter("sport='%s'"%(sport))

	def setIndex(self, index):
		row=index.row()
		self.setPicks(row)
		date=self.model.data(index.sibling(row,WorkoutModel.DATE)).toDate()
		self.calendarWidget.setSelectedDate(date)
		self.mapper.setCurrentModelIndex(index)
		
	def accept(self):
		super(WorkoutDialog,self).accept()
		date=self.calendarWidget.selectedDate()
		row=self.mapper.currentIndex()

		self.model.setData(self.model.index(row,WorkoutModel.DATE),QVariant(date))

		tidx=self.terrain.index(self.terrainCombo.currentIndex(),TerrainModel.ID)
		tval=self.terrain.data(tidx).toInt()[0]
		self.model.setData(self.model.index(row,WorkoutModel.TERRID),tval)

		gidx=self.gear.index(self.gearCombo.currentIndex(),GearModel.ID)
		gval=self.gear.data(gidx).toInt()[0]
		self.model.setData(self.model.index(row,WorkoutModel.GEARID),gval)

		self.mapper.submit()

class SummaryDialog(QDialog, Ui_Summary):
	def __init__(self, parent=None):
		super(SummaryDialog,self).__init__(parent)
		self.setupUi(self)
		self.model = QSqlQueryModel(self)
		self.tableView.setModel(self.model)
		QObject.connect(self.reportCombo, SIGNAL("currentIndexChanged(int)"),self.refresh)

	def refresh(self, ndx):
		if self.reportCombo.currentText() in [ 'By Week' ]:
			self.model.setQuery(QSqlQuery("select strftime('%W', logtime) as 'Week', sport as 'Sport', sum(distance) as 'Distance', round(sum(minutes)/60.0,2) as 'Hours' from workouts group by 1,2 order by 1,2"))
		else:
			self.model.setQuery(QSqlQuery("select sport as 'Sport', sum(distance) as 'Distance', round(sum(minutes)/60.0,2) as 'Hours' from workouts group by 1 order by 1"))


class IronmanWindow(QMainWindow, Ui_Ironman):
	def __init__(self, parent=None):
		super(IronmanWindow,self).__init__(parent)


		self.setupUi(self)
		self.workoutModel = WorkoutModel(self)	
		self.workoutModel.setSort(WorkoutModel.DATE, Qt.DescendingOrder)
		self.tableView.setItemDelegate(QSqlRelationalDelegate(self))
		self.tableView.setModel(self.workoutModel)
		self.workoutModel.select()
		self.tableView.setColumnHidden(WorkoutModel.ID, True)
		self.tableView.setColumnHidden(WorkoutModel.GEARID, True)
		self.tableView.resizeColumnsToContents()

		self.workoutDialog=WorkoutDialog(self, self.workoutModel)
		self.summaryDialog=SummaryDialog(self)

		QObject.connect(self.addButton, SIGNAL("clicked()"), self.add)
		QObject.connect(self.editButton, SIGNAL("clicked()"), self.edit)
		QObject.connect(self.deleteButton, SIGNAL("clicked()"), self.delete)
		QObject.connect(self.workoutDialog, SIGNAL("accepted()"), self.tableView.update)
		QObject.connect(self.tableView, SIGNAL("doubleClicked(QModelIndex)"), self.edit)
		QObject.connect(self.action_Summary, SIGNAL("activated()"), self.summaryDialog.show)
		QObject.connect(self.action_Bike, SIGNAL("activated()"), lambda: self.filter('Bike'))
		QObject.connect(self.action_Swim, SIGNAL("activated()"), lambda: self.filter('Swim'))
		QObject.connect(self.action_Run, SIGNAL("activated()"), lambda: self.filter('Run'))
		QObject.connect(self.action_All, SIGNAL("activated()"), lambda: self.filter(None))

	def filter(self, sport):
		if sport:
			self.workoutModel.setFilter("workouts.sport='%s'"%(sport))
			#print self.workoutModel.lastError().text()
			#print self.workoutModel.selectStatement()
 
		else:
			self.workoutModel.setFilter("")
		self.workoutModel.select()

	def add(self):
		rows=self.workoutModel.rowCount()
		self.workoutModel.insertRow(rows)
		index=self.workoutModel.index(rows,0)
		self.workoutModel.setData(index.sibling(rows,WorkoutModel.DATE),QVariant(QDate.currentDate()))
		self.workoutDialog.calendarWidget.setSelectedDate(QDate.currentDate())
		self.workoutDialog.setIndex(index)
		self.workoutDialog.show()

	def edit(self):
		self.workoutDialog.setIndex(self.tableView.currentIndex())
		self.workoutDialog.show()
	def delete(self):
		index=self.tableView.currentIndex()
		if index.isValid():
			row=index.row()
			self.workoutModel.deleteRowFromTable(row)
			self.workoutModel.select()
			self.tableView.resizeColumnsToContents()


	
if __name__ == "__main__":
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app=QApplication(sys.argv);
	db = QSqlDatabase.addDatabase("QSQLITE")
	db.setDatabaseName("workout.sqlite")
	main=IronmanWindow()
	main.show()
	app.exec_()

