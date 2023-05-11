from django.urls import path
from . import views
from . import TabularRepresentation
from . import SimplePieChart
from . import DonutChart
from . import Speedometer
from . import SimpleBarChart
from . import StackedBarChart
from . import BarInsideBar
from . import BulletChart
from . import ScatterPlot
from . import LineChart
from . import AreaChart
from . import Butterfly
from . import BarWithLine
from . import BarWithScatter
from . import ChartVotes

app_name = 'dashboard'
# app_name = 'TabularRepresentation'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('dashboard/TabularRepresentation/', views.TabularRepresentation, name='TabularRepresentation'),

        # path('', views.loginuser,name='loginuser'),           ######depreciated
        # path('logout/', views.logoutuser,name='logoutuser'),  #####depreciated


]
