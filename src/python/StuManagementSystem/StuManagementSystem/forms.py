# forms.py
from django import forms
from basedb.models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['cid', 'cname', 'credit', 'type']

class SCForm(forms.ModelForm):
    class Meta:
        model = Sc
        fields = ['sid', 'cid', 'score']

class ProfessionForm(forms.ModelForm):
    class Meta:
        model = Profession
        fields = ['pid', 'pname', 'academy']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['sid', 'sname', 'sex', 'getdate', 'pid', 'phone', 'email']

class InfomForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['sid','type','infomation']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['sid','type','cid']


class ImgForm(forms.Form):
    class Meta:
        model = Image
        fields = ['sid','img']
