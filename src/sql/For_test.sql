Delimiter //
Create Function GPA(in_sid char(10))
Returns float
READS SQL DATA
Begin
    Declare gpa float default 0.0;
	Declare state int default 0;
    DECLARE score int;
    DECLARE credits int;
    Declare total_score float default 0;
    Declare total_credits int default 0;
    Declare temp float default 0.0;
    Declare 
		s_c Cursor for
        (Select SC.score, Course.credit
			from student, SC, Course
			Where student.sid=in_sid and student.sid=SC.sid and SC.cid=course.cid and SC.score Is Not NULL);
	Declare Continue handler for NOT FOUND SET state=1;
    
    
    Open s_c;
    Repeat
		Fetch s_c Into score, credits;
        IF state=0 Then
			CASE 
				WHEN score>=95 THEN SET temp=4.3;
                WHEN score<95 and score>=90 THEN SET temp=4.0;
                WHEN score<90 and score>=85 THEN SET temp=3.7;
                WHEN score<85 and score>=82 THEN SET temp=3.3;
                WHEN score<82 and score>=78 THEN SET temp=3.0;
                WHEN score<78 and score>=75 THEN SET temp=2.7;
                WHEN score<75 and score>=72 THEN SET temp=2.3;
                WHEN score<72 and score>=68 THEN SET temp=2.0;
                WHEN score<68 and score>=65 THEN SET temp=1.7;
                WHEN score=64 THEN SET temp=1.5;
                WHEN score<64 and score>=61 THEN SET temp=1.3;
                WHEN score=60 THEN SET temp=1.0;
                ELSE SET temp=0.0;
			END CASE;
        END IF;
        SET total_score = total_score + temp * credits;
        SET total_credits = total_credits + credits;
        Until state=1
	END Repeat;
	Set gpa = total_score/total_credits;
	return gpa;
END //
Delimiter ;

Drop Function GPA;
Select GPA("PB21111681");



