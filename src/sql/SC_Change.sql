Delimiter //
Create Procedure AddSC
(IN n_sid char(10), IN n_cid char(10), IN score int, OUT rv int)
Begin
    Declare nums int default 0;
    Select Count(*) 
    From SC
    Where sid = n_sid and cid = n_cid
	Into nums;
    
    IF nums > 0 THEN
		SET rv=1;
	ELSE 
		SET rv=0;
        Insert Into SC(sid, cid, score) value
        (n_sid, n_cid, score);
	END IF;

End //

Create Procedure DeleteSC
(IN d_sid char(10), IN d_cid char(10), OUT rv int)
Begin
	Declare nums int default 0;
    Select Count(*) Into nums
    From SC
    Where sid = d_sid and cid = d_cid
	;
    
    IF nums > 0 THEN
		SET rv=0;
        Delete From SC Where sid = d_sid and cid = d_cid;
	ELSE 
		SET rv=1;
	END IF;

End //

Create Procedure SearchSC
(IN s_sid char(10), IN s_cid char(10))
Begin
	Select * From SC
    Where sid=s_sid and cid=s_cid;
End //

Create Procedure ChangeSC
(IN c_sid char(10), IN c_cid char(10), IN c_score int, OUT rv int)
Begin
	Declare nums int default 0;
    Select Count(*)
    From SC
    Where sid = c_sid and cid = c_cid
	Into nums;
    
    IF nums > 0 THEN
		SET rv=0;
		-- Update SC SET score=c_score Where sid=c_sid and cid=c_cid; 
        delete From SC Where sid = c_sid and cid = c_cid;
       Insert Into SC(sid, cid, score) value
        (c_sid, c_cid, c_score);
	ELSE 
		SET rv=1;
	END IF;
End //

Delimiter ;

Call AddSC("PB21111681","MATH1006",NULL, @index1);
Call ChangeSC("PB21111681","MATH1006",34, @index1);
