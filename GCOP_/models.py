# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from cloudinary.models import CloudinaryField

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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
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


class Branches(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(unique=True, max_length=100)
    branch_location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'branches'


class ChurchPositions(models.Model):
    postition_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=100)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)  # Cascade deletes related records

    class Meta:
        managed = True
        db_table = 'church_positions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = True
        db_table = 'groups'


class Joinedgroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Groups,on_delete= models.CASCADE, blank=True, null=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE, blank=True, null=True)
    group_position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'joinedGroups'


from django.contrib.auth.models import User

class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    registered_by = models.CharField(max_length=100, blank=True, null=True)  # Stores first name of the user
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    hometown = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    date_joined = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_num = models.CharField(max_length=20, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    nxt_of_kin = models.CharField(max_length=100, blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    welfare_card_num = models.CharField(max_length=50, blank=True, null=True)
    place_of_residence = models.CharField(max_length=50, blank=True, null=True)
    tithe_card_num = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    church_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, db_column='church_branch', blank=True, null=True)
    member_image = CloudinaryField('image', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    baptism_status = models.BooleanField(blank=True, null=True)
    baptist_at_gcop = models.BooleanField(blank=True, null=True)
    is_printed = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'member'



class Relations(models.Model):
    id = models.BigAutoField(primary_key=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_member = models.BooleanField(blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    member_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'relations'


from django import forms
from .models import Member

class MemberImageUploadForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_image']

