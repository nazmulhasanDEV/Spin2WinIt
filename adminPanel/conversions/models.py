from django.db import models
from user.models import *
from product.models import *
import requests
from config.models import TimeStampMixin

class SpinConversionRateIntoUSD(TimeStampMixin):
    spinRateValueInUSD = models.FloatField(default=0.10)


    def __str__(self):
        return str(self.spinRateValueInUSD)