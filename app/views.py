#-*-ecoding: utf-8 -*-
import datetime
import time

from django.core.signals import request_started, request_finished
from django.dispatch.dispatcher import receiver
from rest_framework import serializers, renderers
from rest_framework.renderers import JSONPRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User, Profiling


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class MyApiViewTimer(APIView):
    '''
    APIView intermediária que faz o profiling de todo o
    clico de vida do Django REST framework
    '''
    def dispatch(self, *args, **kwargs):
        global dispatch_time

        print("inicio dispatch")

        dispatch_start = time.time()
        ret = super(MyApiViewTimer, self).dispatch(*args, **kwargs)
        dispatch_time = time.time() - dispatch_start
        print("%s [DISPATH]" %(dispatch_time))

        print("fim dispatch")
        return ret

class MyRendererTimer(renderers.JSONRenderer):
    '''
        Renderer intermediários que calcula o tempo de
        renderização (formato nativo para Json)
    '''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        global render_time
        print("inicio render")

        render_start = time.time()
        ret = super(MyRendererTimer, self).render(data)
        render_time = time.time() - render_start
        print("%s [RENDER]" %(render_time))

        print("fim render")
        return ret

class UserListView(MyApiViewTimer):
    '''
    View princial. Alguns testes são feitos: de banco de dados e de serialização
    (model nativo para dicionario representativo, também nativo)
    '''
    renderer_classes = ((MyRendererTimer, JSONPRenderer))
    def get(self, request, format=None):
        global serializer_time
        global db_time

        ### TIME DB ###
        db_start = time.time()
        users = list(User.objects.all())
        db_time = time.time() - db_start
        print("%s [DB]" %(db_time))
        #################

        ### TIME SERIALIZER ###
        serializer_start = time.time()
        serializer = UserSerializer(users, many=True)
        data = serializer.data
        serializer_time = time.time() - serializer_start
        print("%s [SERIALIZER]" %(serializer_time))
        #################

        return Response(data)


    @receiver(request_started)
    def started_all(sender, **kwargs):
        '''
        Receiver que controla a entrada dos requests
        '''
        print("inicio request")
        global started
        started = time.time()

    @receiver(request_finished)
    def finished_all(sender, **kwargs):
        '''
        Receiver que controla a saída dos resquests
        '''
        print("fim request")

        total = time.time() - started
        api_view_time = dispatch_time - (render_time + serializer_time + db_time)
        request_response_time = total - dispatch_time

        # Feito todos os cálculos de profiling, não haverá over-read para
        # armazenar os dados no banco
        prof = Profiling(
            db_time=db_time,
            serializer_time=serializer_time,
            request_response_time=request_response_time,
            api_view_time=api_view_time,
            render_time=render_time,
            date_time_profiling=datetime.datetime.now(),
        )

        prof.save()

        # print ("Database lookup               | %.4fs" % db_time)
        # print ("Serialization                 | %.4fs" % serializer_time)
        # print ("Django request/response       | %.4fs" % request_response_time)
        # print ("API view                      | %.4fs" % api_view_time)
        # print ("Response rendering            | %.4fs" % render_time)