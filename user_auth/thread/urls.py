from django.urls import path

from . import views

app_name = "thread"

urlpatterns = [
    path('', views.TopicListView.as_view(), name='list'),
    path('2', views.TopicListView2.as_view(), name='list2'),
    # <int:pk> – this part is trickier.
    # It means that Django expects an integer value
    # and will transfer it to a view as a variable called pk.
    # if detail/int object this will be transfer to a view as a 'pk' variable

    #That means if you enter http://127.0.0.1:8000/post/5/ into your browser,
    # Django will understand that you are looking for a view called post_detail
    # and transfer the information that pk equals 5 to that view.

    path("detail/<int:pk>", views.TopicDetailView.as_view(), name="topic"),     # <int宣言：if it is int, this int will be "pk = int" if 5 pk is 5.
    path("detailtemplateview/<int:pk>",
         views.TopicTemplateView_InsteadOfDetailView.as_view(),
         name='topic2'),
    path("create/", views.topic_create, name='create_topic'),
    path(
        "create2/",
         views.topic_create_function,
         name="create_topic2"),
    path('create_form', views.TopicFormView.as_view(), name='create_form'),
    path('create_view', views.TopicCreateView.as_view(), name='create_view'),
    path(),


]