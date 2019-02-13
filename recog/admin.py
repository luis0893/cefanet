from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportActionModelAdmin,ImportExportModelAdmin,ExportActionMixin,ImportExportMixin, ImportExportMixinBase
from .models import Person, Profile
from image_cropping import ImageCroppingMixin
import csv
from django.http import HttpResponse
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
site_header = "Admin PEPLOST"
site_title = "Portal de Administración PEPLOST"
index_title = "Bienvenido a Peplost "


# luis-potrojurado
admin.site.unregister(Group)
admin.site.unregister(User)
#admin.site.register(Person)
@admin.register(Person)
class HeroAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['full_name']
    # list_display = ['full_name_property','Nombres','ApellidoPaterno','ApellidoMaterno','Ci',
    #               'FehaDesaparicion','FehaRegistro','Sexo','Direccion',
    #               'Estado','Edad','Estatura','usuario','get_thumbnail','delete']
    date_hierarchy = 'FehaRegistro'
    fieldsets = [
        ('Información Personal', {
            'fields': ['Nombres','ApellidoPaterno','ApellidoMaterno','Ci',
                       ('FehaDesaparicion','Estado'),'Direccion',('get_thumbnail','facePicture',),]
        }),
        ('Características', {
            'fields': [('Sexo','Edad','Estatura'),('Contextura','Tez','Cabello','Ojos'),'referencia','Descripcion','faceData'],
            #'classes': ['collapse', 'collapse-closed']
        }),
        (None, {'fields': [('FehaRegistro', 'updated_at', 'usuario'),]})
    ]

    def delete(self, obj):
        return mark_safe('<input type="button" value="Eliminar" onclick="location.href=\'{0}/delete/\'" />'.format(obj.pk))
    delete.short_description = 'Acciones'
    list_per_page = 10
    readonly_fields = ['full_name','FehaRegistro','usuario', 'get_thumbnail', 'updated_at','faceData',]
    def get_thumbnail(self, person):
        """
        Admin wrapper to display product.image as thumbnail.
        """
        if person.facePicture:
            return format_html('<a href="%s" target="_blank"><img src="%s" width=50 height=50>'
                               % (person.facePicture.url, person.facePicture.url))
        return None
    get_thumbnail.short_description = 'Imagen'
    search_fields = ['Nombres','ApellidoPaterno','Ci','ApellidoMaterno']

    list_filter = ('Estado','updated_at', 'usuario','Sexo')
    def full_name(self, person):
        if person:
            co=''
            te = ''
            ca=''
            oj=''
            color=False
            #color de fondo
            if person.Estado == True:
                color = '#d7d7d7'
            else:
                color = '#acacac'

            #Contextura
            if person.Contextura=='D':
                co='Delgada'
            elif person.Contextura=='M':
                co='Mediana'
            elif person.Contextura=='S':
                co='Semigruesa'
            elif person.Contextura=='G':
                co='Gruesa'
            else:
                co='niguna'
            #Tono de piel
            if person.Tez=='C':
                te = 'Clara'
            elif person.Tez=='T':
                te = 'Trigueña'
            elif person.Tez=='M':
                te = 'Morena'
            else:
                te = 'niguna'
            #Color de cabello
            if person.Cabello=='N':
                ca='Negro'
            elif person.Cabello=='B':
                ca='Blanco'
            elif person.Cabello=='C':
                ca='Cafe'
            elif person.Cabello=='R':
                ca='Rojo'
            elif person.Cabello == 'RU':
                ca = 'Rubio'
            else:
                ca='niguna'
            # Ojos
            if person.Ojos == 'N':
                oj = 'Negro'
            elif person.Ojos == 'V':
                oj = 'Verde'
            elif person.Ojos == 'C':
                oj = 'Cafe'
            elif person.Ojos == 'CE':
                oj = 'Celeste'
            else:
                oj = 'niguna'
            return format_html(
                           '<div id="card" style="'
                           #'position: absolute;'
                           'width: 700px;height: 245px;background: {16};border-radius: 5px;'
                           'padding: 25px;padding-top: 0;padding-bottom: 0;'
                           'left: 50%;top: 67.5px;'
                           'margin-left: 0px;box-shadow: -20px 0 35px -25px black, 20px 0 35px -25px black;z-index: 5;">'
                           '<img href="{3}" target="_blank"><img src="{4}" style="width: 150px;height: 142px;float: left;'
                           'border-radius: 5px;margin-right: 10px;margin-top: 20px; ">'
                           
                           #'-webkit-filter: sepia(1);-moz-filter: sepia(1);filter: sepia(1);" >'
                           #'<h2>Ondřej Page Bárta</h2>'
                           '</br>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">      Nombre:{0} {1} {2}</p>'       
                           '<p style="font-family: courier;color: #555;font-size: 15px;">        Edad:{6} años.</p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">    Estatura:{7} m.</p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;"> Desapareció:{8} </p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Contextura: {11}</p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Tono de Piel: {12}</p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Color de Cabello: {13} </p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Color de Ojos: {14} </p>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Domicilio:<h style="font-family: courier;color: #555;font-size: 13px;"> {10}</h> </p>'
                           '</br>'
                           '<span class="left bottom" style="font-family: courier;color: #000;font-size: 13px; left: 90px;'
                           'bottom: 25px;clear:both;">Ci.: {5}</span>'
                           '<p style="font-family: courier;color: #555;font-size: 15px;">Descripción: <h style="font-family: courier;color: #555;font-size: 13px;">{15}</h> </p>'
                           #'<span class="left bottom "style="font-family: courier; position: absolute;bottom: 25px;">Ci.: {5}</span>'
                           
                           '<span class="right bottom" style="font-family: courier;color: #000;font-size: 13px;float:right;'
                           '">Ref.: {9}</span>'
                           
                           '</div>'
                           .format(person.Nombres, person.ApellidoPaterno, person.ApellidoMaterno,person.facePicture.url, person.facePicture.url,
                                   person.Ci,person.Edad,person.Estatura,person.FehaDesaparicion,person.referencia,person.Direccion,
                                   co,te,ca,oj,person.Descripcion,color))
        return None
    full_name.short_description = "Personas"
    #full_name = property(full_name)
class ProfileInline(admin.TabularInline):
    model = Profile
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    inlines = [ProfileInline]
    list_display = 'username', 'first_name', 'last_name', 'email','get_phone','get_profesion','get_institucion','get_unidad','get_lugar','delete'
    list_select_related = ('profile',)

    def delete(self, obj):
        return mark_safe('<input type="button" value="Eliminar" onclick="location.href=\'{0}/delete/\'" />'.format(obj.pk))
    delete.short_description = 'Acciones'
    def get_phone(self, instance):
        return instance.profile.phone
    get_phone.short_description = 'Telefono'

    def get_profesion(self, instance):
        return instance.profile.profesion
    get_profesion.short_description = 'Profesion'

    def get_institucion(self, instance):
        return instance.profile.institucion
    get_institucion.short_description = 'Institucion'

    def get_unidad(self, instance):
        return instance.profile.unidad
    get_unidad.short_description = 'Unidad'

    def get_lugar(self, instance):
        return instance.profile.lug_trabajo
    get_lugar.short_description = 'Lugar de Trabajo'

admin.site.add_action(ImportExportModelAdmin)
#admin.site.register(Profile)