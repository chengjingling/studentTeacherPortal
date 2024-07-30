from rest_framework.test import APITestCase, APIRequestFactory
from .model_factories import *
from .serializers import *
from .models import *
from .api import *
import json

# Create your tests here.
class UserSerializerTest(APITestCase):
    user1 = None
    user_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.user_serializer = UserSerializer(instance=self.user1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_userSerializerHasCorrectFields(self):
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'username', 'password']))

    def test_userSerializerHasCorrectData(self):
        data = self.user_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['username'], 'marie')

class AppUserSerializerTest(APITestCase):
    user1 = None
    app_user1 = None
    app_user_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.app_user1 = AppUserFactory.create(user=self.user1)
        self.app_user_serializer = AppUserSerializer(instance=self.app_user1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_appUserSerializerHasCorrectFields(self):
        data = self.app_user_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'user', 'type', 'first_name', 'last_name', 'email', 'photo']))

    def test_appUserSerializerHasCorrectData(self):
        data = self.app_user_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['user'], 1)
        self.assertEqual(data['type'], 'student')
        self.assertEqual(data['first_name'], 'Marie')
        self.assertEqual(data['last_name'], 'Todd')
        self.assertEqual(data['email'], 'marie@gmail.com')
        self.assertEqual(data['photo'], '/media/user_photos/user1.jpg')

class CourseSerializerTest(APITestCase):
    user1 = None
    student1 = None
    user2 = None
    student2 = None
    user3 = None
    teacher1 = None
    course1 = None
    course_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='mark')
        self.user2.set_password('Mark123!@#')
        self.student2 = AppUserFactory.create(id=2,
                                              user=self.user2,
                                              type='student',
                                              first_name='Mark',
                                              last_name='Hensley',
                                              email='mark@gmail.com',
                                              photo='user_photos/user2.jpg')
        self.user3 = UserFactory.create(id=3, username='amy')
        self.user3.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=3,
                                              user=self.user3,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.course1.students.add(self.student1)
        self.course1.students.add(self.student2)
        self.course_serializer = CourseSerializer(instance=self.course1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_courseSerializerHasCorrectFields(self):
        data = self.course_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'code', 'name', 'description', 'teacher', 'students']))

    def test_courseSerializerHasCorrectData(self):
        data = self.course_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['code'], 'CM1005')
        self.assertEqual(data['name'], 'Introduction to programming 1')
        self.assertEqual(data['description'], 'This module is focused on basic programming techniques. By taking this module, you will learn how to use the basic elements of computer programming such as variables, conditionals, functions and loops. You will also learn how to create interactive, graphical computer programs. You will also be introduced to basic object-oriented programming techniques. Assessment: Coursework only.')
        self.assertEqual(data['teacher'], 3)
        self.assertEqual(data['students'], [1, 2])

class MaterialSerializerTest(APITestCase):
    user1 = None
    teacher1 = None
    course1 = None
    material1 = None
    material_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create(id=2, username='amy')
        self.user1.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=2,
                                              user=self.user1,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.material1 = MaterialFactory.create(course=self.course1)
        self.material_serializer = MaterialSerializer(instance=self.material1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_materialSerializerHasCorrectFields(self):
        data = self.material_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'course', 'file', 'filename']))

    def test_materialSerializerHasCorrectData(self):
        data = self.material_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['course'], 1)
        self.assertEqual(data['file'], '/media/course_materials/Midterm%20Brief.pdf')

class FeedbackSerializerTest(APITestCase):
    user1 = None
    student1 = None
    user2 = None
    teacher1 = None
    course1 = None
    feedback1 = None
    feedback_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='amy')
        self.user2.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=2,
                                              user=self.user2,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.feedback1 = FeedbackFactory.create(student=self.student1, course=self.course1)
        self.feedback_serializer = FeedbackSerializer(instance=self.feedback1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_feedbackSerializerHasCorrectFields(self):
        data = self.feedback_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'student', 'course', 'description']))

    def test_feedbackSerializerHasCorrectData(self):
        data = self.feedback_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['student'], 1)
        self.assertEqual(data['course'], 1)
        self.assertEqual(data['description'], 'Ms Amy is friendly and provides ample support for her students!')

class StatusSerializerTest(APITestCase):
    user1 = None
    student1 = None
    status1 = None
    status_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.status1 = StatusFactory.create(student=self.student1)
        self.status_serializer = StatusSerializer(instance=self.status1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_statusSerializerHasCorrectFields(self):
        data = self.status_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'student', 'timestamp', 'description', 'formatted_timestamp']))

    def test_statusSerializerHasCorrectData(self):
        data = self.status_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['student'], 1)
        self.assertEqual(data['timestamp'], '2024-02-20T12:24:00+08:00')
        self.assertEqual(data['description'], 'Yay just submitted my CM1015 assignment!')

