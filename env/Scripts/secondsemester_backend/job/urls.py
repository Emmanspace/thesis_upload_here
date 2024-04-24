from django.urls import path, re_path
from . import views

# for mongoDb
from job import views

urlpatterns = [
    path('notification/', views.notificationView.as_view()),
    path('newest/', views.NewestHistoryView.as_view()),
    path('<int:pk>/', views.DashboardView.as_view()),
    # added
    path('total/', views.totalSlots_View.as_view()),
    path('available/', views.availableSlots_View.as_view()),
    path('parking/', views.parkingSlots_View.as_view()),


    # (updated) mongoDB
    re_path(r'^department$', views.departmentApi),
    re_path(r'^department/([0-9]+)$', views.departmentApi),

    # for example (notifiaction api to front end)
    re_path(r'^notification$', views.departmentApi),

    # for dashboard api
    re_path(r'^total$', views.totalSlotsApi),
    re_path(r'^available$', views.availableApi),
    re_path(r'^parking$', views.parkingApi),
    
    # for jairo's db
    re_path(r'^track$', views.realTimeApi),

    re_path(r'^history$', views.historyApi),
    re_path(r'^sse$', views.sse, name='sse'),
    re_path(r'^count_documents$', views.count_documents, name='count_documents'),
    re_path(r'^decrement_documents$', views.decrement_documents, name='decrement_documents'),

    # for getting user documents to be printed in history tab
    re_path(r'^documents$', views.get_documents),
    # re_path(r'^get_user/(?P<user_id>[0-9a-f-]+)$', views.get_user_documents, name='get_user_documents'),

    # for user update/change in user settings
    # re_path(r'^profile/(?P<user_id>\d+)/$', views.user_profile),
    # path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    # re_path(r'^profile/(?P<user_id>\d+)/$', views.user_profile, name='user_profile'),

    # re_path(r'^register$', views.UserCreateAPIView.as_view()),
    re_path(r'pasok$', views.UserLoginAPIView.as_view()),
    re_path(r'^registration$', views.UserRegistrationView.as_view(), name='user-registration'),

    re_path(r'^register/$', views.UserRegistrationView.as_view(), name='user-registration'),
    re_path(r'^login/$', views.UserLoginAPIView.as_view(), name='user-login'),
    # re_path(r'^profile/$', views.UserProfileDetail.as_view(), name='user-profile'),
    # 
    # this is original (woprking)
    re_path(r'^update/(?P<pk>[0-9a-f]{24})/$', views.UpdateDocumentView.as_view(), name='update_document'),
    re_path(r'^getdocuments/(?P<id>.+)/$', views.get, name='get_document'),  # Capture any characters
    re_path(r'^getus$', views.get_user),
    # re_path(r'^getuser/(?P<id>\d+)/$', views.get_user, name='get_user'),
    
    # re_path(r'^api/tutorials$', views.user_list),
    # re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', views.user_detail),
    # re_path(r'^api/tutorials/published$', views.user_list_published)
    re_path(r'^api/v1/users/$', views.register_user)

]