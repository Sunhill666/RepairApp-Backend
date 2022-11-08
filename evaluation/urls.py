from django.urls import path, re_path

from evaluation.views import EvaluationListCreateView, EvaluationRetrieveView

urlpatterns = [
    path('evaluate/', EvaluationListCreateView.as_view()),
    re_path(r'^evaluate/(?P<pk>\d+)/$', EvaluationRetrieveView.as_view()),
]
