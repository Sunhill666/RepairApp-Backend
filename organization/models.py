from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    team_name = models.CharField(_("小组名称"), max_length=10, unique=True)

    def __str__(self):
        return self.team_name

    class Meta:
        db_table = 'team'


class User(AbstractUser):
    username = models.CharField(
        _("学号"),
        max_length=32,
        primary_key=True,
        error_messages={
            "unique": _("相同用户已存在"),
        },
    )
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, default=None, related_name='team')
    team_leader = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True, default=None, related_name='leader')
    first_name = models.CharField(_("名"), max_length=10)
    last_name = models.CharField(_("姓"), max_length=5)

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        full_name = "%s%s" % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    service_num = models.IntegerField(_("服务次数"), default=0)
    total_avg = models.DecimalField(_("总评平均值"), max_digits=2, decimal_places=1, default=0)
    attitude_avg = models.DecimalField(_("态度平均值"), max_digits=2, decimal_places=1, default=0)
    proficiency_avg = models.DecimalField(_("效率平均值"), max_digits=2, decimal_places=1, default=0)
    speed_avg = models.DecimalField(_("速度平均值"), max_digits=2, decimal_places=1, default=0)

    class Meta:
        db_table = "userprofile"
