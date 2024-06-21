from django.db import models

# Create your models here.
class Course(models.Model):
    cid = models.CharField(primary_key=True, max_length=10)
    cname = models.CharField(max_length=20)
    credit = models.IntegerField()
    type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'

class Evaluation(models.Model):
    sid = models.OneToOneField('Student', models.DO_NOTHING, db_column='sid', primary_key=True)  # The composite primary key (sid, type) found, that is not supported. The first column is selected.
    type = models.IntegerField()
    cid = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'evaluation'
        unique_together = (('sid', 'type'),)


class Info(models.Model):
    sid = models.OneToOneField('Student', models.DO_NOTHING, db_column='sid', primary_key=True)  # The composite primary key (sid, type, infomation) found, that is not supported. The first column is selected.
    type = models.CharField(max_length=8)
    infomation = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'info'
        unique_together = (('sid', 'type', 'infomation'),)


class Profession(models.Model):
    pid = models.CharField(primary_key=True, max_length=10)
    pname = models.CharField(max_length=20)
    academy = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'profession'


class Sc(models.Model):
    sid = models.OneToOneField('Student', models.DO_NOTHING, db_column='sid', primary_key=True)  # The composite primary key (sid, cid) found, that is not supported. The first column is selected.
    cid = models.ForeignKey(Course, models.DO_NOTHING, db_column='cid')
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc'
        unique_together = (('sid', 'cid'),)


class Student(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
    sname = models.CharField(max_length=20)
    sex = models.CharField(max_length=2)
    getdate = models.DateField()
    pid = models.ForeignKey(Profession, models.DO_NOTHING, db_column='pid')
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Image(models.Model):
    img = models.ImageField(upload_to='img/')  # 设置图片上传路径

