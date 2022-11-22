from django.db import models
from django.utils.translation import gettext_lazy as _

from organization.models import User
from repair.models import RepairForm


class EvaluationForm(models.Model):
    repair_form = models.OneToOneField(RepairForm, on_delete=models.CASCADE)
    repair_man = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation_man = models.CharField(_("评价人姓名"), max_length=10)
    total_rate = models.IntegerField(_("总评"), default=5)
    attitude_rate = models.IntegerField(_("态度评分"), default=5)
    attitude_desc = models.TextField(_("态度描述"), max_length=60, default=None, null=True)
    proficiency_rate = models.IntegerField(_("熟练度评分"), default=5)
    proficiency_desc = models.TextField(_("熟练度描述"), max_length=60, default=None, null=True)
    speed_rate = models.IntegerField(_("速度评分"), default=5)
    speed_desc = models.TextField(_("速度描述"), max_length=60, default=None, null=True)
    evaluation_desc = models.TextField(_("服务整体评价"), max_length=200, default="用户未做出具体评价")
    pics = models.ImageField(upload_to='eva_pic/%Y/%m/', null=True, blank=True)

    class Meta:
        db_table = 'evaluation'
