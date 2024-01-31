from django.urls import path,re_path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index,name='index'),
    path('admin-dashboard', views.admin_index,name='admin_index'),
    path('editor-dashboard', views.editor_index,name='editor_index'),
    path('staff-dashboard', views.staff_index,name='staff_index'),
    path('student-dashboard', views.student_index,name='student_index'),
]