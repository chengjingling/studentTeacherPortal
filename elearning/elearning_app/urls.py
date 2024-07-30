from django.urls import path
from . import views
from . import api

urlpatterns = [
    # shared paths
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('my_courses', views.my_courses, name='my_courses'),
    path('my_courses/<str:code>', views.course_details, name='course_details'),
    path('my_courses/<str:code>/<str:filename>/view', views.view_material, name='view_material'),
    path('search_students', views.search_students, name='search_students'),
    path('search_students/<int:id>', views.user_details, name='student_details'),
    path('search_teachers', views.search_teachers, name='search_teachers'),
    path('search_teachers/<int:id>', views.user_details, name='teacher_details'),
    path('chats', views.chats, name='chats'),
    path('chats/<str:room_name>', views.chat, name='chat'),
    path('chats/<str:room_name>/join', views.join_chat, name='join_chat'),
    path('chats/<str:room_name>/leave', views.leave_chat, name='leave_chat'),
    path('notifications', views.notifications, name='notifications'),
    path('profile', views.profile, name='profile'),
    # student paths
    path('available_courses', views.available_courses, name='available_courses'),
    path('available_courses/<str:code>/enrol', views.enrol, name='enrol'),
    path('my_courses/<str:code>/unenrol', views.unenrol, name='unenrol'),
    path('feedback', views.feedback, name='feedback'),
    # teacher paths
    path('my_courses/course/create', views.create_course, name='create_course'),
    path('my_courses/<str:code>/update', views.update_course, name='update_course'),
    path('my_courses/<str:code>/<int:id>/remove', views.remove_student_from_course, name='remove_student_from_course'),
    # api paths
    path('api/app_user/<int:id>', api.AppUserAPI.as_view(), name='app_user_api'),
    path('api/course/<str:code>', api.CourseAPI.as_view(), name='course_api'),
    path('api/material/<str:code>/<int:id>', api.MaterialAPI.as_view(), name='material_api'),
    path('api/feedback/<str:code>', api.FeedbackAPI.as_view(), name='feedback_api'),
    path('api/status', api.StatusAPI.as_view(), name='status_api'),
    path('api/chat/<str:room_name>', api.ChatAPI.as_view(), name='chat_api'),
    path('api/enrol_notification/<int:id>', api.EnrolNotificationAPI.as_view(), name='enrol_notification_api'),
    path('api/material_notification/<int:id>', api.MaterialNotificationAPI.as_view(), name='material_notification_api'),
]