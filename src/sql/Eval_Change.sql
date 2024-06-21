Delimiter //
Create Procedure AddEval
(IN n_sid char(10), IN n_cid char(10), IN n_type int, OUT rv int)
Begin
    
	Declare nums int default 0;
    Start Transaction;
    Select Count(*) 
    From Evaluation
    Where sid = n_sid and type = n_type
	Into nums;
    
    IF nums > 0 THEN
		SET rv=1;
        Rollback;
	ELSE 
		SET rv=0;
        Insert Into evaluation(sid, type, cid) value
        (n_sid, n_type, n_cid);
        Commit;
	END IF;


End //

Create Procedure DeleteEval
(IN d_sid char(10), IN d_cid char(10), IN d_type int, OUT rv int)
Begin
	Declare nums int default 0;
    Select Count(*) 
    From Evaluation
    Where sid = d_sid and type = n_type
	Into nums;
    
    IF nums > 0 THEN
		SET rv=1;
	ELSE 
		SET rv=0;
        Delete from Evaluation where
        sid = d_sid and type = n_type;
	END IF;


End //

Delimiter ;

Drop procedure AddEval;
Drop procedure DeleteEval;

Call AddEval("PB21111681","MATH1006",0, @index1);
Call AddEval("PB21111681","MATH1006",1, @index1);