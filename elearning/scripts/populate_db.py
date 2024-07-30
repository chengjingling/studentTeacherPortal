import sys
import os
import django
from pytz import timezone
from datetime import datetime

sys.path.append('/Users/jingling/Desktop/SIM/Y3S1/CM3035 Advanced web development/Finals/FINAL_PROJECT/elearning')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

from django.contrib.auth.models import User
from elearning_app.models import *

User.objects.all().delete()
AppUser.objects.all().delete()
Course.objects.all().delete()
Material.objects.all().delete()
Feedback.objects.all().delete()

user_photos = ['user1.jpg', 'user2.jpg', 'user3.jpg', 'user4.jpg', 'user5.jpg', 'user6.jpg', 'user7.jpg', 'user8.jpg', 'user9.jpg', 'user10.jpg']

for filename in os.listdir('media/user_photos'):
    if filename not in user_photos:
        os.unlink(os.path.join('media/user_photos', filename))

course_materials = [
    'Midterm Brief.pdf',
    'Endterm Brief.pdf',
    'CM2010 Past Exam 2022-09.pdf',
    'CM2010 Past Exam 2022-03.pdf',
    'CM2010 Past Exam 2021-09.pdf',
    'CM2010 Past Exam 2021-03.pdf',
    '01 - CM2015 - Introduction to Data Programming (2022-10).pdf',
    '02 - CM2015 - Variables, control flow and functions (2022-10).pdf',
    '03 - CM2015 - Data structures (2022-10).pdf',
    '04 - CM2015 - Reading and writing data on the filesystem (2022-10).pdf',
    '05 - CM2015 - Retrieving data from the web (2022-10).pdf',
    '06 - CM2015 - Retrieving data from databases using query languages (2022-10).pdf',
    '07 - CM2015 - Cleaning and restructuring data (2022-10).pdf',
    '08 - CM2015 - Cleaning and restructuring data (2022-10).pdf',
    '09 - CM2015 - Data plotting (2022-10).pdf',
    '10 - CM2015 - Version control systems (2022-10).pdf'
]

for filename in os.listdir('media/course_materials'):
    if filename not in course_materials:
        os.unlink(os.path.join('media/course_materials', filename))

superuser = User.objects.create_superuser(username='admin')
superuser.set_password('Admin123!@#')
superuser.save()

user1 = User.objects.create(username='marie')
user1.set_password('Marie123!@#')
user1.save()
appuser1 = AppUser.objects.create(id=1,
                                  user=user1,
                                  type='student',
                                  first_name='Marie',
                                  last_name='Todd',
                                  email='marie@gmail.com',
                                  photo='user_photos/user1.jpg')
appuser1.save()

user2 = User.objects.create(username='mark')
user2.set_password('Mark123!@#')
user2.save()
appuser2 = AppUser.objects.create(id=2,
                                  user=user2,
                                  type='student',
                                  first_name='Mark',
                                  last_name='Hensley',
                                  email='mark@gmail.com',
                                  photo='user_photos/user2.jpg')
appuser2.save()

user3 = User.objects.create(username='hilary')
user3.set_password('Hilary123!@#')
user3.save()
appuser3 = AppUser.objects.create(id=3,
                                  user=user3,
                                  type='student',
                                  first_name='Hilary',
                                  last_name='Hunter',
                                  email='hilary@gmail.com',
                                  photo='user_photos/user3.jpg')
appuser3.save()

user4 = User.objects.create(username='shelia')
user4.set_password('Shelia123!@#')
user4.save()
appuser4 = AppUser.objects.create(id=4,
                                  user=user4,
                                  type='student',
                                  first_name='Shelia',
                                  last_name='Chan',
                                  email='shelia@gmail.com',
                                  photo='user_photos/user4.jpg')
appuser4.save()

user5 = User.objects.create(username='clarissa')
user5.set_password('Clarissa123!@#')
user5.save()
appuser5 = AppUser.objects.create(id=5,
                                  user=user5,
                                  type='student',
                                  first_name='Clarissa',
                                  last_name='Carlson',
                                  email='clarissa@gmail.com',
                                  photo='user_photos/user5.jpg')
appuser5.save()

user6 = User.objects.create(username='amy')
user6.set_password('Amy123!@#')
user6.save()
appuser6 = AppUser.objects.create(id=6,
                                  user=user6,
                                  type='teacher',
                                  first_name='Amy',
                                  last_name='Osborn',
                                  email='amy@gmail.com',
                                  photo='user_photos/user6.jpg')
