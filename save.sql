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
COMMIT;
