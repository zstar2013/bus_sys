from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
app_name='bus_info'
# urlpatterns=[
#     #ex: /polls/
#     path('',views.index,name='index'),
#     #ex:/polls/5/
#     path('<int:question_id>/',views.detail,name='detail'),
#     #ex:/polls/5/results/
#     path('<int:question_id>/results/',views.results,name='results'),
#     #ex:/polls/5/vote/
#     path('<int:question_id>/vote/',views.vote,name='vote'),
#     # add the word 'specifics'
#     path('specifics/<int:question_id>/',views.detail,name='detail'),
# ]

urlpatterns=[
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
    path('<int:bus_info_id>/alter/',views.alter,name='alter'),
    path('export/',views.exportOilData,name='export'),
    path('option_result/',views.OptionResult,name='option_result'),
    path('<int:size>/reset_table_size/',views.resetTableSize,name='reset_table_size'),
]