class ChatSerializerTest(APITestCase):
    user1 = None
    admin1 = None
    user2 = None
    member1 = None
    chat1 = None
    chat_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.admin1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='mark')
        self.user2.set_password('Mark123!@#')
        self.member1 = AppUserFactory.create(id=2,
                                             user=self.user2,
                                             type='student',
                                             first_name='Mark',
                                             last_name='Hensley',
                                             email='mark@gmail.com',
                                             photo='user_photos/user2.jpg')
        self.chat1 = ChatFactory.create(admin=self.admin1)
        self.chat1.members.add(self.admin1)
        self.chat1.members.add(self.member1)
        self.chat_serializer = ChatSerializer(instance=self.chat1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_chatSerializerHasCorrectFields(self):
        data = self.chat_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'room_name', 'admin', 'members', 'chat_log']))

    def test_chatSerializerHasCorrectData(self):
        data = self.chat_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['room_name'], 'CM1005 Assignment 1')
        self.assertEqual(data['admin'], 1)
        self.assertEqual(data['members'], [1, 2])
        self.assertEqual(data['chat_log'], 'Marie Todd: Any ideas for what website we should create?\nMark Hensley: How about a travel website?\n')

class EnrolNotificationSerializerTest(APITestCase):
    user1 = None
    student1 = None
    user2 = None
    teacher1 = None
    course1 = None
    notification1 = None
    enrol_notification_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='amy')
        self.user2.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=2,
                                              user=self.user2,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.notification1 = EnrolNotificationFactory.create(course=self.course1, student=self.student1, teacher=self.teacher1)
        self.enrol_notification_serializer = EnrolNotificationSerializer(instance=self.notification1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_enrolNotificationSerializerHasCorrectFields(self):
        data = self.enrol_notification_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'course', 'student', 'teacher', 'read']))

    def test_enrolNotificationSerializerHasCorrectData(self):
        data = self.enrol_notification_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['course'], 1)
        self.assertEqual(data['student'], 1)
        self.assertEqual(data['teacher'], 2)
        self.assertEqual(data['read'], False)

class MaterialNotificationSerializerTest(APITestCase):
    user1 = None
    student1 = None
    user2 = None
    teacher1 = None
    course1 = None
    material1 = None
    notification1 = None
    material_notification_serializer = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='amy')
        self.user2.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=2,
                                              user=self.user2,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.material1 = MaterialFactory.create(course=self.course1)
        self.notification1 = MaterialNotificationFactory.create(material=self.material1, student=self.student1)
        self.material_notification_serializer = MaterialNotificationSerializer(instance=self.notification1)

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_materialNotificationSerializerHasCorrectFields(self):
        data = self.material_notification_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'material', 'student', 'read']))

    def test_materialNotificationSerializerHasCorrectData(self):
        data = self.material_notification_serializer.data
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['material'], 1)
        self.assertEqual(data['student'], 1)
        self.assertEqual(data['read'], False)

class CreateCourseTest(APITestCase):
    user1 = None
    teacher1 = None
    course1 = None
    good_url = ''
    bad_url = ''
    good_data = {}
    bad_data = {}
    data_with_existing_code = {}
    factory = None
    view = None

    def setUp(self):
        self.user1 = UserFactory.create(id=2, username='amy')
        self.user1.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=2,
                                              user=self.user1,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.good_url = '/api/my_courses/CM1005'
        self.bad_url = '/api/bad_url'
        self.good_data = {
            'code': 'CM1010',
            'name': 'Introduction to programming 2',
            'description': 'This module builds on and extends the programming skill set you developed in Introduction to Programming I. You will study a collection of more extensive, case study programs and you will work on a larger programming project from a pre-existing code base. Assessment: Coursework only.'
        }
        self.bad_data = {
            'field1': '',
            'field2': ''
        }
        self.data_with_existing_code = {
            'code': 'CM1005',
            'name': 'Introduction to programming 1',
            'description': 'This module is focused on basic programming techniques. By taking this module, you will learn how to use the basic elements of computer programming such as variables, conditionals, functions and loops. You will also learn how to create interactive, graphical computer programs. You will also be introduced to basic object-oriented programming techniques. Assessment: Coursework only.'
        }
        self.factory = APIRequestFactory()
        self.view = CourseAPI.as_view()

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_createCourseReturnsSuccess(self):
        request = self.factory.post(self.good_url, self.good_data)
        request.user = self.user1
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

    def test_createCourseReturnsFailureOnBadUrl(self):
        response = self.client.post(self.bad_url, self.good_data, format='multipart')
        self.assertEqual(response.status_code, 404)

    def test_createCourseReturnsFailureOnBadData(self):
        request = self.factory.post(self.good_url, self.bad_data)
        request.user = self.user1
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_createCourseReturnsFailureOnExistingCode(self):
        request = self.factory.post(self.good_url, self.data_with_existing_code)
        request.user = self.user1
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

