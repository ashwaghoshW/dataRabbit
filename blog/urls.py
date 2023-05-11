
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('blog/TargetVsAchievements',views.TargetVsAchievements, name='TargetVsAchievements')
    # path('blog/SimplePieChart',views.SimplePieChart, name='SimplePieChart')
]
