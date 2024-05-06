from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib import admin
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('aboutUs/', TemplateView.as_view(template_name='aboutUs.html'), name='aboutUs'),
    path('admin/', admin.site.urls),
]
