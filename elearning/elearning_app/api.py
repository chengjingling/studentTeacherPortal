from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from datetime import datetime
import pytz
from .forms import *

class AppUserAPI(generics.GenericAPIView):
    serializer_class = AppUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        type = request.data.get('type')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        photo = request.data.get('photo')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()

        app_user = AppUser.objects.create(user=user,
                                          type=type,
                                          first_name=first_name,
                                          last_name=last_name,
                                          email=email,
                                          photo=photo)

        data = self.get_serializer(app_user).data

        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        try:
            instance = AppUser.objects.get(id=kwargs['id'])

        except AppUser.DoesNotExist as e:
            return Response('app user does not exist', status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = AppUser.objects.get(id=kwargs['id'])

        except AppUser.DoesNotExist as e:
            return Response('app user does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        instance.user.delete()

        return Response('app user deleted', status=status.HTTP_200_OK)

class CourseAPI(generics.GenericAPIView):
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        name = request.data.get('name')
        description = request.data.get('description')
        teacher = AppUser.objects.get(user=request.user)
        code_exists = Course.objects.filter(code=code).exists()

        if not code or not name or not description:
            return Response('missing fields', status=status.HTTP_400_BAD_REQUEST)

        elif code_exists:
            return Response('code exists', status=status.HTTP_400_BAD_REQUEST)

        else:
            instance = Course.objects.create(code=code,
                                             name=name,
                                             description=description,
                                             teacher=teacher)

            data = self.get_serializer(instance).data

            return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(code=kwargs['code'])

        except Course.DoesNotExist as e:
            return Response('course does not exist', status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(course).data

        teacher = AppUser.objects.get(id=data['teacher'])
        teacher_data = AppUserSerializer(teacher).data

        students_data = []

        for id in data['students']:
            student = AppUser.objects.get(id=id)
            student_data = AppUserSerializer(student).data
            students_data.append(student_data)

        app_user = AppUser.objects.get(user=request.user)
        app_user_data = AppUserSerializer(app_user).data

        data['teacher'] = teacher_data
        data['students'] = students_data
        data['app_user'] = app_user_data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        code = request.data.get('code')
        name = request.data.get('name')
        description = request.data.get('description')
        code_exists = Course.objects.filter(code=code).exists()

        if not code or not name or not description:
            return Response('missing fields', status=status.HTTP_400_BAD_REQUEST)

        elif code != kwargs['code'] and code_exists:
            return Response('code exists', status=status.HTTP_400_BAD_REQUEST)

        else:
            try:
                instance = Course.objects.get(code=kwargs['code'])

            except Course.DoesNotExist as e:
                return Response('course does not exist', status=status.HTTP_404_NOT_FOUND)

            instance.code = code
            instance.name = name
            instance.description = description
            instance.save()

            data = self.get_serializer(instance).data

            return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = Course.objects.get(code=kwargs['code'])

        except Course.DoesNotExist as e:
            return Response('course does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.delete()

        return Response('course deleted', status=status.HTTP_200_OK)

class MaterialAPI(generics.ListAPIView):
    serializer_class = MaterialSerializer

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(code=kwargs['code'])
        file = request.data.get('file')
        
        material = Material.objects.create(course=course, file=file)

        for student in course.students.all():
            material_notification = MaterialNotification.objects.create(material=material, student=student, read=False)

        data = self.get_serializer(material).data

        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(code=kwargs['code'])

        except Course.DoesNotExist as e:
            return Response('course does not exist', status=status.HTTP_404_NOT_FOUND)

        materials = Material.objects.filter(course=course)
        materials_data = self.get_serializer(materials, many=True).data

        for i in range(len(materials)):
            materials_data[i]['course'] = CourseSerializer(materials[i].course).data
            materials_data[i]['course']['teacher'] = AppUserSerializer(materials[i].course.teacher).data

        app_user = AppUser.objects.get(user=request.user)
        app_user_data = AppUserSerializer(app_user).data

        data = {}
        data['materials'] = materials_data
        data['app_user'] = app_user_data

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = Material.objects.get(id=kwargs['id'])

        except Material.DoesNotExist as e:
            return Response('material does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.delete()

        return Response('material deleted', status=status.HTTP_200_OK)

class FeedbackAPI(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):
        student = AppUser.objects.get(user=request.user)
        course = Course.objects.get(code=request.data.get('course').split(' ')[0])
        description = request.data.get('description')
        
        instance = Feedback.objects.create(student=student, course=course, description=description)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(code=kwargs['code'])

        except Course.DoesNotExist as e:
            return Response('course does not exist', status=status.HTTP_404_NOT_FOUND)

        feedbacks = Feedback.objects.filter(course=course)
        
        data = self.get_serializer(feedbacks, many=True).data

        for i in range(len(feedbacks)):
            data[i]['student'] = AppUserSerializer(feedbacks[i].student).data

        return Response(data, status=status.HTTP_200_OK)

class StatusAPI(generics.ListAPIView):
    serializer_class = StatusSerializer

    def post(self, request, *args, **kwargs):
        student = AppUser.objects.get(user=request.user)
        timestamp = datetime.now(pytz.timezone('Asia/Singapore'))
        description = request.data.get('description')
        
        instance = Status.objects.create(student=student, timestamp=timestamp, description=description)

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all().order_by('-timestamp')
        
        data = self.get_serializer(statuses, many=True).data

        for i in range(len(statuses)):
            data[i]['student'] = AppUserSerializer(statuses[i].student).data

        return Response(data, status=status.HTTP_200_OK)

class ChatAPI(generics.GenericAPIView):
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        chat_form = ChatForm(request.POST)

        if chat_form.is_valid():
            room_name = request.data.get('room_name')
            admin = AppUser.objects.get(user=request.user)
            
            chat = Chat.objects.create(room_name=room_name, admin=admin, chat_log='')
            chat.members.add(admin)

            data = self.get_serializer(chat).data

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            return Response('room name exists', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(room_name=kwargs['room_name'])

        except Chat.DoesNotExist as e:
            return Response('chat does not exist', status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(chat).data
        data['admin'] = AppUserSerializer(chat.admin).data

        for i in range(len(chat.members.all())):
            data['members'][i] = AppUserSerializer(chat.members.all()[i]).data

        app_user = AppUser.objects.get(user=request.user)
        data['app_user'] = AppUserSerializer(app_user).data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(room_name=kwargs['room_name'])

        except Chat.DoesNotExist as e:
            return Response('chat does not exist', status=status.HTTP_404_NOT_FOUND)

        app_user = AppUser.objects.get(user=request.user)

        chat.chat_log += f'{app_user.first_name} {app_user.last_name}: {request.data.get("message")}\n'
        chat.save()

        data = self.get_serializer(chat).data

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            instance = Chat.objects.get(room_name=kwargs['room_name'])

        except Chat.DoesNotExist as e:
            return Response('chat does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.delete()

        return Response('chat deleted', status=status.HTTP_200_OK)

class EnrolNotificationAPI(generics.ListAPIView):
    serializer_class = EnrolNotificationSerializer

    def get(self, request, *args, **kwargs):
        app_user = AppUser.objects.get(user=request.user)
        notifications = EnrolNotification.objects.filter(teacher=app_user).order_by('-id')

        data = self.get_serializer(notifications, many=True).data

        for i in range(len(notifications)):
            data[i]['course'] = CourseSerializer(notifications[i].course).data
            data[i]['student'] = AppUserSerializer(notifications[i].student).data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            instance = EnrolNotification.objects.get(id=kwargs['id'])

        except EnrolNotification.DoesNotExist as e:
            return Response('enrol notification does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.read = True
        instance.save()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)

class MaterialNotificationAPI(generics.ListAPIView):
    serializer_class = MaterialNotificationSerializer

    def get(self, request, *args, **kwargs):
        app_user = AppUser.objects.get(user=request.user)
        notifications = MaterialNotification.objects.filter(student=app_user).order_by('-id')

        data = self.get_serializer(notifications, many=True).data

        for i in range(len(notifications)):
            data[i]['material'] = MaterialSerializer(notifications[i].material).data
            data[i]['material']['course'] = CourseSerializer(notifications[i].material.course).data

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            instance = MaterialNotification.objects.get(id=kwargs['id'])

        except MaterialNotification.DoesNotExist as e:
            return Response('material notification does not exist', status=status.HTTP_404_NOT_FOUND)

        instance.read = True
        instance.save()

        data = self.get_serializer(instance).data

        return Response(data, status=status.HTTP_200_OK)