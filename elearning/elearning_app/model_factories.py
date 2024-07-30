import factory
from .models import *
from pytz import timezone
from datetime import datetime

class UserFactory(factory.django.DjangoModelFactory):
    id = 1
    username = 'marie'

    class Meta:
        model = User

class AppUserFactory(factory.django.DjangoModelFactory):
    id = 1
    type = 'student'
    first_name = 'Marie'
    last_name = 'Todd'
    email = 'marie@gmail.com'
    photo = 'user_photos/user1.jpg'

    class Meta:
        model = AppUser

class CourseFactory(factory.django.DjangoModelFactory):
    id = 1
    code = 'CM1005'
    name = 'Introduction to programming 1'
    description = 'This module is focused on basic programming techniques. By taking this module, you will learn how to use the basic elements of computer programming such as variables, conditionals, functions and loops. You will also learn how to create interactive, graphical computer programs. You will also be introduced to basic object-oriented programming techniques. Assessment: Coursework only.'

    class Meta:
        model = Course

class MaterialFactory(factory.django.DjangoModelFactory):
    id = 1
    file = 'course_materials/Midterm Brief.pdf'

    class Meta:
        model = Material

class FeedbackFactory(factory.django.DjangoModelFactory):
    id = 1
    description = 'Ms Amy is friendly and provides ample support for her students!'

    class Meta:
        model = Feedback

class StatusFactory(factory.django.DjangoModelFactory):
    id = 1
    timestamp = timezone('Asia/Singapore').localize(datetime(2024, 2, 20, 12, 24, 0))
    description = 'Yay just submitted my CM1015 assignment!'

    class Meta:
        model = Status

class ChatFactory(factory.django.DjangoModelFactory):
    id = 1
    room_name = 'CM1005 Assignment 1'
    chat_log = 'Marie Todd: Any ideas for what website we should create?\nMark Hensley: How about a travel website?\n'

    class Meta:
        model = Chat

class EnrolNotificationFactory(factory.django.DjangoModelFactory):
    id = 1
    read = False

    class Meta:
        model = EnrolNotification

class MaterialNotificationFactory(factory.django.DjangoModelFactory):
    id = 1
    read = False

    class Meta:
        model = MaterialNotification