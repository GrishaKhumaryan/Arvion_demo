import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                              help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                              max_length=150, unique=True,
                                              validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                                              verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False,
                                                 help_text='Designates whether the user can log into this admin site.',
                                                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                                                  help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                                                  verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Ծննդյան ամսաթիվ')),
                ('phone_number', models.CharField(blank=True, max_length=25, verbose_name='Հեռախոսահամար')),
                ('address', models.TextField(blank=True, verbose_name='Բնակության հասցե')),
                ('emergency_contact_phone',
                 models.CharField(blank=True, max_length=25, verbose_name='Վստահված հեռախոսահամար')),
                ('profile_picture',
                 models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='Պրոֆիլի նկար')),
                ('public_profile_id',
                 models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Հանրային ID (QR)')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Ալերգիայի անվանում')),
            ],
            options={
                'verbose_name': 'Ալերգիա',
                'verbose_name_plural': 'Ալերգիաներ',
            },
        ),
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=5, unique=True, verbose_name='Խմբի անվանում')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Հիվանդության անվանում')),
            ],
            options={
                'verbose_name': 'Հիվանդություն',
                'verbose_name_plural': 'Հիվանդություններ',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Անվանում')),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Դեղամիջոցի անվանում')),
            ],
            options={
                'verbose_name': 'Դեղամիջոց',
                'verbose_name_plural': 'Դեղամիջոցներ',
            },
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Վիրահատության անվանում')),
            ],
            options={
                'verbose_name': 'Վիրահատություն',
                'verbose_name_plural': 'Վիրահատություններ',
            },
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True,
                                              related_name='doctor_profile', serialize=False,
                                              to=settings.AUTH_USER_MODEL, verbose_name='Օգտատեր')),
                ('specialty', models.CharField(max_length=100, verbose_name='Մասնագիտություն')),
                ('license_number', models.CharField(max_length=50, unique=True, verbose_name='Լիցենզիայի համար')),
                ('workplace', models.CharField(blank=True, max_length=255, null=True, verbose_name='Աշխատավայր')),
                ('biography', models.TextField(blank=True, null=True, verbose_name='Իմ մասին')),
            ],
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True,
                                              related_name='patient_profile', serialize=False,
                                              to=settings.AUTH_USER_MODEL, verbose_name='Օգտատեր')),
                ('weight_kg',
                 models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Քաշ (կգ)')),
                ('height_cm',
                 models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Հասակ (սմ)')),
                ('other_notes', models.TextField(blank=True, verbose_name='Այլ նշումներ')),
                ('allergies', models.ManyToManyField(blank=True, to='main.allergy', verbose_name='Ալերգիաներ')),
                ('blood_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                  to='main.bloodgroup', verbose_name='Արյան խումբ')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='main.gender', verbose_name='Սեռ'),
        ),
        migrations.CreateModel(
            name='PatientCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis_date', models.DateField(blank=True, null=True, verbose_name='Ախտորոշման ամսաթիվ')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.condition',
                                                verbose_name='Հիվանդություն')),
            ],
        ),
        migrations.CreateModel(
            name='PatientMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.CharField(blank=True, max_length=100, verbose_name='Դեղաչափ')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Ընդունման սկիզբ')),
                ('notes', models.TextField(blank=True, verbose_name='Նշումներ')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.medication',
                                                 verbose_name='Դեղամիջոց')),
            ],
        ),
        migrations.CreateModel(
            name='PatientSurgery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgery_date', models.DateField(blank=True, null=True, verbose_name='Վիրահատության ամսաթիվ')),
                ('notes', models.TextField(blank=True, verbose_name='Նշումներ')),
                ('surgery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.surgery',
                                              verbose_name='Վիրահատություն')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.patientprofile')),
            ],
            options={
                'unique_together': {('patient', 'surgery')},
            },
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='conditions',
            field=models.ManyToManyField(through='main.PatientCondition', to='main.condition',
                                         verbose_name='Հիվանդություններ'),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='medications',
            field=models.ManyToManyField(through='main.PatientMedication', to='main.medication',
                                         verbose_name='Դեղամիջոցներ'),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='surgeries',
            field=models.ManyToManyField(through='main.PatientSurgery', to='main.surgery',
                                         verbose_name='Վիրահատություններ'),
        ),
        migrations.AddField(
            model_name='patientmedication',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.patientprofile'),
        ),
        migrations.AddField(
            model_name='patientcondition',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.patientprofile'),
        ),
        migrations.AlterUniqueTogether(
            name='patientmedication',
            unique_together={('patient', 'medication')},
        ),
        migrations.AlterUniqueTogether(
            name='patientcondition',
            unique_together={('patient', 'condition')},
        ),
    ]
