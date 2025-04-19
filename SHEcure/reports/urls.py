from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('upvote/<int:report_id>/', views.upvote_report, name='upvote_report'),
    path('report/<int:report_id>/add_comment/', views.add_comment, name='add_comment'),
    path('report_submission/', views.report_submission, name='report_submission'),
    path('reports/', views.reports_list, name='reports_list'),
    # ... other URL patterns ...
]