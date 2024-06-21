Create Table Profession(
	pid char(10),
	pname varchar(20) Not NULL,
	academy varchar(20) Not NULL,
	Constraint PK_Profession Primary Key(pid)
);

Create Table Student(
	sid char(10),
	sname varchar(20) Not NULL,
	sex varchar(2) Not NULL,
	getdate date Not NULL,
	pid char(10) Not NULL,
	phone char(11),
	email varchar(50) ,
	Constraint PK_Stu Primary Key(sid),
	Constraint FK_Stu_Profession Foreign Key(pid) References Profession(pid),
	Constraint CK_phone Check(phone like '1%' and length(phone) = 11),
	Constraint CK_email Check(email like '%@%.%'),
	Constraint CK_sid Check(sid REGEXP "[A-Z]{2}[0-9]{8}"),
    Constraint CK_sex Check(sex In ("男","女"))
);

Create Table Course(
	cid char(10),
	cname varchar(20) Not NULL,
	credit int Not NULL,
	type varchar(10),
	Constraint PK_Course Primary Key(cid),
    Constraint CK_credit Check (credit > 0 and credit <7)
);

Create Table SC(
	sid char(10),
	cid char(10),
	score int,
	Constraint PK_SC Primary Key(sid, cid),
    Constraint FK_SID1 Foreign Key(sid) References Student(sid),
    Constraint FK_CID1 Foreign Key(cid) References Course(cid),
    Constraint CK_Score Check (score>=0 and score <=100)
);

Create Table Info(
	sid char(10),
	type varchar(8),
	infomation varchar(40), 
	Constraint PK_Info Primary Key(sid, type, infomation),
    Constraint FK_SID2 Foreign Key(sid) References Student(sid),
    Constraint CK_type Check (type In ("开除","留校察看","违纪","警告","科研成果","比赛成绩","奖学金","社会贡献"))
);

Create Table Evaluation(
	sid char(10),
	type int,
	cid char(10) Not NULL,
	Constraint PK_Evaluation Primary Key(sid, type),
    Constraint FK_SID3 Foreign Key(sid) References Student(sid),
    Constraint CK_type1 Check( type <= 7 and type >= 0)
);