appuser6.save()

user7 = User.objects.create(username='lynne')
user7.set_password('Lynne123!@#')
user7.save()
appuser7 = AppUser.objects.create(id=7,
                                  user=user7,
                                  type='teacher',
                                  first_name='Lynne',
                                  last_name='Hanson',
                                  email='lynne@gmail.com',
                                  photo='user_photos/user7.jpg')
appuser7.save()

user8 = User.objects.create(username='wilson')
user8.set_password('Wilson123!@#')
user8.save()
appuser8 = AppUser.objects.create(id=8,
                                  user=user8,
                                  type='teacher',
                                  first_name='Wilson',
                                  last_name='Reyes',
                                  email='wilson@gmail.com',
                                  photo='user_photos/user8.jpg')
appuser8.save()

user9 = User.objects.create(username='charles')
user9.set_password('Charles123!@#')
user9.save()
appuser9 = AppUser.objects.create(id=9,
                                  user=user9,
                                  type='teacher',
                                  first_name='Charles',
                                  last_name='Duran',
                                  email='charles@gmail.com',
                                  photo='user_photos/user9.jpg')
appuser9.save()

user10 = User.objects.create(username='sebastian')
user10.set_password('Sebastian123!@#')
user10.save()
appuser10 = AppUser.objects.create(id=10,
                                   user=user10,
                                   type='teacher',
                                   first_name='Sebastian',
                                   last_name='Barrett',
                                   email='sebastian@gmail.com',
                                   photo='user_photos/user10.jpg')
appuser10.save()

course1 = Course.objects.create(id=1,
                                code='CM1005',
                                name='Introduction to programming 1',
                                description='This module is focused on basic programming techniques. By taking this module, you will learn how to use the basic elements of computer programming such as variables, conditionals, functions and loops. You will also learn how to create interactive, graphical computer programs. You will also be introduced to basic object-oriented programming techniques. Assessment: Coursework only.',
                                teacher=appuser7)
course1.students.add(appuser1)
course1.students.add(appuser2)
course1.students.add(appuser3)
course1.save()

course2 = Course.objects.create(id=2,
                                code='CM1010',
                                name='Introduction to programming 2',
                                description='This module builds on and extends the programming skill set you developed in Introduction to Programming I. You will study a collection of more extensive, case study programs and you will work on a larger programming project from a pre-existing code base. Assessment: Coursework only.',
                                teacher=appuser7)
course2.students.add(appuser4)
course2.students.add(appuser5)
course2.save()

course3 = Course.objects.create(id=3,
                                code='CM1015',
                                name='Computational mathematics',
                                description='Understanding the manner in which computational systems represent and process numbers is critical to working effectively in the computational domain. Applied areas of computing which you will study in this programme such as graphics, data programming and signal processing depend upon a solid understanding of linear algebra and geometry. Assessment: ONE two-hour unseen written examinations and coursework.',
                                teacher=appuser7)
course3.students.add(appuser1)
course3.students.add(appuser2)
course3.students.add(appuser3)
course3.save()

course4 = Course.objects.create(id=4,
                                code='CM1020',
                                name='Discrete mathematics',
                                description='Discrete mathematics covers mathematical topics relating to discrete structures and processes that students of computer science will encounter throughout their study. It includes topics such as set theory, logic, functions, series, recursion and induction, graphs, and trees. Assessment: ONE two-hour unseen written examinations and coursework.',
                                teacher=appuser7)
course4.students.add(appuser4)
course4.students.add(appuser5)
course4.save()

course5 = Course.objects.create(id=5,
                                code='CM2005',
                                name='Object oriented programming',
                                description='You will learn what objects and classes are and how to write your classes. You will see how objects can interact with each other, including defining and implementing interfaces to control the interaction. You will learn how to use inheritance to inherit and extend functionality from parent classes. You will learn how to write code according to style guidelines and how to write formal code documentation. Assessment: Coursework only.',
                                teacher=appuser6)
course5.students.add(appuser1)
course5.students.add(appuser2)
course5.students.add(appuser3)
course5.save()

course6 = Course.objects.create(id=6,
                                code='CM2010',
                                name='Software design and development',
                                description='This module aims to advance your software development skills so that you can write more robust and complicated programs. You will learn how to use a range of programming techniques to check the data before processing it. You will learn about test-driven development, where you write tests for your code, and write the code itself, in parallel. You will also learn how to use software versioning tools to manage a software project as it develops. Assessment: ONE two-hour unseen written examinations and coursework.',
                                teacher=appuser6)
