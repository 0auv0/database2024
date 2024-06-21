from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.contrib import messages
from django.conf import settings

from basedb.models import *
from .forms import *
user = ""

def hello(request):
    return HttpResponse("Hello world ! ")

def home(request):
    with connection.cursor() as cursor:
        if(request.user.is_superuser):
            cursor.execute("""
                    SELECT *
                    FROM Student, Profession
                    WHERE Student.pid = Profession.pid
            """)
            results = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT *
                FROM Student, Profession
                WHERE Student.pid = Profession.pid
                AND Student.sid = %s
            """, [request.user.username])
            results = cursor.fetchall()

        if request.method == "POST":
            if 'add_stu' in request.POST:
                form = StudentForm(request.POST)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, 'Student added successfully.')
                    except Exception as e:
                        messages.error(request, f'Error adding student: {e}')
                else:
                    messages.error(request, f'Error in student form: {form.errors}')
            elif 'edit_stu' in request.POST:
                student_id = request.POST.get('sid')
                student_edit = get_object_or_404(Student, sid=student_id)
                form = StudentForm(request.POST, instance=student_edit)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, 'Student edited successfully.')
                    except Exception as e:
                        messages.error(request, f'Error editing student: {e}')
                else:
                    messages.error(request, f'Error in student form: {form.errors}')
            elif 'delete_stu' in request.POST:
                student_id = request.POST.get('sid')
                student_delete = Student.objects.filter(sid=student_id)
                for i in student_delete:
                    Sc.objects.filter(sid=i.sid).delete()
                    Info.objects.filter(sid=i.sid).delete()
                    Evaluation.objects.filter(sid=i.sid).delete()
                student_delete.delete()
                messages.success(request, 'Student and related entries deleted successfully.')
            elif 'add_img' in request.POST:
                # sid = request.POST.get('sid')
                # print(sid, request.user.username)
                # if sid != request.user.username:
                #     messages.error(request, 'You can only upload your own image.')
                #     return redirect('home')

                form = ImgForm(request.POST, request.FILES)
                if form.is_valid():
                    new_name = '%s.jpg' % request.user.username
                    where = '%s/img/%s' % (settings.MEDIA_ROOT, new_name)
                    with open(where, 'wb+') as destination:
                        print(where)
                        for chunk in request.FILES['img'].chunks():
                            destination.write(chunk)
                    messages.success(request, 'Image uploaded successfully.')
                else:
                    messages.error(request, 'Error in image form.')

            return redirect('home')
        return render(request, "home.html", {'person':results, 'form':StudentForm(), 'form1':ImgForm()})

def test(request):
    return render(request, "helloworld.html")

def register(request):
    return render(request, "register.html")

def profession(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM Profession
        """)
        results = cursor.fetchall()
    if request.method == "POST":
        if 'add_profession' in request.POST:
            form = ProfessionForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Profession added successfully.')
                except Exception as e:
                    messages.error(request, f'Error adding profession: {e}')
            else:
                messages.error(request, f'Error in profession form: {form.errors}')
        elif 'edit_profession' in request.POST:
            profession_id = request.POST.get('pid')
            profession_edit = get_object_or_404(Profession, pid=profession_id)
            form = ProfessionForm(request.POST, instance=profession_edit)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Profession edited successfully.')
                except Exception as e:
                    messages.error(request, f'Error editing profession: {e}')
            else:
                messages.error(request, f'Error in profession form: {form.errors}')
        elif 'delete_profession' in request.POST:
            profession_id = request.POST.get('pid')
            profession_delete = get_object_or_404(Profession, pid=profession_id)
            student_delete = Student.objects.filter(pid=profession_id)
            for i in student_delete:
                Sc.objects.filter(sid=i.sid).delete()
                Info.objects.filter(sid=i.sid).delete()
                Evaluation.objects.filter(sid=i.sid).delete()

            student_delete.delete()
            profession_delete.delete()
            messages.success(request, 'Profession and related student entries deleted successfully.')
        return redirect('profession_pages')
    return render(request, "profession.html",{'profession': results, 'form': ProfessionForm() })

