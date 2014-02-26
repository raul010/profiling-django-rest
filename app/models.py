from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

class Profiling(models.Model):

    def __str__(self):
        return str(self.date_time_profiling)

    db_time = models.DecimalField(max_digits=7, decimal_places=5)
    serializer_time = models.DecimalField(max_digits=7, decimal_places=5)
    request_response_time = models.DecimalField(max_digits=7, decimal_places=5)
    api_view_time = models.DecimalField(max_digits=7, decimal_places=5)
    render_time = models.DecimalField(max_digits=7, decimal_places=5)
    date_time_profiling = models.DateTimeField()