# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.BigIntegerField()
    permission_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type_id = models.BigIntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    user_id = models.BigIntegerField()
    group_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    permission_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Bjcp2015(models.Model):
    style_id = models.CharField(primary_key=True, max_length=10)
    style_name = models.TextField(blank=True, null=True)
    og_high = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    og_low = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    ibu_high = models.BigIntegerField(blank=True, null=True)
    ibu_low = models.BigIntegerField(blank=True, null=True)
    fg_high = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    fg_low = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    srm_high = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    srm_low = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    abv_high = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    abv_low = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    overallimpression = models.TextField(blank=True, null=True)
    aroma = models.TextField(blank=True, null=True)
    appearance = models.TextField(blank=True, null=True)
    flavor = models.TextField(blank=True, null=True)
    mouthfeel = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)
    characteristicingredients = models.TextField(blank=True, null=True)
    stylecomparison = models.TextField(blank=True, null=True)
    commercialexamples = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bjcp2015'


class Brewbatch(models.Model):
    id = models.BigAutoField(primary_key=True)
    batchnum = models.BigIntegerField(blank=True, null=True)
    batch_size = models.BigIntegerField(blank=True, null=True)
    fv = models.BigIntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    ename = models.TextField(blank=True, null=True)
    cname = models.TextField(blank=True, null=True)
    can = models.CharField(max_length=4, blank=True, null=True)
    yeast = models.CharField(max_length=10, blank=True, null=True)
    generation = models.BigIntegerField(blank=True, null=True)
    brewday = models.DateField(blank=True, null=True)
    coldcrashday = models.DateField(blank=True, null=True)
    packageday = models.DateField(blank=True, null=True)
    fermentationdays = models.BigIntegerField(blank=True, null=True)
    ferment_temperature = models.BigIntegerField(blank=True, null=True)
    pitch_rate = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    est_og = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    og = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    est_fg = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    fg = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    est_abv = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    abv = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    ibu = models.BigIntegerField(blank=True, null=True)
    srm = models.BigIntegerField(blank=True, null=True)
    do_ppm = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    evaporation = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pressure_psi = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    temp_f = models.BigIntegerField(blank=True, null=True)
    co2_vol = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    yeast_suspension = models.BigIntegerField(blank=True, null=True)
    original_ph = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    final_ph = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    final_ntu_s = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    final_ntu_e = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    centrifuge_ntu = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    brewer = models.TextField(blank=True, null=True)
    millergap_mm = models.TextField(blank=True, null=True)
    est_brewhouse_efficiency = models.BigIntegerField(blank=True, null=True)
    brewhouse_efficiency = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    est_preboil_gravity = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    preboil_gravity = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    filter_time = models.BigIntegerField(blank=True, null=True)
    add_sugar = models.BigIntegerField(blank=True, null=True)
    sparging_vol = models.BigIntegerField(blank=True, null=True)
    sparging_gravity = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    dry_hopping = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dry_hopping_total_oil = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    attenuation = models.BigIntegerField(blank=True, null=True)
    productioin_vol = models.BigIntegerField(blank=True, null=True)
    forecast_vol = models.BigIntegerField(blank=True, null=True)
    price = models.BigIntegerField(blank=True, null=True)
    loss = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    brewers_note = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    tasting_note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brewbatch'


class DjangoAdminLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.BigAutoField(primary_key=True)
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


class MainBeer(models.Model):
    id = models.BigAutoField(primary_key=True)
    tapnum = models.CharField(max_length=2)
    time = models.CharField(max_length=10)
    style = models.CharField(max_length=20)
    ename = models.CharField(max_length=20)
    cname = models.CharField(max_length=20)
    abv = models.FloatField()
    ibu = models.BigIntegerField()
    srm = models.BigIntegerField()
    nt_29l = models.BigIntegerField()
    nt_330ml = models.BigIntegerField()
    awardrecord = models.CharField(max_length=100)
    malt = models.CharField(max_length=100)
    hop = models.CharField(max_length=100)
    adj = models.CharField(max_length=100)
    feature = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    keyword = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'main_beer'


class MainCan(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = models.CharField(max_length=10)
    ename = models.CharField(max_length=20)
    cname = models.CharField(max_length=20)
    abv = models.FloatField()
    nt_330ml = models.BigIntegerField()
    description = models.CharField(max_length=150)
    image_url = models.CharField(max_length=100)
    order_url = models.CharField(max_length=100)
    order_text = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'main_can'


class Malt(models.Model):
    brand = models.TextField(blank=True, null=True)
    product = models.TextField(blank=True, null=True)
    lot = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    wort_colour_ebc = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    color_lovibond = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    extract = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    extract_potential_sg = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    moisture = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fine_grind_db = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    fine_grind_as_is = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coarse_grind_db = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    coarse_grind_as_is = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    difference = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    price_ntd_kg = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    price_usd_lb = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'malt'


class Package(models.Model):
    package_id = models.AutoField(primary_key=True)
    package = models.CharField(max_length=15)
    volume_l = models.DecimalField(max_digits=4, decimal_places=2)
    command = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'package'


class PlcFv1(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv1'


class PlcFv10(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv10'


class PlcFv11(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv11'


class PlcFv12(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv12'


class PlcFv13(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv13'


class PlcFv14(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv14'


class PlcFv15(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv15'


class PlcFv16(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv16'


class PlcFv17(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv17'


class PlcFv18(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv18'


class PlcFv19(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv19'


class PlcFv2(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv2'


class PlcFv20(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv20'


class PlcFv21(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv21'


class PlcFv22(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    psi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    psi_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    co2vol_sp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv22'


class PlcFv3(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv3'


class PlcFv4(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv4'


class PlcFv5(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv5'


class PlcFv6(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv6'


class PlcFv7(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv7'


class PlcFv8(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv8'


class PlcFv9(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_fv9'


class PlcGlycol1(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cooler1 = models.IntegerField(blank=True, null=True)
    cooler2 = models.IntegerField(blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_glycol1'


class PlcGlycol2(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cooler1 = models.IntegerField(blank=True, null=True)
    cooler2 = models.IntegerField(blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_glycol2'


class PlcHotwater(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve = models.IntegerField(blank=True, null=True)
    volume = models.DecimalField(max_digits=7, decimal_places=5, blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)
    flowvolume = models.DecimalField(max_digits=7, decimal_places=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_hotwater'


class PlcIcewater(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    volume = models.DecimalField(max_digits=7, decimal_places=5, blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_icewater'


class PlcMashlauter(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve = models.IntegerField(blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)
    pumpspeed = models.IntegerField(blank=True, null=True)
    agitator = models.IntegerField(blank=True, null=True)
    agitatorspeed = models.IntegerField(blank=True, null=True)
    flowmeter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_mashlauter'


class PlcWortkettle(models.Model):
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    setpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valve1 = models.IntegerField(blank=True, null=True)
    valve2 = models.IntegerField(blank=True, null=True)
    chimneytemperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    chimneyvalve = models.IntegerField(blank=True, null=True)
    pump = models.IntegerField(blank=True, null=True)
    pumpspeed = models.IntegerField(blank=True, null=True)
    flowmeter = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    flowvolume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plc_wortkettle'
