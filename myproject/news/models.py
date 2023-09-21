# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models

from django.db import models


class Category(models.Model):
    cat2_id = models.SmallIntegerField(primary_key=True)
    cat1_name = models.CharField(max_length=16)
    cat2_name = models.CharField(max_length=16)
    platform_name = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'CATEGORY'


class Comment(models.Model):
    news = models.ForeignKey('News', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    comment = models.TextField()
    date_upload = models.DateTimeField()
    date_fix = models.DateTimeField(blank=True, null=True)
    good_cnt = models.SmallIntegerField(blank=True, null=True)
    bad_cnt = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'COMMENT'


class News(models.Model):
    cat2 = models.ForeignKey(Category, models.DO_NOTHING)
    title = models.CharField(max_length=256)
    press = models.CharField(max_length=16, blank=True, null=True)
    writer = models.CharField(max_length=32, blank=True, null=True)
    date_upload = models.DateTimeField()
    date_fix = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    sticker = models.JSONField()
    url = models.CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'NEWS'


class News6Recommand(models.Model):
    news = models.OneToOneField(News, models.DO_NOTHING, primary_key=True)
    recommand = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'NEWS6_RECOMMAND'


class User(models.Model):
    user_id = models.CharField(unique=True, max_length=8, db_collation='utf8mb3_bin')
    user_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'USER'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class NewsRecommend(models.Model):
    id = models.BigAutoField(primary_key=True)
    news = models.ForeignKey(News, models.DO_NOTHING, blank=True, null=True)
    topic = models.ForeignKey('NewsTopic', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_recommend'


class NewsTopic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'news_topic'