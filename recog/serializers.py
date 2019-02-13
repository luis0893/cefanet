from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import Person,Profile
from django.contrib.auth.models import User
#from rest_framework.compat import authenticate
from django.contrib.auth import authenticate,login
from rest_auth.serializers import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from rest_framework import exceptions
from drf_extra_fields.fields import Base64ImageField

#Usuario-------------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone','institucion','unidad','lug_trabajo']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
                                     message=" Ya existe un usuario con este Email.", )])
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email','password',]
class PerfilSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user','phone','institucion','unidad','lug_trabajo',]

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data=self.validated_data['user']
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        perf, created = Profile.objects.update_or_create(user=user,
                            phone=validated_data['phone'],
                            institucion=validated_data['institucion'],
                            unidad=validated_data['unidad'],
                            lug_trabajo=validated_data['lug_trabajo'])
        return perf
class UsuarioSerializer(serializers.ModelSerializer):
    #Profile = ProfileSerializer(many=False, required=False, allow_null=True)
    profile=ProfileSerializer(required=False)
    #profile = ProfileSerializer(many=True, read_only=True)
    class Meta:
        model = User
        #fields = '__all__' #con esta funcion de muestra todos los atributos del usuario
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email','profile']



class UsuarioCrearActualizarSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
    message=" Ya existe un usuario con este correo.", )])
    #email2 = EmailField(label = 'Confirm Email')
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all(),
    message=" El username ya existe.", )])
    profile = ProfileSerializer()
    #profile =serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
            'password',
            'profile'
        ]

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        email = validated_data['email']
        password = validated_data['password']
        profile=validated_data['profile']

        user_obj = User(
            username = username,
            email = email,
            first_name = first_name
        )

        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UsuarioListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]

class UsuarioDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',

        ]

class LoginSerializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self, data):
        username=data.get("username","")
        password = data.get("password", "")
        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg="User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg="Unable to login with give credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


#Persona------------------------------------------------------------------
class PersonSerializer(serializers.ModelSerializer):
    facePicture = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Person
        fields = ('id','Nombres','ApellidoPaterno','ApellidoMaterno','Ci',
                  'FehaDesaparicion','FehaRegistro','Sexo','Direccion',
                  'Estado','Edad','Estatura','Descripcion','Contextura',
                  'Tez','Cabello','Ojos','usuario','facePicture','faceData')

        """def filter_query(self, queryset):
    queryset = super(PersonSerializer)
def filter_queryset(self, queryset):
    queryset = super(InvoiceViewSet, self).filter_queryset(queryset)
    return queryset.order_by('-id')"""

class PeopleSerializer(serializers.ModelSerializer):
    #facePicture = Base64ImageField(max_length=None, use_url=True, )
    #faceData=serializers.CharField(read_only=True)

    #usuario = UserSerializer(read_only=True)
    class Meta:
        model = Person
        fields = ('id','Nombres','ApellidoPaterno','ApellidoMaterno','Ci',
                  'FehaDesaparicion','FehaRegistro','Sexo','Direccion',
                  'Estado','Edad','Estatura','Descripcion','referencia','Contextura',
                  'Tez','Cabello','Ojos','usuario','facePicture','faceData')
        read_only_fields = ['id',]

class PersonCreate(serializers.ModelSerializer):
    Ci = serializers.CharField(validators=[UniqueValidator(queryset=Person.objects.all(),
    message="Ya existe una persona con este Ci")])
    class Meta:
        model = Person
        fields = ('Nombres','ApellidoPaterno','ApellidoMaterno','Ci',
                  'FehaDesaparicion','FehaRegistro','Sexo','Direccion',
                  'Estado','Edad','Estatura','Descripcion','Contextura',
                  'Tez','Cabello','Ojos','usuario',)
        def create(self, validate_data):
            Nombres              =validate_data['Nombres']
            ApellidoPaterno     =validate_data['ApellidoPaterno']
            ApellidoMaterno     = validate_data['ApellidoMaterno']
            Ci                  = validate_data['Ci']
            FehaDesaparicion    = validate_data['FehaDesaparicion']
            FehaRegistro        = validate_data['FehaRegistro']
            Sexo                = validate_data['Sexo']
            Direccion           = validate_data['Direccion']
            Estado              = validate_data['Estado']
            Edad                = validate_data['Edad']
            Estatura            = validate_data['Estatura']
            Descripcion         = validate_data['Descripcion']
            Contextura          = validate_data['Contextura']
            Tez                 = validate_data['Tez']
            Cabello             = validate_data['Cabello']
            Ojos                = validate_data['Ojos']
            usuario             = validate_data['usuario']

            person_obj=Person(
                Nombres=Nombres,
                ApellidoPaterno=ApellidoPaterno,
                ApellidoMaterno=ApellidoMaterno,
                Ci=Ci,
                FehaDesaparicion=FehaDesaparicion,
                FehaRegistro=FehaRegistro,
                Sexo=Sexo,
                Direcci=Direccion,
                Estado=Estado,
                Edad=Edad,
                Estatura=Estatura,
                Descripcion=Descripcion,
                Contextura=Contextura,
                Tez=Tez,
                Cabello=Cabello,
                Ojos=Ojos,
                usuario=usuario
            )
            person_obj.save()
