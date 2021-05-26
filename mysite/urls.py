from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="search"),
    path('login/', views.sign_in),
    path('register/', views.sign_up),
    path('userinfo/', views.userinfo),
    path('logout/', views.log_out),
    path('New_Exploit_Report/', views.new_exploit_report),
    path('Report_List/<slug:judge>/<slug:slug>/', views.report_list),
    path('Report_Post/<slug:judge>/<slug:slug>/<int:id>', views.report_post),
    path('New_InforCollect_Report/', views.new_inforcollect_report),
    path('Delete_Post/<slug:judge>/<slug:slug>/<int:id>', views.delete_post),
    path('Judge_Post/<slug:judge>/<slug:slug>/<slug:success>/<int:id>', views.judge_post),
]