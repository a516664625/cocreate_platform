"""
组队信息表
team 队伍信息表
team_application 队伍申请表
team_members 队伍成员表
"""
from django.db import models

from project.models import Project
from user.models import User


# 队伍信息表
class Team(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='队伍ID')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目ID')
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='队伍负责人')
    team_name = models.CharField(max_length=100, verbose_name='队伍名称')
    is_recruitment_open = models.BooleanField(verbose_name='是否开启招募', default=True)
    recruitment_requirements = models.TextField(blank=True, verbose_name='招募要求')
    recruitment_end_date = models.DateField(blank=True, null=True, verbose_name='招募结束日期')
    recruitment_slots = models.IntegerField(blank=True, null=True, verbose_name='招募人数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.team_name

    class Meta:
        db_table = 'team'
        verbose_name = '队伍信息'
        verbose_name_plural = verbose_name


# 队伍申请表
class Application(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='申请ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='队伍')
    application_msg = models.CharField(max_length=255, verbose_name='申请消息')
    STATUS_CHOICES = (
        ('待加入', '待加入'),
        ('忽略', '忽略'),
        ('已加入', '已加入'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='申请状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"申请ID: {self.id}"

    class Meta:
        db_table = 'team_application'
        verbose_name = '队伍申请'
        verbose_name_plural = verbose_name


# 队伍成员表
class Member(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='队伍')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='成员ID')
    is_leader = models.BooleanField(default=False, verbose_name='是否队长')
    join_date = models.DateField(blank=True, null=True, verbose_name='加入日期')
    leave_date = models.DateField(blank=True, null=True, verbose_name='离开日期')
    MEMBER_STATUS_CHOICES = (
        ('正常', '正常'),
        ('已离开', '已离开'),
        ('被移除', '被移除'),
    )
    member_status = models.CharField(max_length=10, choices=MEMBER_STATUS_CHOICES, blank=True, null=True,
                                     verbose_name='成员状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"成员ID: {self.id}"

    class Meta:
        db_table = 'team_members'
        verbose_name = '队伍成员'
        verbose_name_plural = verbose_name
