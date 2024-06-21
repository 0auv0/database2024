Delimiter //
Create Procedure AddInfo
(IN n_sid char(10), IN n_type varchar(8), IN n_infomation varchar(40), OUT rv int)
Begin
    Declare nums int default 0;
    Select Count(*) 
    From Info
    Where sid = n_sid and Info.type=n_type and infomation=n_infomation
	Into nums;
    
    IF nums > 0 THEN
		SET rv=1;
	ELSE 
		SET rv=0;
        Insert Into Info(sid, type, infomation) value
        (n_sid, n_type, n_infomation);
	END IF;

End //

Create Procedure DeleteInfo
()
Begin


End //

Create Procedure SearchInfo
()
Begin


End //

Create Procedure ChangeInfo
()
Begin



End //

Delimiter ;