Delimiter //
Create Trigger DeleteInfo1
After Delete On SC For Each Row
Begin
	Declare count INT default 0;
    Select COUNT(*)
    From SC
    Where SC.sid = old.sid
    AND SC.score is not null
    AND SC.score < 60
    Into count;

	IF count < 3 THEN
		Delete from Info
        Where sid = old.sid and type = '警告' and infomation = '存在挂科现象';
	END IF;
End //

Create Trigger AddInfo1
After Insert On SC For Each Row
Begin
	Declare count INT default 0;
    Select COUNT(*)
    From SC
    Where SC.sid = new.sid
    AND SC.score is not null
    AND SC.score < 60
    Into count;

	IF count = 3 THEN
		Insert Into Info(sid, type, infomation)value(new.sid,'警告','存在挂科现象');
	END IF;
End //

Create Trigger EditInfo1
Before Update On SC For Each Row
Begin
	Declare count INT default 0;
    Select * From SC
	Where SC.sid = old.sid
    and SC.score < 60
	Into count;
    
    
	IF count = 3 THEN
		IF (old.score is null) or (old.score < 60 and new.score >= 60) THEN
			Insert Into Info(sid, type, infomation)value(new.sid,'警告','存在挂科现象');
        END IF;
    END IF;

	IF count = 2 THEN
		IF old.score < 60 and new.score >= 60 THEN
			Delete from Info
			Where sid = old.sid and type = '警告' and infomation = '存在挂科现象';
        END IF;
	END IF;
End //


Delimiter ;

Drop Trigger AddInfo1;
Drop Trigger DeleteInfo1;