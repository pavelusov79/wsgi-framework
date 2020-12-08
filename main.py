from core.core import Application
import views

route = {
    '/': views.Main(),
    '/services/': views.Services(),
    '/portfolio/': views.Portfolio(),
    '/contacts/': views.Contact()
}


def secret_controller(request):
    # пример Front Controller
    request['secret_key'] = '123'


front_controllers = [
    secret_controller
]

application = Application(route, front_controllers)

# Запуск:
# gunicorn main:application
