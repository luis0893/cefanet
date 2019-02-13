# Generated by Django 2.1.1 on 2018-10-10 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recog', '0028_auto_20181010_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='ApellidoMaterno',
            field=models.CharField(help_text='Introduzca un apellido correcto', max_length=35, null=True, verbose_name='Apellido Materno'),
        ),
        migrations.AlterField(
            model_name='person',
            name='ApellidoPaterno',
            field=models.CharField(help_text='Introduzca un apellido correcto', max_length=35, null=True, verbose_name='Apellido Paterno'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Cabello',
            field=models.CharField(choices=[('N', 'Negro'), ('B', 'Blanco'), ('C', 'Cafe'), ('R', 'Rojo'), ('RU', 'Rubio')], default='N', max_length=5, null=True, verbose_name='Color de Cabello'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Ci',
            field=models.CharField(help_text='Introduzca un numero de CI. correcto', max_length=10, null=True, unique=True, verbose_name='Cédula de Identidad'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Contextura',
            field=models.CharField(choices=[('D', 'Delgada'), ('M', 'Mediana'), ('S', 'Semigruesa'), ('G', 'Gruesa')], default='D', max_length=5, null=True, verbose_name='Tipo de Contextura'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Descripcion',
            field=models.TextField(max_length=200, null=True, verbose_name='Descripción '),
        ),
        migrations.AlterField(
            model_name='person',
            name='Direccion',
            field=models.CharField(max_length=50, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Edad',
            field=models.IntegerField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='Estatura',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='FehaDesaparicion',
            field=models.DateField(null=True, verbose_name='Desaparición en Fecha:'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Nombres',
            field=models.CharField(help_text='Introduzca un nombre correcto', max_length=50, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Ojos',
            field=models.CharField(choices=[('N', 'Negro'), ('V', 'Verde'), ('C', 'Cafe'), ('CE', 'Celeste')], default='N', max_length=5, null=True, verbose_name='Color de Ojos'),
        ),
        migrations.AlterField(
            model_name='person',
            name='Sexo',
            field=models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], default='M', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='Tez',
            field=models.CharField(choices=[('C', 'Clara'), ('T', 'Trigueña'), ('M', 'Morena')], default='C', max_length=5, null=True, verbose_name='Tono de Piel'),
        ),
        migrations.AlterField(
            model_name='person',
            name='faceData',
            field=models.TextField(default='', null=True, verbose_name='Vector de Características'),
        ),
        migrations.AlterField(
            model_name='person',
            name='facePicture',
            field=models.ImageField(max_length=255, null=True, upload_to='faces/%m/%d/%Y', verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='person',
            name='usuario',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Registrado/Actualizado por:'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='institucion',
            field=models.CharField(max_length=50, null=True, verbose_name='Institución'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='lug_trabajo',
            field=models.CharField(max_length=50, null=True, verbose_name='Lugar de trabajo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='unidad',
            field=models.CharField(max_length=50, null=True, verbose_name='Unidad de Trabajo'),
        ),
    ]