course6.students.add(appuser4)
course6.students.add(appuser5)
course6.save()

course7 = Course.objects.create(id=7,
                                code='CM2015',
                                name='Programming with data',
                                description='This module will show you how to work with data: getting data from a variety of sources, visualising data in compelling, informative ways, processing data to make it useful and shareable, and reasoning with data to test hypotheses and make parameterised predictions. The module will also introduce you to a new language and programming environment that is well-adapted to languages for these applications. Assessment: ONE two-hour unseen written examinations and coursework.',
                                teacher=appuser6)
course7.students.add(appuser1)
course7.students.add(appuser2)
course7.students.add(appuser3)
course7.save()

course8 = Course.objects.create(id=8,
                                code='CM2020',
                                name='Agile software projects',
                                description='This module aims to provide insights and practice in software development using contemporary methods to produce software that meets the needs of users and supports an organisation’s business function. The module will enable you to gain competence in the conceptualisation of a technology-based solution to a real-world problem, fulfilling the requirements of users and taking constraints imposed by the prevailing and foreseen market conditions and lessons learned from prototypes into account. Assessment: Coursework only.',
                                teacher=appuser6)
course8.students.add(appuser1)
course8.students.add(appuser2)
course8.students.add(appuser3)
course8.students.add(appuser4)
course8.students.add(appuser5)
course8.save()

course9 = Course.objects.create(id=9,
                                code='CM3005',
                                name='Data science',
                                description='By taking this module, you will be working with different types of data, processing text data and gaining a data science skillset. With these skillsets, you will be able to generate plots and interactive visualisations of data and how to apply statistical methods to the interpretation of results. You will also learn about a range of application domains for data science. Assessment: ONE two-hour unseen written examinations and coursework.',
                                teacher=appuser8)
course9.students.add(appuser1)
course9.students.add(appuser2)
course9.students.add(appuser3)
course9.save()

course10 = Course.objects.create(id=10,
                                 code='CM3010',
                                 name='Databases and advanced data techniques',
                                 description='You will learn how to use SQL and NoSQL databases to store tabular data and documents; audio and video data, and the challenges of working with this kind of data. Assessment: ONE two-hour unseen written examinations and coursework.',
                                 teacher=appuser8)
course10.students.add(appuser4)
course10.students.add(appuser5)
course10.save()

course11 = Course.objects.create(id=11,
                                 code='CM3015',
                                 name='Machine learning and neural networks',
                                 description='You will learn how to solve common machine learning problems such as regression, classification, clustering, matrix completion and pattern recognition. You will learn about neural networks and how they can be trained and optimised, including an exploration of deep neural networks. You will learn about machine learning and neural network software libraries that allow you to develop machine learning systems rapidly, and how to verify and evaluate the results. Assessment: Coursework only.',
                                 teacher=appuser8)
course11.students.add(appuser1)
course11.students.add(appuser2)
course11.students.add(appuser3)
course11.save()

course12 = Course.objects.create(id=12,
                                 code='CM3020',
                                 name='Artificial intelligence',
                                 description='This module is focused on Artificial Intelligence techniques. You will become familiar with the foundations of agent-based approaches to software design, decision making and problem solving including under uncertainty thru the topics covered in this module. Assessment: ONE two-hour unseen written examinations and coursework.',
                                 teacher=appuser8)
course12.students.add(appuser4)
course12.students.add(appuser5)
course12.save()

material1 = Material.objects.create(id=1,
                                    course=course5,
                                    file='course_materials/Midterm Brief.pdf')
material1.save()

material2 = Material.objects.create(id=2,
                                    course=course5,
                                    file='course_materials/Endterm Brief.pdf')
material2.save()

material3 = Material.objects.create(id=3,
                                    course=course6,
                                    file='course_materials/CM2010 Past Exam 2022-09.pdf')
material3.save()

material4 = Material.objects.create(id=4,
                                    course=course6,
                                    file='course_materials/CM2010 Past Exam 2022-03.pdf')
material4.save()

material5 = Material.objects.create(id=5,
                                    course=course6,
                                    file='course_materials/CM2010 Past Exam 2021-09.pdf')
material5.save()

material6 = Material.objects.create(id=6,
                                    course=course6,
                                    file='course_materials/CM2010 Past Exam 2021-03.pdf')
