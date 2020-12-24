import views

from core.core import MockApplication

route = {
    '/': views.Main(),
    '/services/': views.Services(),
    '/portfolio/': views.Portfolio(),
    # '/contacts/': views.Contact(),
    '/create-course/': views.CreateCourse(),
    '/create-category/': views.CreateCategory(),
    '/category-list/': views.CategoryList()
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = '123'


front_controllers = [
    secret_controller
]

# application = Application(route, front_controllers)
application = MockApplication(route, front_controllers)

# Запуск:
# gunicorn main:application
