import json

from core.templates import render


class Main:

    def __call__(self, request):
        data_list = [
          {"service": "Стрижка женская", "price": "900", "img": "/static/img/female1.png"},
          {"service": "Укладка", "price": "1000", "img": "/static/img/ukladka2.png"},
          {"service": "Окраска любой сложности", "price": "1500", "img": "/static/img/okras1.png"},
          {"service": "Лечение, биоинкрустация волос, ламинирование", "price": "1200", "img": "/static/img/laminir1.png"},
          {"service": "Мужские стрижки", "price": "600", "img": "/static/img/male1.png"},
          {"service": "Детские стрижки", "price": "400", "img": "/static/img/child1.png"},
          {"service": "Услуги лешмейкера", "price": "1800", "img": "/static/img/lesh1.png"},
          {"service": "Услуги перманентного макияжа", "price": "2000", "img": "/static/img/tat1.png"}
        ]
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
        secret = request.get('secret_key', None)
        return '200 OK', render('contacts.html', secret=secret)



