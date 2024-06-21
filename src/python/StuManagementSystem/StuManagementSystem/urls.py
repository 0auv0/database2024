from django.urls import path
from django.urls.conf import include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views
from . import testdb

urlpatterns = [
    path("", views.home,name='home'),
    path('hello/', views.test),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('course/', views.course, name='course_pages'),
    path('info/', views.info, name='info_pages'),
    path('profession/', views.profession, name='profession_pages'),
    path('score', views.score, name='score_pages'),
    path('evaluation', views.evaluation, name='evaluation_pages'),
    # path('logout/', include('logout.urls')),
    # path('login/', testdb.testdb),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)