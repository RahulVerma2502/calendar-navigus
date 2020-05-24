from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.CharField(max_length=50)
    time_start = models.CharField(max_length=50)
    time_end = models.CharField(max_length=50)
    appointment_with = models.CharField(max_length=50, blank=True)
    update_time = models.DateField(auto_now=True, auto_now_add=False)

    # show filed in admin panel
    def __str__(self):
        return self.date

    def __str__(self):
        return self.time_start

    def __str__(self):
        return self.time_end

    def __str__(self):
        return self.appointment_with
