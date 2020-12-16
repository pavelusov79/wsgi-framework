import datetime
import json

from core.templates import render


class Main:

    def __call__(self, request):
        secret = request.get('secret_key', None)
        return '200 OK', render('index.html', secret=secret)


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



