from django.test import TestCase
from django.utils import timezone
import datetime

from .models import BusInfo,CarType,MonthlyFeedback

from django.urls import reverse

def create_car_type(type_name,car_length):
    return CarType.objects.create(type_name=type_name,car_length=car_length)
def create_bus_info(car_id,type_name):
    time=timezone.now()
    c=CarType.objects.get(type_name=type_name)
    return BusInfo.objects.create(car_id=car_id,publish_date=time,cartype_id=c.id)
def get_carType_by_id(type_id):
    return CarType.objects.get(pk=type_id)
def create_feedback_type(car_id,car_length):
    return MonthlyFeedback.objects.create(carinfo_id=car_id,car_length=car_length)


class BusInfoModelTest(TestCase):
    def test_get_Length(self):
        type = create_car_type('1213455', '8.9')
        bi=create_bus_info("闽AY8801",'1213455')
        carlength=bi.get_car_length()
        self.assertEqual(carlength,'8.9')

class feedbackModeTest(TestCase):
    def test_save_feedback(self):
        feedback=create_feedback_type()


