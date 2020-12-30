import datetime
import json

from core.templates import render
# from main import application
from models import TrainingSite, BaseSerializer, EmailNotifier, SmsNotifier
from loggin_mod import debug, Logger, fake
from core.cbv import CreateView, ListView


site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@fake
class Main:

    def __call__(self, request):
        logger.log('Список курсов')
        secret = request.get('secret_key', None)
        categories = site.categories
        return '200 OK', render('index.html', objects_list=site.courses, categories=categories)


@debug
class CreateCourse:

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            category_id = data.get('category_id')
            print(category_id)
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)
            # редирект?
            # return '302 Moved Temporarily', render('create_course.html')
            # Для начала можно без него
            return '200 OK', render('create_course.html')
        else:
            categories = site.categories
            return '200 OK', render('create_course.html', categories=categories)


@debug
class CreateCategory:

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            # редирект?
            # return '302 Moved Temporarily', render('create_course.html')
            # Для начала можно без него
            return '200 OK', render('create_category.html')
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


@debug
class CategoryList:

    def __call__(self, request):
        logger.log('Список категорий')
        secret = request.get('secret_key', None)
        return '200 OK', render('category_list.html', objects_list=site.categories)


class Services:

    def __call__(self, request):
        with open("static/data.json") as f:
            data_json = json.load(f)
        # secret = request.get('secret_key', None)
        # context = [{'data_json': data_json}, {'secret': secret}]
        return '200 OK', render('price.html', data_json=data_json)


class Portfolio:

    def __call__(self, request):
        secret = request.get('secret_key', None)
        return '200 OK', render('portfolio.html', secret=secret)


# @application.add_route('/contacts/')
class Contact:

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            tel = data['tel']
            service = data['servise']
            date = data['date']
            time = data['time']
            # print(f'Нам пришла заявка от {name}, конт. тел: {tel}\nзапись на услугу: '
            #       f' {service}\nдата: {date}, время: {time}')
            with open("static/data_from_post.txt", 'a') as f:
                f.write(f'{datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")} заявка от'
                        f' {name}, конт. тел: {tel}\nзапись на услугу: '
                        f'{service}\nдата: {date}, время: {time}\n\n')
        secret = request.get('secret_key', None)
        return '200 OK', render('contacts.html', secret=secret)


class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)
