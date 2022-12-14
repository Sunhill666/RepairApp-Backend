from django.urls import path
from rest_framework import routers

from organization import views
from organization.views import AdminTeamViewSet, AdminUserViewSet, get_workbook

router = routers.DefaultRouter()

router.register(r'admin/team', AdminTeamViewSet)
router.register(r'admin/user', AdminUserViewSet)

urlpatterns = [
    path('admin/changepwd/', views.change_pwd),
    path('admin/get_workbook/', get_workbook)
] + router.urls
