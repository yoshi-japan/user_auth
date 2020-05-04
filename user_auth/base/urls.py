from django.urls import path
from . import views

app_name = 'base'

def y(request):
    return views.HttpResponse("heelo dir")

urlpatterns = [
    path('',views.top, name='top'),
    # when you use url template you can associate name with this view.
    # {% url base:top %} this link takes me to the reflect above view.
    # {% url app_name:name %} app_name is the variable in views.py name is the one of parameters of path in urls.py
    path('s', views.second, name='second'),
    path('top', views.top2, name="top2"),
    path('class_top', views.TopView.as_view(template_name = 'base/home.html'), name='topview'),
    # this path below is satisfactory when we just reflect template html(no modified)
    path('term/', views.TopView.as_view(template_name='base/term.html'), name='term'),


]