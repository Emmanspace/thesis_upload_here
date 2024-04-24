from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/intent/', include('job.urls')),
    re_path(r'^', include('job.urls')),

    # for mongodb
    # path('person/', include('job.urls')),

    #for mongoDB (updated)
    re_path(r'^', include('job.urls')),

    

    # additional
    # re_path(r'^admin', include('djoser.urls')),
    # re_path(r'^api/v1/', include('djoser.urls')),
    # re_path(r'^api/v1/', include('djoser.urls.authtoken')),
    # re_path(r'^api/v1/intent', include('job.urls'))
]
