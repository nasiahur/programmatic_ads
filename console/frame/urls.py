#
# django
#
from django.conf.urls import url

#
# our
#
from frame import views

urlpatterns = [
	url(r'^apply$', views.ApplyView.as_view(), name='ApplyView'),
    url(r'^reload$', views.ReloadView.as_view(), name='ReloadView'),
    url(r'^restart$', views.RestartView.as_view(), name='RestartView'),
]
