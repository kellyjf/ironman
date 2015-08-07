


drop table if exists workouts;
create table workouts (
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

drop table if exists gear;
create table gear (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	brand    varchar(32),      
	model    varchar(32),      
	purchase_date   datetime
);


drop table if exists terrains;
create table terrains (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	name     varchar(32),
	quantum  float
);

