import json
import requests

from datetime import date



accuweaAPI = 'kPqXCPMAsRuG7twU0MzrJOIZmWQtlTgi'
dias_semana = ['Domingo', 'Segunda-feira' , 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']


def pegarCoor():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200):
        print('Não foi possível obter a localização')
        return None
    else:
        try:
            local = (json.loads(r.text))
            coordenadas = {}
            coordenadas['lat'] = local['geoplugin_latitude']
            coordenadas['long'] = local['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarcodigolocal(lat, long):
    localtionapiurl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/" \
                      + "search?apikey=" + accuweaAPI \
                      + "&q=" + lat + "%2C" + long + "&language=pt-br"

    r = requests.get(localtionapiurl)
    if (r.status_code != 200):
        print('Não foi possível obter o cód. do local')
        return None
    else:
        try:
            locationresp = json.loads(r.text)
            infolocal = {}
            infolocal['nomelocal'] = locationresp['LocalizedName'] + ',' \
                                     + locationresp['AdministrativeArea']['LocalizedName'] + '.' \
                                     + locationresp['Country']['LocalizedName']
            infolocal['codigolocal'] = locationresp['Key']
            return infolocal
        except:
            return None


def pegartempoagr(codigolocal, nomelocal):
    CurrenteAPI = 'http://dataservice.accuweather.com/currentconditions/v1/' \
                  + codigolocal + '?apikey=' + accuweaAPI + '&language=pt-br'

    r = requests.get(CurrenteAPI)
    if (r.status_code != 200):
        print('Não foi possível obter o clima atual')
        return None

    else:
        try:
            CurrentCondResp = json.loads(r.text)
            infoclima = {}
            infoclima['textoClima'] = CurrentCondResp[0]['WeatherText']
            infoclima['temp'] = CurrentCondResp[0]['Temperature']['Metric']['Value']
            infoclima['nomelocal'] = nomelocal
            return infoclima
        except:
            return None

def tempo5dias(codigolocal):
    DailyAPI = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' \
                  + codigolocal + '?apikey=' + accuweaAPI + '&language=pt-br&metric=true'

    r = requests.get(DailyAPI)
    if (r.status_code != 200):
        print('Não foi possível obter o clima atual')
        return None
    else:
        try:
            DailyCondResp = json.loads(r.text)
            infoclima5 = []
            for dia in DailyCondResp['DailyForecasts']:
                climadia = {}
                climadia['max'] = dia['Temperature']['Maximum']['Value']
                climadia['min'] = dia['Temperature']['Minimum']['Value']
                climadia['clima'] = dia['Day']['IconPhrase']
                diasemana = int(date.fromtimestamp(dia['EpochDate']).strftime('%w'))
                climadia['dia'] = dias_semana[diasemana]
                infoclima5.append(climadia)
            return infoclima5
        except:
            return None

# http://dataservice.accuweather.com/forecasts/v1/daily/5day/127164?apikey=kPqXCPMAsRuG7twU0MzrJOIZmWQtlTgi&language=pt-br&metric=true

# Inicio


coordena = pegarCoor()

try:
    local = pegarcodigolocal(coordena['lat'], coordena['long'])
    climaatual = pegartempoagr(local['codigolocal'],local['nomelocal'])
    print('Clima atual em:  ' + climaatual['nomelocal'])
    print(climaatual['textoClima'])
    print('temp: ' + str(climaatual['temp']) + "\xb0" + "C")

    print('\nClima para hoje e para os próximos dias:\n')

    Previsao5dia = tempo5dias(local['codigolocal'])
    for dia in Previsao5dia:
        print(dia['dia'])
        print('Mínima ' + str(dia['min']) + '\xb0' + 'C')
        print('Máxima ' + str(dia['max']) + '\xb0' + 'C')
        print('Clima ' + dia['clima'])
        print('------------------------')
except:
     print('Não foi possível obter o clima atual.'  )
