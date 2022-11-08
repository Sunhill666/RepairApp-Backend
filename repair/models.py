from django.db import models
from django.utils.translation import gettext_lazy as _

from organization.models import User
from utils.validators import PhoneNumberValidator


class RepairForm(models.Model):
    class Role(models.TextChoices):
        TEC = 'Teacher', _('老师')
        STU = 'Student', _('学生')
        OTR = 'Other', _('其他')

    class RepairType(models.TextChoices):
        SYS = 'System', _('系统故障')
        HRD = 'Hardware', _('硬件故障')
        NET = 'Network', _('网络故障')
        DAT = 'DATA', _('数据恢复')

    class Status(models.TextChoices):
        RPT = 'Reported', _('已申报')
        APT = 'Appointed', _('已委派')
        NRD = 'Not Rated', _('未评价')
        FID = 'Finished', _('已完成')

    report_man = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report', null=True)
    name = models.CharField(_("报修人名称"), max_length=10)
    contact = models.CharField(_("报修人联系方式"), max_length=30, validators=[PhoneNumberValidator])
    appointment_time = models.DateTimeField(_("预约时间"))
    locate = models.CharField(_("维修地点"), max_length=128)
    role = models.CharField(_("报修人身份"), choices=Role.choices, max_length=7)
    type = models.CharField(_("报修类型"), choices=RepairType.choices, max_length=8)
    descript = models.TextField(_("故障描述"), max_length=500)
    appointment = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='repair')

    start_time = models.DateTimeField(_("报修时间"), auto_now_add=True)
    accept_time = models.DateTimeField(_("受理时间"), default=None, null=True)
    end_time = models.DateTimeField(_("完成时间"), default=None, null=True)
    status = models.CharField(_("状态"), choices=Status.choices, default=Status.RPT, max_length=9)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'form'