def info(request):
    with connection.cursor() as cursor:
        if request.user.is_superuser:
            cursor.execute("""
                SELECT *
                FROM Info, Student
                WHERE Info.sid = Student.sid
            """)
        else:
            cursor.execute("""
                SELECT *
                FROM Info, Student
                WHERE Info.sid = Student.sid
                AND Info.sid = %s
            """, [request.user.username])
        results = cursor.fetchall()

        if request.method == "POST":
            if 'add_info' in request.POST:
                sid = request.POST.get('sid')
                type = request.POST.get('type')
                infomation = request.POST.get('infomation')
                rv = 0
                with connection.cursor() as cursor:
                    cursor.callproc('AddInfo', [sid, type, infomation, rv])
                    cursor.execute('SELECT @rv')
                    result = cursor.fetchone()

                    if result and result[0] == 1:
                        messages.error(request, 'Info already exists.')
                    else:
                        messages.success(request, 'Info added successfully.')
                return redirect('info_pages')
            elif 'edit_info' in request.POST:
                student_id = request.POST.get('sid')
                info_type = request.POST.get('type')
                info_info = request.POST.get('infomation')
                info_edit = get_object_or_404(Info, sid=student_id, type=info_type, infomation=info_info)
                form = InfomForm(request.POST, instance=info_edit)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, 'Info edited successfully.')
                    except Exception as e:
                        messages.error(request, f'Error editing info: {e}')
                else:
                    messages.error(request, f'Error in info form: {form.errors}')
            elif 'delete_info' in request.POST:
                student_id = request.POST.get('sid')
                info_type = request.POST.get('type')
                info_info = request.POST.get('infomation')
                # info_delete = get_object_or_404(Info, sid=student_id, type=info_type, infomation=info_info)
                info_delete = Info.objects.filter(sid=student_id, type=info_type, infomation=info_info)
                info_delete.delete()
                messages.success(request, 'Info entry deleted successfully.')
            return redirect('info_pages')
    return render(request, "info.html", {'info': results, 'form': InfomForm()})


def course(request):
    with connection.cursor() as cursor:
        if request.user.is_superuser:
            cursor.execute("""
                SELECT *
                FROM Student, Course, SC
                WHERE Student.sid = SC.sid
                AND Course.cid = SC.cid
            """)
        else:
            cursor.execute("""
                SELECT *
                FROM Student, Course, SC
                WHERE Student.sid = SC.sid
                AND Course.cid = SC.cid
                AND Student.sid = %s
            """, [request.user.username])
        results = cursor.fetchall()

    course_list = Course.objects.all()
    if request.method == "POST":
        if 'add_course' in request.POST:
            return handle_course_add(request)
        elif 'edit_course' in request.POST:
            return handle_course_edit(request)
        elif 'delete_course' in request.POST:
            return handle_course_delete(request)
        elif 'add_Sc' in request.POST:
            return handle_sc_add(request)
        elif 'delete_Sc' in request.POST:
            return handle_sc_delete(request)

    return render(request, "course.html",
                  {'SC': results, 'course': course_list, 'form': CourseForm(), 'form1': SCForm()})