class RetrieveCourseTest(APITestCase):
    user1 = None
    student1 = None
    user2 = None
    student2 = None
    user3 = None
    teacher1 = None
    course1 = None
    material1 = None
    material2 = None
    feedback1 = None
    feedback2 = None
    good_url = ''
    bad_url = ''
    url_with_nonexistent_code = ''
    expected_data = {}
    factory = None
    view = None

    def setUp(self):
        self.user1 = UserFactory.create()
        self.user1.set_password('Marie123!@#')
        self.student1 = AppUserFactory.create(user=self.user1)
        self.user2 = UserFactory.create(id=2, username='mark')
        self.user2.set_password('Mark123!@#')
        self.student2 = AppUserFactory.create(id=2,
                                              user=self.user2,
                                              type='student',
                                              first_name='Mark',
                                              last_name='Hensley',
                                              email='mark@gmail.com',
                                              photo='user_photos/user2.jpg')
        self.user3 = UserFactory.create(id=3, username='amy')
        self.user3.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=3,
                                              user=self.user3,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.course1.students.add(self.student1)
        self.course1.students.add(self.student2)
        self.good_url = '/api/my_courses/CM1005'
        self.bad_url = '/api/bad_url'
        self.url_with_nonexistent_code = '/api/my_courses/CM1010'
        self.expected_data = {
            'id': 1,
            'code': 'CM1005',
            'name': 'Introduction to programming 1',
            'description': 'This module is focused on basic programming techniques. By taking this module, you will learn how to use the basic elements of computer programming such as variables, conditionals, functions and loops. You will also learn how to create interactive, graphical computer programs. You will also be introduced to basic object-oriented programming techniques. Assessment: Coursework only.',
            'teacher': {
                'id': 3,
                'user': 3,
                'type': 'teacher',
                'first_name': 'Amy',
                'last_name': 'Osborn',
                'email': 'amy@gmail.com',
                'photo': '/media/user_photos/user6.jpg'
            },
            'students': [
                {
                    'id': 1,
                    'user': 1,
                    'type': 'student',
                    'first_name': 'Marie',
                    'last_name': 'Todd',
                    'email': 'marie@gmail.com',
                    'photo': '/media/user_photos/user1.jpg'
                },
                {
                    'id': 2,
                    'user': 2,
                    'type': 'student',
                    'first_name': 'Mark',
                    'last_name': 'Hensley',
                    'email': 'mark@gmail.com',
                    'photo': '/media/user_photos/user2.jpg'
                }
            ],
            'app_user': {
                'id': 3,
                'user': 3,
                'type': 'teacher',
                'first_name': 'Amy',
                'last_name': 'Osborn',
                'email': 'amy@gmail.com',
                'photo': '/media/user_photos/user6.jpg'
            }
        }
        self.factory = APIRequestFactory()
        self.view = CourseAPI.as_view()

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_retrieveCourseReturnsSuccess(self):
        self.maxDiff = None
        request = self.factory.get(self.good_url)
        request.user = self.user3
        response = self.view(request, code='CM1005')
        self.assertEqual(response.status_code, 200)
        response.render()
        data = json.loads(response.content)
        self.assertEqual(data, self.expected_data)

    def test_retrieveCourseReturnsFailureOnBadUrl(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_retrieveCourseReturnsFailureOnNonexistentCode(self):
        request = self.factory.get(self.url_with_nonexistent_code)
        request.user = self.user3
        response = self.view(request, code='CM1010')
        self.assertEqual(response.status_code, 404)

class UpdateCourseTest(APITestCase):
    user1 = None
    teacher1 = None
    course1 = None
    course2 = None
    good_url = ''
    bad_url = ''
    url_with_nonexistent_code = ''
    good_data = {}
    bad_data = {}
    data_with_existing_code = {}
    factory = None
    view = None

    def setUp(self):
        self.user1 = UserFactory.create(id=1, username='amy')
        self.user1.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=1,
                                              user=self.user1,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.course2 = CourseFactory.create(id=2,
                                            code='CM1010',
                                            name='Introduction to programming 2',
                                            description='This module builds on and extends the programming skill set you developed in Introduction to Programming I. You will study a collection of more extensive, case study programs and you will work on a larger programming project from a pre-existing code base. Assessment: Coursework only.',
                                            teacher=self.teacher1)
        self.good_url = '/api/my_courses/CM1005'
        self.bad_url = '/api/bad_url'
        self.url_with_nonexistent_code = '/api/my_courses/CM0000'
        self.good_data = {
            'code': 'CM1015',
            'name': 'Computational mathematics',
            'description': 'Understanding the manner in which computational systems represent and process numbers is critical to working effectively in the computational domain. Applied areas of computing which you will study in this programme such as graphics, data programming and signal processing depend upon a solid understanding of linear algebra and geometry. Assessment: ONE two-hour unseen written examinations and coursework.'
        }
        self.bad_data = {
            'field1': '',
            'field2': ''
        }
        self.data_with_existing_code = {
            'code': 'CM1010',
            'name': 'Introduction to programming 2',
            'description': 'This module builds on and extends the programming skill set you developed in Introduction to Programming I. You will study a collection of more extensive, case study programs and you will work on a larger programming project from a pre-existing code base. Assessment: Coursework only.'
        }
        self.factory = APIRequestFactory()
        self.view = CourseAPI.as_view()

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_updateCourseReturnsSuccess(self):
        request = self.factory.put(self.good_url, self.good_data)
        request.user = self.user1
        response = self.view(request, code='CM1005')
        self.assertEqual(response.status_code, 200)

    def test_updateCourseReturnsFailureOnBadUrl(self):
        response = self.client.put(self.bad_url, self.good_data, format='multipart')
        self.assertEqual(response.status_code, 404)

    def test_updateCourseReturnsFailureOnNonexistentCode(self):
        request = self.factory.put(self.url_with_nonexistent_code, self.good_data)
        request.user = self.user1
        response = self.view(request, code='CM0000')
        self.assertEqual(response.status_code, 404)

    def test_updateCourseReturnsFailureOnBadData(self):
        request = self.factory.put(self.good_url, self.bad_data)
        request.user = self.user1
        response = self.view(request, code='CM1005')
        self.assertEqual(response.status_code, 400)

    def test_updateCourseReturnsFailureOnExistingCode(self):
        request = self.factory.put(self.good_url, self.data_with_existing_code)
        request.user = self.user1
        response = self.view(request, code='CM1005')
        self.assertEqual(response.status_code, 400)

class DeleteCourseTest(APITestCase):
    user1 = None
    teacher1 = None
    course1 = None
    good_url = ''
    bad_url = ''
    url_with_nonexistent_code = ''
    factory = None
    view = None

    def setUp(self):
        self.user1 = UserFactory.create(id=1, username='amy')
        self.user1.set_password('Amy123!@#')
        self.teacher1 = AppUserFactory.create(id=1,
                                              user=self.user1,
                                              type='teacher',
                                              first_name='Amy',
                                              last_name='Osborn',
                                              email='amy@gmail.com',
                                              photo='user_photos/user6.jpg')
        self.course1 = CourseFactory.create(teacher=self.teacher1)
        self.good_url = '/api/my_courses/CM1005'
        self.bad_url = '/api/bad_url'
        self.url_with_nonexistent_code = '/api/my_courses/CM0000'
        self.factory = APIRequestFactory()
        self.view = CourseAPI.as_view()

    def tearDown(self):
        User.objects.all().delete()
        AppUser.objects.all().delete()
        Course.objects.all().delete()
        Material.objects.all().delete()
        Feedback.objects.all().delete()
        Status.objects.all().delete()
        Chat.objects.all().delete()
        EnrolNotification.objects.all().delete()
        MaterialNotification.objects.all().delete()
        UserFactory.reset_sequence(0)
        AppUserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        MaterialFactory.reset_sequence(0)
        FeedbackFactory.reset_sequence(0)
        StatusFactory.reset_sequence(0)
        ChatFactory.reset_sequence(0)
        EnrolNotificationFactory.reset_sequence(0)
        MaterialNotificationFactory.reset_sequence(0)

    def test_deleteCourseReturnsSuccess(self):
        request = self.factory.delete(self.good_url)
        request.user = self.user1
        response = self.view(request, code='CM1005')
        self.assertEqual(response.status_code, 200)

    def test_deleteCourseReturnsFailureOnBadUrl(self):
        response = self.client.delete(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_deleteCourseReturnsFailureOnNonexistentCode(self):
        request = self.factory.delete(self.url_with_nonexistent_code)
        request.user = self.user1
        response = self.view(request, code='CM0000')
        self.assertEqual(response.status_code, 404)