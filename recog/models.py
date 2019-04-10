
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
from .utils import *
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .helper import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
import base64
# Create your models here.



class Person(models.Model):
    Nombres = models.CharField(max_length=50,verbose_name='Nombre',help_text='Introduzca un nombre correcto',null=True, blank=False)
    ApellidoPaterno = models.CharField(max_length=35,verbose_name='Apellido Paterno',help_text='Introduzca un apellido correcto',null=True, blank=True)
    ApellidoMaterno = models.CharField(max_length=35,verbose_name='Apellido Materno',help_text='Introduzca un apellido correcto',null=True, blank=False)
    Ci = models.CharField(max_length=10,unique=True,verbose_name='Cédula de Identidad',help_text='Introduzca un numero de CI. correcto',null=True, blank=False)
    FehaDesaparicion = models.DateField(verbose_name='Desaparecio en Fecha:',null=True, blank=False)
    FehaRegistro = models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')
    SEXOS = (('F', 'Femenino'), ('M', 'Masculino'))
    Sexo = models.CharField(max_length=1, choices=SEXOS, default='M',null=True, blank=False)
    Direccion = models.CharField(max_length=50,verbose_name='Dirección',null=True, blank=False)
    Estado = models.BooleanField(default=False,verbose_name='Estado')
    Edad=models.IntegerField(null=True, blank=False,validators= [MaxValueValidator(100),MinValueValidator(1)],)
    Estatura=models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=False)
    Descripcion=models.TextField(max_length=200,null=True, blank=False,verbose_name='Descripción de la Desaparición ')
    referencia=models.TextField(max_length=50,null=True,verbose_name='Referencias', blank=False)
    #Contextura
    CONTX = (('D', 'Delgada'), ('M', 'Mediana'), ('S', 'Semigruesa'), ('G', 'Gruesa'))
    Contextura = models.CharField(max_length=5, choices=CONTX, default='D',verbose_name='Tipo de Contextura',null=True, blank=False)
    #Tez
    TEZS = (('C', 'Clara'), ('T', 'Trigueña'), ('M', 'Morena'))
    Tez = models.CharField(max_length=5, choices=TEZS, default='C',verbose_name='Tono de Piel',null=True, blank=False)
    #ColorPelo
    PELO = (('N', 'Negro'), ('B', 'Blanco'), ('C', 'Cafe'), ('R', 'Rojo'), ('RU', 'Rubio'))
    Cabello = models.CharField(max_length=5, choices=PELO, default='N',verbose_name='Color de Cabello',null=True, blank=False)
    #ColorOjos
    OJO= (('N', 'Negro'), ('V', 'Verde'), ('C', 'Cafe'), ('CE', 'Celeste'))
    Ojos = models.CharField(max_length=5, choices=OJO, default='N',verbose_name='Color de Ojos',null=True, blank=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1,verbose_name='Registrado/Actualizado por:',null=True, blank=False)
    #usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, default=1)
    #default='/profile_img/default.png',
    facePicture = models.ImageField(upload_to='faces/%m/%d/%Y',max_length=255, null=True, blank=False,verbose_name='Dirección',
                                    help_text='La imagen debe contener una Persona.',validators=[face_detection],)
                                    #default='/default.jpg')
    #cropping = ImageRatioField('facePicture', '700x500',free_crop=True, size_warning=True)
    faceData = models.TextField(default='',null=True,verbose_name='Vector de Características')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Fue Modificado en:')
    def __str__(self):
        return "{0}".format(self.Nombres)
        #return self.Nombres,self.id
    @property
    def title(self):
        return self.Nombres
    class Meta:
        ordering=['-FehaRegistro']
        verbose_name='Persona'
        verbose_name_plural = "Personas"

@receiver(post_save, sender=Person, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
    if instance.facePicture:
        img = instance.facePicture
        id=instance.id
        #resize_img(img, 160, 160)
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # fullpath = BASE_DIR + instance.facePicture.url
        detected_face(img,id)

@receiver(post_delete, sender=Person)
def instance_deleted(sender, instance, **kwargs):
    if instance.id:
        id = instance.id
        delete_user(id)

class Profile(models.Model):
    phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    phone=models.IntegerField(null=True,unique=True, verbose_name='Teléfono', validators = [phone_validator])
    profesion=models.CharField(max_length=50, null=True, blank=False,verbose_name='Profesión')
    institucion = models.CharField(max_length=50, null=True, blank=False,verbose_name='Institución')
    unidad = models.CharField(max_length=50, null=True, blank=False,verbose_name='Unidad de Trabajo')
    lug_trabajo = models.CharField(max_length=50, null=True, blank=False,verbose_name='Lugar de trabajo')

    def __str__(self):
        return "{0} {1} {2}".format(self.user.first_name, self.user.last_name, self.phone)
    class Meta:
        verbose_name_plural = "Perfiles"
        verbose_name='Perfil'