def score(request):
    with connection.cursor() as cursor:
        if request.user.is_superuser:
            cursor.execute("""
                SELECT *
                FROM Student, Course, SC
                WHERE Student.sid = SC.sid
                AND Course.cid = SC.cid
            """)
        else:
            cursor.execute("""
                SELECT *
                FROM Student, Course, SC
                WHERE Student.sid = SC.sid
                AND Course.cid = SC.cid
                AND SC.score is not null
                AND Student.sid = %s
            """, [request.user.username])
        results = cursor.fetchall()

        if request.method == 'POST':
            sid = request.POST.get('sid')
            cid = request.POST.get('cid')
            score = int(request.POST.get('score'))

            try:
                with connection.cursor() as cursor:
                    # 调用存储过程
                    cursor.callproc('ChangeSC', [sid, cid, score, 0])
                    # 获取输出参数的值
                    cursor.execute('SELECT @_ChangeSC_3')
                    rv = cursor.fetchone()[0]

                if rv == 0:
                    messages.success(request, 'SC entry updated successfully.')
                else:
                    messages.success(request, 'SC entry inserted successfully.')

            except Exception as e:
                messages.error(request, f'Error in changing SC entry: {e}')
            return redirect('score_pages')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT GPA(%s)
            """, [request.user.username])
            GPA = cursor.fetchone()[0]

    return render(request, "score.html", {'SC': results, 'gpa':GPA})

def evaluation(request):
    with connection.cursor() as cursor:
        if request.user.is_superuser:
            cursor.execute("""
                SELECT *
                FROM Student, Course, Evaluation
                WHERE Student.sid = Evaluation.sid
                AND Course.cid = Evaluation.cid
            """)
        else:
            cursor.execute("""
                SELECT *
                FROM Student, Course, Evaluation
                WHERE Student.sid = Evaluation.sid
                AND Course.cid = Evaluation.cid
                AND Student.sid = %s
            """, [request.user.username])
        results = cursor.fetchall()

        if request.method == 'POST':
            sid = request.POST.get('sid')
            cid = request.POST.get('cid')
            type = request.POST.get('type')

            if "add_evaluation" in request.POST:
                rv = 0
                with connection.cursor() as cursor:
                    cursor.callproc('AddEval', [sid, cid, type, rv])
                    cursor.execute('SELECT @rv')
                    result = cursor.fetchone()

                    if result and result[0] == 1:
                        messages.error(request, 'Evaluation already exists.')
                    else:
                        messages.success(request, 'Evaluation added successfully.')
            elif "delete_evaluation" in request.POST:
                evaluation_delete = Evaluation.objects.filter(sid=sid, cid=cid, type=type)
                evaluation_delete.delete()
                messages.success(request, 'Evaluation entry deleted successfully.')

            return redirect('evaluation_pages')



    return render(request, "evaluation.html",{'evaluation': results, 'form': EvaluationForm() })

def handle_course_add(request):
    form = CourseForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Course added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding course: {e}')
    return redirect('course_pages')


def handle_course_edit(request):
    course_id = request.POST.get('cid')
    course_edit = get_object_or_404(Course, cid=course_id)
    form = CourseForm(request.POST, instance=course_edit)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Course edited successfully.')
        except Exception as e:
            messages.error(request, f'Error editing course: {e}')
    return redirect('course_pages')


def handle_course_delete(request):
    course_id = request.POST.get('cid')
    course_delete = get_object_or_404(Course, cid=course_id)
    Sc_delete = Sc.objects.filter(cid=course_id)
    Sc_delete.delete()
    course_delete.delete()
    messages.success(request, 'Course and related SC entries deleted successfully.')
    return redirect('course_pages')

def handle_sc_add(request):
    # form = SCForm(request.POST)
    # if form.is_valid():
    #     try:
    #         form.save()
    #         messages.success(request, 'SC added successfully.')
    #     except Exception as e:
    #         messages.error(request, f'Error adding SC: {e}')
    # else:
    #     messages.error(request, f'Error in SC form: {form.errors}')
    sid = request.POST.get('sid')
    cid = request.POST.get('cid')
    rv = 0
    with connection.cursor() as cursor:
        cursor.callproc('AddSC', [sid, cid, None, rv])
        cursor.execute('SELECT @rv')
        result = cursor.fetchone()

        if result and result[0] == 1:
            messages.error(request, 'SC already exists.')
        else:
            messages.success(request, 'SC added successfully.')
    return redirect('course_pages')

def handle_sc_delete(request):
    sid = request.POST.get('sid')
    cid = request.POST.get('cid')
    sc_delete = Sc.objects.filter(sid=sid, cid=cid)
    sc_delete.delete()
    messages.success(request, 'SC entry deleted successfully.')
    return redirect('course_pages')