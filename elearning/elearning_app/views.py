from .forms import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import *
import os
from django.core.serializers import serialize

# Create your views here.
def register(request):
    user_form = UserForm()
    profile_form = UserProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return redirect('/')

        else:
            return render(request, 'login_failed.html')

    else:
        return render(request, 'login.html')

def user_logout(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        logout(request)
        messages.success(request, 'User logged out.')
        return redirect('/login')

def index(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        status_form = StatusForm()
        user_details = AppUser.objects.get(user=request.user)

        if user_details.type == 'student':
            unread_notifications = len(MaterialNotification.objects.filter(student=user_details, read=False))
            courses = Course.objects.filter(students=user_details)

        else:
            unread_notifications = len(EnrolNotification.objects.filter(teacher=user_details, read=False))
            courses = Course.objects.filter(teacher=user_details)

        return render(request, 'index.html', {'status_form': status_form, 'unread_notifications': unread_notifications, 'courses': courses, 'user_details': user_details})

def my_courses(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        user_details = AppUser.objects.get(user=request.user)

        if user_details.type == 'student':
            courses = Course.objects.filter(students=user_details)

        else:
            courses = Course.objects.filter(teacher=user_details)

        return render(request, 'my_courses.html', {'courses': courses, 'user_details': user_details})

def course_details(request, code):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        material_form = MaterialForm()
        user_details = AppUser.objects.get(user=request.user)

        try:
            course = Course.objects.get(code=code)

        except Course.DoesNotExist as e:
            course = None

        return render(request, 'course_details.html', {'material_form': material_form, 'course': course, 'user_details': user_details})

def view_material(request, code, filename):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        course = Course.objects.get(code=code)
        material = Material.objects.get(course=course, file='course_materials/'+filename)
        content_type = 'application/' + filename.split('.')[-1]

        with open(material.file.path, 'rb') as file:
            file_content = file.read()

        return HttpResponse(file_content, content_type=content_type)

def search_students(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        students = serialize('json', AppUser.objects.filter(type='student'))
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'search_students.html', {'students': students, 'user_details': user_details})

def search_teachers(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        teachers = serialize('json', AppUser.objects.filter(type='teacher'))
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'search_teachers.html', {'teachers': teachers, 'user_details': user_details})

def user_details(request, id):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'user_details.html', {'id': id, 'user_details': user_details})

def chats(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        chat_form = ChatForm()
        user_details = AppUser.objects.get(user=request.user)
        my_chats = Chat.objects.filter(members=user_details)
        other_chats = Chat.objects.exclude(members=user_details)
        return render(request, 'chats.html', {'chat_form': chat_form, 'my_chats': my_chats, 'other_chats': other_chats, 'user_details': user_details})

def chat(request, room_name):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'chat.html', {'room_name': room_name, 'user_details': user_details})

def join_chat(request, room_name):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        chat = Chat.objects.get(room_name=room_name)
        user_details = AppUser.objects.get(user=request.user)
        chat.members.add(user_details)
        return redirect(f'/chats/{room_name}')

def leave_chat(request, room_name):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        chat = Chat.objects.get(room_name=room_name)
        user_details = AppUser.objects.get(user=request.user)

        if chat.admin != user_details:
            chat.members.remove(user_details)
            messages.success(request, f'Left "{room_name}".')
            return redirect('/chats')

        else:
            return HttpResponse('You are not authorised to perform this action.')

def notifications(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'notifications.html', {'user_details': user_details})

def profile(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'profile.html', {'user_details': user_details})

def available_courses(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        courses = Course.objects.all()
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'available_courses.html', {'courses': courses, 'user_details': user_details})

def enrol(request, code):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        course = Course.objects.get(code=code)
        student = AppUser.objects.get(user=request.user)
        course.students.add(student)
        enrol_notification = EnrolNotification.objects.create(course=course,
                                                              student=student,
                                                              teacher=course.teacher,
                                                              read=False)
        messages.success(request, f'Enrolled to "{course.code} {course.name}".')
        return redirect(f'/my_courses/{course.code}')

def unenrol(request, code):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        course = Course.objects.get(code=code)
        student = AppUser.objects.get(user=request.user)
        course.students.remove(student)
        messages.success(request, f'Unenrolled from "{course.code} {course.name}".')
        return redirect('/my_courses')

def feedback(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        feedback_form = FeedbackForm()
        user_details = AppUser.objects.get(user=request.user)
        courses = Course.objects.filter(students=user_details)
        feedbacks = Feedback.objects.filter(student=user_details)
        return render(request, 'feedback.html', {'feedback_form': feedback_form, 'courses': courses, 'feedbacks': feedbacks, 'user_details': user_details})

def create_course(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        course_form = CourseForm()
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'create_course.html', {'course_form': course_form, 'user_details': user_details})

def update_course(request, code):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        try:
            course = Course.objects.get(code=code)

        except Course.DoesNotExist as e:
            course = None
            
        course_form = CourseForm(instance=course)
        user_details = AppUser.objects.get(user=request.user)
        return render(request, 'update_course.html', {'course_form': course_form, 'course': course, 'user_details': user_details})

def remove_student_from_course(request, code, id):
    if request.user.is_anonymous:
        messages.warning(request, 'Please log in.')
        return redirect('/login')

    elif request.user.is_staff:
        messages.warning(request, 'Cannot access website with admin account.')
        return redirect('/login')

    else:
        course = Course.objects.get(code=code)
        student = AppUser.objects.get(id=id)
        course.students.remove(student)
        messages.success(request, f'"{student.first_name} {student.last_name}" removed from "{course.code} {course.name}".')
        return redirect(f'/my_courses/{course.code}')