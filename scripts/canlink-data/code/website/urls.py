from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.conf import settings
from . import views

urlpatterns = [
        url(r'^$', views.main, name="main"),
        url(r'^submit/$', views.index, name="index"),
        url(r'^record-d/(?P<id>\d+)(?P<format>\.[a-zA-Z]{2,})$', views.deleteRecord, name='record-d'),
        url(r'^deleted/$', views.deleted, name='deleted'),
        url(r'^stop/(?P<id>\d+)/$', views.stop, name='stop'),
        url(r'^thesisSubmission/$', views.thesisSubmission, name="thesisSubmission"),
        url(r'^submit/thesisSubmission/$', views.thesisSubmission, name="thesisSubmission"),
        url(r'^main/$', views.main, name="main"),
        url(r'^progress/$', views.progress, name='progress'),
        url(r'^upload/(?P<file>.+)/(?P<status>.+)$', views.upload, name="upload"),
        url(r'^upload/$', views.upload, name="upload"),
        url(r'^search/$', views.search, name="search"),
        url(r'^csh/$', views.csh, name="csh"),
        url(r'^csh_autosuggest/$', views.csh_autosuggest, name="csh_autosuggest"),
        url(r'^csh_search/$', views.csh_search, name="csh_search"),
        url(r'^get_csh/(?P<id>/*)', views.get_csh, name="get_csh"),
        url(r'^archive/$', views.archive, name='archive'),
        url(r'^delete_archive/(?P<id>\d+)/$', views.delete_archive, name='delete_archive'),
    	url(r'^delete_archive_all/$', views.delete_archive_all, name='delete_archive_all'),
        url(r'^getitem/(?P<id>/*)', views.getitem, name="getitem"),
        url(r'^download/$', views.download, name='download'),
        url('accounts/', include('django.contrib.auth.urls')),
        url(r'^change_password/$', views.change_password, name='change_password'),
        url(r'^register/$', views.register, name="register"),
        url(r'^reg_user/$', views.reg_user, name="reg_user"),
        url(r'^update_user/$', views.update_user, name="update_user"),
        url(r'^checkUser/$', views.checkUser, name="checkUser"),
        url(r'^checkskey/$', views.checkskey, name="checkskey"),
        url(r'^profile/(?P<username>.+)/(?P<error>.+)/$', views.profile, name='profile'),
        url(r'^updateUri', views.updateUri, name="updateUri")       # github webhook
]
