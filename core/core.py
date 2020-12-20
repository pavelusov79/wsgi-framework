import chardet
import urllib.parse


class Application:

    def parse_input_data(self, data: str):
        result = {}
        if data:
            data = urllib.parse.unquote_plus(data)
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v

        return result

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            get_encoding = chardet.detect(data)
            data_str = data.decode(get_encoding['encoding'])
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, route: dict, front_controllers: list):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.route = route
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        # текущий url
        path = env['PATH_INFO']
        if path[-1] != '/':
            path = path + '/'

        # Получаем все данные запроса
        method = env['REQUEST_METHOD']
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)
        query_string = env['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.route:
            # получаем view по url
            view = self.route[path]
            request = {}
            # добавляем параметры запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                controller(request)
            # вызываем view, получаем результат
            code, text = view(request)
            # возвращаем заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа
            return [text.encode('utf-8')]
        else:
            # Если url нет в urlpatterns - то страница не найдена
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b"Not Found"]


class DebugApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)
        # super().__call__(env, start_response)
    #
    # def add_route(self, url):
    #     def inner(view):
    #         self.urlpatterns[url] = view
    #         self.application.urlpatterns[url] = view
    #
    #     return inner


class MockApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        # start_response('200 OK', [('Content-Type', 'text/html')])
        # return [b'Hello from Mock']
        return self.application(env, start_response)
