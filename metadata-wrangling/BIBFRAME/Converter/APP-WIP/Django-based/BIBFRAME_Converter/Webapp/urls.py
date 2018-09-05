"""BIBFRAME_Converter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic.edit import DeleteView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^record-d/(?P<id>\d+)(?P<format>\.[a-zA-Z]{3})(?P<old_id>\d+)$', views.deleteRecord, name='record-d'),
    url(r'^stop/(?P<id>\d+)/$', views.stop, name='stop'),
    url(r'^deleted/$', views.deleted, name='deleted'),
    url(r'^processingQueue/$', views.processingQueue, name='processingQueue'),
    url(r'^processing/$', views.processing, name='processing'),
    url(r'^processing_duplicate/$', views.processing_duplicate, name='processing_duplicate'),
    url(r'^uploaded/(?P<id>\d+)/$', views.model_form_upload, name='model_form_upload')
]
