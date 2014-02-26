#-*- coding: utf-8 -*-
import timeit
import warnings

from django.core.management.base import NoArgsCommand, CommandError
import sys
from app.models import Profiling, User


class Command(NoArgsCommand):
    '''
    Toda esta classe, será rodada com o script ( request_and_list_prof.sh )
    [Esta classe Command envia um aviso, pois ela em si não lida com argumentos,
    pode ignorar o aviso, os parâmetros enviados serão tratados fora da classe]
    '''
    def handle_noargs(self, **options):
        pass

def do_timeit(loop_number):

    # chama o médodo objects_all, a quandidade de vezes recebido no parâmetro
    d = timeit.timeit('objects_all()', setup='from ' + __name__ + ' import objects_all', number=loop_number)
    print('%s - Tempo Médio para cada ciclo da requisição até a resposta do site. Comparado entre %d entrada(s)]' %("%.5fs"%(avg_db), count))
    print('%s - [Tempo Médio para %d query(ies) (SELECT * FROM table) efetuadas na Base de Dados]' %("%.5fs"%(d / loop_number), loop_number) )
    print('%s - Database' %(avg_db))
    print('%s - Serializacao' %(avg_serializer))
    print('%s - Request Response' %(avg_request_response))
    print('%s - Api View' %(avg_api_view))
    print('%s - Render' %(avg_render_time))

def objects_all():
    '''
    Faz um select em toda a base do Profiling, e retorna a média de tempo de cada
    atributo (ou seja, de cada coluna da base)
    '''

    global count
    global db_timem, serializer_time, request_response_time, api_view_time, render_time
    global avg_db, avg_serializer, avg_request_response, avg_api_view, avg_render_time

    db_time = 0
    serializer_time = 0
    request_response_time = 0
    api_view_time = 0
    render_time = 0

    avg_db = 0
    count = 0
    profs = Profiling.objects.all()

    for prof in profs:
        db_time = db_time + prof.db_time
        serializer_time = serializer_time + prof.serializer_time
        request_response_time = request_response_time + prof.request_response_time
        api_view_time = api_view_time + prof.api_view_time
        render_time = render_time + prof.render_time

        count = count + 1

    avg_db = db_time / count
    avg_serializer = serializer_time / count
    avg_request_response = request_response_time / count
    avg_api_view = api_view_time / count
    avg_render_time = render_time / count

    # for prof in profs:
    #     if not count:
    #         db_time = prof.db_time
    #         count = count + 1
    #         continue
    #
    #     db_time = db_time + prof.db_time
    #     count = count + 1
    #
    # avg_db = db_time / count



loop_number = 1
for args in sys.argv:
    if args.startswith('loop'):
        arg = args.split('loop')
        print(args)
        print(arg)
        loop_number = arg[1]


do_timeit(int(loop_number))