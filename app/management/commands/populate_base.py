#-*- coding: utf-8 -*-
import timeit
import warnings

from django.core.management.base import NoArgsCommand, CommandError
import sys
from app.models import Profiling, User


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        pass

for i in range(10):
        u = User(username='Raul%d' %(i), email='raul%d@gmail.com'%(i))
        u.save()