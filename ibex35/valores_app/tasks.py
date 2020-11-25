from time import sleep
import datetime
import pytz
from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Valor


@shared_task
def create_valor():
    print("creating data")
    resp = requests.get(url="https://www.bolsamadrid.es/ing/aspx/Mercados/Precios.aspx?indice=ESI100000000")
    soup = BeautifulSoup(resp.text, "lxml")

    valores = soup.find(id="ctl00_Contenido_tblAcciones").find_all("tr")[1:]

    for fila in valores:
        valor = fila.find_all("td")

        nombre = valor[0].text
        ultimo = substitute_commas(valor[1].text)
        variacion_porciento = substitute_commas(valor[2].text)
        maximo = substitute_commas(valor[3].text)
        minimo = substitute_commas(valor[4].text)
        volumen = substitute_commas(valor[5].text)
        capitalizacion = substitute_commas(valor[6].text)
        datetime_str = valor[7].text + " " + valor[8].text

        datetime_object = format_datetime(datetime_str)

        try:
            Valor.objects.get(nombre=nombre)
            continue
        except Valor.DoesNotExist:

            Valor.objects.create(
                nombre=nombre,
                ultimo=ultimo,
                variacion_porciento=variacion_porciento,
                maximo=maximo,
                minimo=minimo,
                volumen=volumen,
                capitalizacion=capitalizacion,
                actualizacion=datetime_object,
            )

            sleep(5)


@shared_task
# some heavy stuff here
def update_currency():
    print('Updating Ibex35 data ..')
    resp = requests.get(url="https://www.bolsamadrid.es/ing/aspx/Mercados/Precios.aspx?indice=ESI100000000")
    soup = BeautifulSoup(resp.text, "lxml")

    valores = soup.find(id="ctl00_Contenido_tblAcciones").find_all("tr")[1:]

    for fila in valores:
        valor = fila.find_all("td")

        nombre = valor[0].text
        ultimo = substitute_commas(valor[1].text)
        variacion_porciento = substitute_commas(valor[2].text)
        maximo = substitute_commas(valor[3].text)
        minimo = substitute_commas(valor[4].text)
        volumen = substitute_commas(valor[5].text)
        capitalizacion = substitute_commas(valor[6].text)
        datetime_str = valor[7].text + " " + valor[8].text

        datetime_object = format_datetime(datetime_str)

        # create dictionary
        data = {"nombre": nombre,
                "ultimo": ultimo,
                "variacion_porciento": variacion_porciento,
                "maximo": maximo,
                "minimo": minimo,
                "volumen": volumen,
                "capitalizacion": capitalizacion,
                "actualizacion": datetime_object,
                }

        # find the object by filtering and update all fields
        Valor.objects.filter(nombre=nombre).update(**data)

        sleep(5)


def format_datetime(datetime_str):
    datetime_object = datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
    timezone = pytz.timezone("Europe/Madrid")
    return timezone.localize(datetime_object)


def substitute_commas(number: str) -> str:
    number = number.replace(",", "")
    return number


create_valor()
while True:
    # updating data every 15 seconds
    sleep(15)
    update_currency()
