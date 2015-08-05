
drop table if exists runs;
create table runs (
	id       integer   primary key autoincrement,
	logtime  datetime,
	minutes  integer,
	miles    float,
	terrain_id  integer,
	shoe_id     integer,
	foreign key(terrain_id) references terrains(id),
	foreign key(shoe_id) references shoes(id)
);

drop table if exists shoes;
create table shoes (
	id       integer   primary key autoincrement,
	brand    varchar(32),      
	model    varchar(32),      
	purchase_date   datetime
);

drop table if exists terrains;
create table terrains (
	id       integer   primary key autoincrement,
	sport    varchar(32),      
	name     varchar(32)      
);

drop table if exists swims;
create table swims (
	id       integer   primary key autoincrement,
	logtime  datetime,
	minutes  integer,
	yards    integer,
	terrain_id  integer,
	suit_id     integer,
	foreign key(terrain_id) references terrains(id),
	foreign key(suit_id) references suits(id)
);

drop table if exists suits;
create table suits (
	id       integer   primary key autoincrement,
	brand    varchar(32),      
	model    varchar(32),      
	purchase_date   datetime
);

drop table if exists rides;
create table rides (
	id       integer   primary key autoincrement,
	logtime  datetime,
	minutes  integer,
	miles    float,
	terrain_id  integer,
	bike_id  integer,
	foreign key(terrain_id) references terrains(id),
	foreign key(bike_id) references bikes(id)
);

drop table if exists bikes;
create table bikes (
	id       integer   primary key autoincrement,
	brand    varchar(32),      
	model    varchar(32),      
	purchase_date   datetime
);
