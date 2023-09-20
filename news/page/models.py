# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category1(models.Model):
    cat1_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'CATEGORY_1'


class Category2(models.Model):
    cat2_id = models.SmallAutoField(primary_key=True)
    cat1 = models.ForeignKey(Category1, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'CATEGORY_2'


class News(models.Model):
    platform = models.ForeignKey('Platform', models.DO_NOTHING, blank=True, null=True)
    cat1 = models.ForeignKey(Category1, models.DO_NOTHING, blank=True, null=True)
    cat2 = models.ForeignKey(Category2, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    press = models.CharField(max_length=16, blank=True, null=True)
    writer = models.CharField(max_length=16, blank=True, null=True)
    date_upload = models.DateTimeField(blank=True, null=True)
    date_fix = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    num_comm = models.IntegerField(blank=True, null=True)
    sticker = models.JSONField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NEWS'


class Platform(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'PLATFORM'


class User(models.Model):
    platform = models.ForeignKey(Platform, models.DO_NOTHING, blank=True, null=True)
    user_id = models.CharField(unique=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'USER'


# 운영 DB에서 사용할 Table (Topic, Recommend)
