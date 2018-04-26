from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from .models import CarType,BusInfo
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from bus_info.logic.feedback import feedback as fb
from bus_info.models import MonthlyFeedback,BusInfo



class IndexView(generic.ListView):
    template_name = 'bus_info/index.html'
    paginate_by = 10
    context_object_name = 'bi_list'
    def get(self, request, *args, **kwargs):

        pass


    def get_queryset(self):
        """Return the last five published questions.(not including those set to be
        published in the future)"""
        set=BusInfo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        return set
    def reset_paginate_by(self,num):
        self.paginate_by=num


class TablesView(generic.ListView):
    template_name = 'bus_info/tables.html'
    context_object_name = 'latest_car_list'
    def get_queryset(self):
        """Return the last five published questions.(not including those set to be
        published in the future)"""
        return BusInfo.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class DetailView(generic.DetailView):
    model=BusInfo
    template_name = 'bus_info/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        :return:
        """
        return BusInfo.objects.filter(published_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = BusInfo
    template_name = 'bus_info/results.html'


def alter(request,bus_info_id):
    bus_info=get_object_or_404(BusInfo,pk=bus_info_id)
    result=fb.scanfiles(["G:\\油耗\\一队油表.xls", "G:\\油耗\\三车队油表.xls", "G:\\油耗\\四队油表.xls", "G:\\油耗\\五队油表.xls"], "G:\\油耗\\营达车队.xls")

    return HttpResponseRedirect(reverse('bus_info:results', args=(bus_info.id,)))