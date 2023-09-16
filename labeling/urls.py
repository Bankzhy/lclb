
from django.urls import path

from labeling import views

urlpatterns = [
    path('', views.lc_index, name='lc_index'),
    path('lc_review', views.lc_review, name='lc_review'),
    path('lc_project_list', views.lc_project_list, name='lc_project_list'),
    path('create_lc_project', views.create_lc_project, name='create_lc_project'),
    path('class_list', views.class_list, name='class_list'),
    path('post_pos_class', views.post_pos_class, name='post_pos_class'),
    path('post_neg_class', views.post_neg_class, name='post_neg_class'),
    path('post_del_class', views.post_del_class, name='post_del_class'),
]
