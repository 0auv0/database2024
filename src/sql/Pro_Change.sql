Delimiter //
Create Procedure AddPro
(In new_pid char(10), In new_pname varchar(20), In new_academy varchar(20), Out rv int)
Begin
	Declare state int default 0;


End //

Create Procedure DeletePro
(In old_pid char(10), Out rv int)
Begin
	Declare state int default 0;
	Declare num int default 0;
	Select Count(*)
    From Profession
    Where old_pid = pid
    Into num;
    IF num > 0 Then
		SET state = 1;
	END IF;
    CASE
		WHEN state=0 THEN 
			SET rv = 0;
		WHEN state=1 THEN
			SET rv = 1;
    END CASE;
    
End //

Create Procedure SearchPro
(In s_pid char(10), Out rv int, Out s_pname varchar(20), Out s_academy varchar(20))
Begin
	Declare state int default 0;

End //

Create Procedure ChangePro
()
Begin



End //

Delimiter ;