material6.save()

material7 = Material.objects.create(id=7,
                                    course=course7,
                                    file='course_materials/01 - CM2015 - Introduction to Data Programming (2022-10).pdf')
material7.save()

material8 = Material.objects.create(id=8,
                                    course=course7,
                                    file='course_materials/02 - CM2015 - Variables, control flow and functions (2022-10).pdf')
material8.save()

material9 = Material.objects.create(id=9,
                                    course=course7,
                                    file='course_materials/03 - CM2015 - Data structures (2022-10).pdf')
material9.save()

material10 = Material.objects.create(id=10,
                                     course=course7,
                                     file='course_materials/04 - CM2015 - Reading and writing data on the filesystem (2022-10).pdf')
material10.save()

material11 = Material.objects.create(id=11,
                                     course=course7,
                                     file='course_materials/05 - CM2015 - Retrieving data from the web (2022-10).pdf')
material11.save()

material12 = Material.objects.create(id=12,
                                     course=course7,
                                     file='course_materials/06 - CM2015 - Retrieving data from databases using query languages (2022-10).pdf')
material12.save()

material13 = Material.objects.create(id=13,
                                     course=course7,
                                     file='course_materials/07 - CM2015 - Cleaning and restructuring data (2022-10).pdf')
material13.save()

material14 = Material.objects.create(id=14,
                                     course=course7,
                                     file='course_materials/08 - CM2015 - Cleaning and restructuring data (2022-10).pdf')
material14.save()

material15 = Material.objects.create(id=15,
                                     course=course7,
                                     file='course_materials/09 - CM2015 - Data plotting (2022-10).pdf')
material15.save()

material16 = Material.objects.create(id=16,
                                     course=course7,
                                     file='course_materials/10 - CM2015 - Version control systems (2022-10).pdf')
material16.save()

feedback1 = Feedback.objects.create(id=1,
                                    student=appuser1,
                                    course=course5,
                                    description='Ms Amy is friendly and provides ample support for her students!')
feedback1.save()

feedback2 = Feedback.objects.create(id=2,
                                    student=appuser2,
                                    course=course5,
                                    description='This course has a heavy workload, it is a bit stressful :(')
feedback2.save()

status1 = Status.objects.create(id=1,
                                student=appuser3,
                                timestamp=timezone('Asia/Singapore').localize(datetime(2024, 2, 20, 12, 24, 0)),
                                description='Yay just submitted my CM1015 assignment!')
status1.save()

status2 = Status.objects.create(id=2,
                                student=appuser4,
                                timestamp=timezone('Asia/Singapore').localize(datetime(2024, 2, 22, 12, 35, 0)),
                                description='CM2010 exam tomorrow, feeling nervous :(')
status2.save()

chat1 = Chat.objects.create(id=1,
                            room_name='CM1010 Chat',
                            admin=appuser6,
                            chat_log='Amy Osborn: Hello students, welcome to CM1010 Introduction to programming 2!\nAmy Osborn: You may use this chat to ask me any questions you have relating to the course.\nShelia Chan: Hello :)\nClarissa Carlson: Hi Ms Amy!\n')
chat1.members.add(appuser6)
chat1.members.add(appuser4)
chat1.members.add(appuser5)
chat1.save()

chat2 = Chat.objects.create(id=2,
                            room_name='CM2020 Group Project',
                            admin=appuser1,
                            chat_log='Marie Todd: Any ideas for what website we should create?\nMark Hensley: How about a travel website?\nHilary Hunter: Or we could do an e-commerce website\n')
chat2.members.add(appuser1)
chat2.members.add(appuser2)
chat2.members.add(appuser3)
chat2.members.add(appuser4)
chat2.members.add(appuser5)
chat2.save()

notification1 = EnrolNotification.objects.create(id=1,
                                                 course=course3,
                                                 student=appuser1,
                                                 teacher=appuser6,
                                                 read=True)
notification1.save()

notification2 = EnrolNotification.objects.create(id=2,
                                                 course=course3,
                                                 student=appuser2,
                                                 teacher=appuser6,
                                                 read=False)
notification2.save()

notification3 = MaterialNotification.objects.create(id=1,
                                                    material=material1,
                                                    student=appuser1,
                                                    read=True)
notification3.save()

notification4 = MaterialNotification.objects.create(id=2,
                                                    material=material2,
                                                    student=appuser1,
                                                    read=False)
notification4.save()