PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE workouts (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	logtime  datetime,
	minutes  integer,
	miles    float,
	terrain_id  integer,
	gear_id     integer,
	foreign key(terrain_id) references terrains(id),
	foreign key(gear_id) references gear(id)
);
INSERT INTO "workouts" VALUES(2,'Swim','2015-08-01T00:00:00',40,11.0,NULL,NULL);
INSERT INTO "workouts" VALUES(4,'Run','2015-08-03',20,2.0,13,5);
INSERT INTO "workouts" VALUES(6,'Swim','2015-08-03',75,3500.0,3,3);
INSERT INTO "workouts" VALUES(11,'Bike','2015-08-05',65,20.0,6,1);
INSERT INTO "workouts" VALUES(12,'Swim','2015-08-05',60,2000.0,3,3);
INSERT INTO "workouts" VALUES(13,'Run','2015-08-06',24,2.4,13,5);
CREATE TABLE gear (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	brand    varchar(32),      
	model    varchar(32),      
	purchase_date   datetime
);
INSERT INTO "gear" VALUES(1,'Bike','Litespeed','Road','1/1/2001');
INSERT INTO "gear" VALUES(2,'Bike','Cervelo','P2C','1/1/2009');
INSERT INTO "gear" VALUES(3,'Swim','Agon','Jammers','1/1/2014');
INSERT INTO "gear" VALUES(4,'Swim','Agon','Tights','1/1/2015');
INSERT INTO "gear" VALUES(5,'Run','Mizuno','Blue','1/1/2015');
INSERT INTO "gear" VALUES(6,'Run','Someone','Orange','1/1/2015');
CREATE TABLE terrains (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	name     varchar(32),
	quantum  float
);
INSERT INTO "terrains" VALUES(3,'Swim','25 Yards',0.0142045);
INSERT INTO "terrains" VALUES(4,'Swim','25 Meters',0.0155343);
INSERT INTO "terrains" VALUES(5,'Swim','50 Meters',0.0310686);
INSERT INTO "terrains" VALUES(6,'Bike','Climbing',0.1);
INSERT INTO "terrains" VALUES(7,'Bike','Flat',0.1);
INSERT INTO "terrains" VALUES(8,'Bike','Commute',0.1);
INSERT INTO "terrains" VALUES(9,'Bike','Trainer',0.1);
INSERT INTO "terrains" VALUES(10,'Run','Hills',0.1);
INSERT INTO "terrains" VALUES(11,'Run','Track',0.1);
INSERT INTO "terrains" VALUES(12,'Run','Trail',0.1);
INSERT INTO "terrains" VALUES(13,'Run','Treadmill',0.1);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('terrains',13);
INSERT INTO "sqlite_sequence" VALUES('gear',6);
INSERT INTO "sqlite_sequence" VALUES('workouts',13);
COMMIT;
