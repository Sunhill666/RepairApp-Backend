from django.urls import path, re_path

from repair.views import RepairFormListCreateView, RepairFormRetrieveUpdateDestroyView, finish_repair, appoint_repair

urlpatterns = [
    path('report/', RepairFormListCreateView.as_view()),
    re_path(r'^report/(?P<pk>\d+)/$', RepairFormRetrieveUpdateDestroyView.as_view()),
    path('finish/', finish_repair),
    path('appoint/', appoint_repair)
]
