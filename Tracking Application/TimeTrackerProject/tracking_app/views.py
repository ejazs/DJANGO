from django.shortcuts import render
from django.db.models import Sum, Count, Q
from rest_framework.generics import CreateAPIView , ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import TrackingLog, IdleLog
from .serializers import  TrackingLogSerializer, IdleLogSerializer
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.embed import components

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import GnBu3, OrRd3
from bokeh.plotting import figure



class Dashboard(LoginRequiredMixin, ListView):
  queryset = TrackingLog.objects.all()
  template_name = 'dashboard.html'

class DataListView(LoginRequiredMixin, ListView):
  queryset = TrackingLog.objects.all()
  template_name = 'data_list.html'
  context_object_name = 'logs'

class PerUserPerAppReportView(LoginRequiredMixin, ListView):
  queryset = TrackingLog.objects.values('date', 'emp_id', 'username','app_name', ).annotate(app_time_spent=Sum('app_time_spent'))
  template_name = 'perUserPerApp.html'
  context_object_name = 'logs'

  def get_context_data(self,  **kwargs):
    qs = super(PerUserPerAppReportView, self).get_context_data(**kwargs)
    
    for data in qs.get('object_list'):
      data['idle_time'] = IdleLog.objects.values( 'host_id', 'date').filter(
                            Q(host_id=data['username']) &
                            Q( date=data['date'])
                            ).annotate(idle_time= Sum('duration'))
                            
    print(qs.get('object_list'))
    return qs


class PerUserReportView(LoginRequiredMixin, ListView):
  queryset = TrackingLog.objects.values('date', 'emp_id', 'username', ).annotate(app_time_spent=Sum('app_time_spent'))
  template_name = 'perUser.html'
  context_object_name = 'logs'

  def get_context_data(self,  **kwargs):
    qs = super(PerUserReportView, self).get_context_data(**kwargs)
    
    for data in qs.get('object_list'):
      data['idle_time'] = IdleLog.objects.values( 'host_id', 'date').filter(
                            Q(host_id=data['username']) &
                            Q( date=data['date'])
                            ).annotate(idle_time= Sum('duration'))
                            
    print(qs.get('object_list'))
    return qs


class IdleDataListView(LoginRequiredMixin, ListView):
  queryset = IdleLog.objects.all()
  template_name = 'idle_data_list.html'
  context_object_name = 'logs'


class ListTrackingLogAPI(ListAPIView):
  queryset = TrackingLog.objects.all()
  serializer_class = TrackingLogSerializer
  # permission_classes = [IsAuthenticated]


class CreateTrackingLogAPI(CreateAPIView):
  queryset = TrackingLog.objects.all()
  serializer_class = TrackingLogSerializer
  # permission_classes = [IsAuthenticated]

class ListIdleLogAPIView(ListAPIView):
  queryset = IdleLog.objects.all()
  serializer_class = IdleLogSerializer

class CreateIdleLogAPIView(CreateAPIView):
  queryset = IdleLog.objects.all()
  serializer_class = IdleLogSerializer


class TestView(ListView):
  queryset = TrackingLog.objects.values('date', 'emp_id', 'username','app_name',).annotate(app_time_spent=Sum('app_time_spent'))
  template_name = 'test.html'
  context_object_name = 'logs'

  def get_context_data(self,  **kwargs):
    qs = super(TestView, self).get_context_data(**kwargs)
    
    for data in qs.get('object_list'):
      data['idle_time'] = IdleLog.objects.values( 'host_id', 'date').filter(
                            Q(host_id=data['username']) &
                            Q( date=data['date'])
                            ).annotate(idle_time= Sum('duration'))
                            
    print(qs.get('object_list'))
    return qs


def test_view(request):
  
  fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
  years = ["2015", "2016", "2017"]
  colors = ["#c9d9d3", "#718dbf", "#e84d60"]

  data = {'fruits' : fruits,
        '2015'   : [2, 1, 4, 3, 2, 4],
        '2016'   : [5, 3, 4, 2, 4, 6],
        '2017'   : [3, 2, 4, 4, 5, 3]}

  p = figure(x_range=fruits, plot_height=250, title="Fruit Counts by Year",
            toolbar_location=None, tools="")

  p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
              legend_label=years)

  p.y_range.start = 0
  p.x_range.range_padding = 0.1
  p.xgrid.grid_line_color = None
  p.axis.minor_tick_line_color = None
  p.outline_line_color = None
  p.legend.location = "top_left"
  p.legend.orientation = "horizontal"

  script, div = components(p)

  fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
  years = ["2015", "2016", "2017"]

  exports = {'fruits' : fruits,
            '2015'   : [2, 1, 4, 3, 2, 4],
            '2016'   : [5, 3, 4, 2, 4, 6],
            '2017'   : [3, 2, 4, 4, 5, 3]}
  imports = {'fruits' : fruits,
            '2015'   : [-1, 0, -1, -3, -2, -1],
            '2016'   : [-2, -1, -3, -1, -2, -2],
            '2017'   : [-1, -2, -1, 0, -2, -2]}

  p = figure(y_range=fruits, plot_height=250, x_range=(-16, 16), title="Fruit import/export, by year",
            toolbar_location=None)

  p.hbar_stack(years, y='fruits', height=0.9, color=GnBu3, source=ColumnDataSource(exports),
              legend_label=["%s exports" % x for x in years])

  p.hbar_stack(years, y='fruits', height=0.9, color=OrRd3, source=ColumnDataSource(imports),
              legend_label=["%s imports" % x for x in years])

  p.y_range.range_padding = 0.1
  p.ygrid.grid_line_color = None
  p.legend.location = "top_left"
  p.axis.minor_tick_line_color = None
  p.outline_line_color = None

  script1, div1 = components(p)
  #Store components 
  # script, div = components(p)
  context = {'script': script, 'div':div, 'script1' : script1, 'div1': div1}
  return render(request, 'graph.html' , context)
