from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication,BasicAuthentication
from rest_framework.response import Response
from rest_framework import viewsets,generics,mixins
from rest_framework.permissions import *
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import status
from .serializers import *
from .models import Person, Profile
from .helper import *
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from skimage import io
from django.contrib.auth.decorators import login_required
from .decorators import admin_hr_required, admin_only
from .permissions import IsOwnerOrReadOnly
from drf_extra_fields.fields import Base64ImageField
#--------------------------------------------models--------
# Create your views here.


class PerAPIView(generics.ListCreateAPIView):
    """
    A class based view for creating and fetching student records
    """
    queryset = Person.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = [AllowAny]
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        profil = Person.objects.all()
        serializer = PeopleSerializer(profil, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """

        serializer = PeopleSerializer(data=request.data,)
        if serializer.is_valid(raise_exception=ValueError):
            #post = serializer.save(usuario=self.request.user)
            #serializer.save(usuario=self.request.user)
            #user = serializer.save(usuario=)
            #user.save()
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
#Persona------------------------------------------------------------
#@csrf_exempt
class PersonaListarAPI(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

class PersonaCreateAPI(generics.CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonCreate(queryset,many=True)
    permission_classes = [AllowAny]

class PersonaDeleteAPIView(generics.DestroyAPIView):
	#authentication_classes = []
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

class PersonaEditAPIView(generics.RetrieveUpdateAPIView):
    """
    Serializador para editar un USUARIO por ID
    """
    queryset = Person.objects.all()
    serializer_class = PersonCreate
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

#Usuarios-----------------------------------------------------------------------------------------------------------------------------------
#class CrearUserAPIView()
class ProfileAPIView(generics.ListCreateAPIView):
    """
    A class based view for creating and fetching student records
    """
    queryset = User.objects.all()
    #queryset = Person.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [AllowAny]
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        profil = Profile.objects.all()
        serializer = PerfilSerializer(profil, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        serializer = PerfilSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class UsuarioCrearAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioCrearActualizarSerializer
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UsuarioListarAPIView(generics.ListAPIView):
    #queryset = Pipol.objects.all().order_by('-date_joined')
    serializer_class = UsuarioSerializer
   # serializer_class = UsuarioListarSerializer
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)# Isowner:solo si es admin
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    #def perform_create(self, serializer):
     #   serializer.save(owner=self.request.user)
    def get_queryset(self):
        return User.objects.all()

class UsuarioDetalleByIdAPIView(generics.RetrieveAPIView):
    """
    Serializador para ver detalles de un USUARIO por ID
    """

    queryset = User.objects.all()
    serializer_class = UsuarioDetalleSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class UsuarioEditarAPIView(generics.RetrieveUpdateAPIView):
    """
    Serializador para editar un USUARIO por ID
    """
    queryset = User.objects.all()
    serializer_class = UsuarioCrearActualizarSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UsuarioEliminarAPIView(generics.DestroyAPIView):
    """
    Serializador par eliminar un usuario por ID
    """
    queryset = User.objects.all()
    #serializer_class = UsuarioDetalleSerializer
    serializer_class =UsuarioSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
   # permission_classes = [permissions.IsAuthenticated]


class UserByEmail(generics.RetrieveAPIView):
    """
    Serializador para ver detalles de un USUARIO por Email
    """
    queryset = User.objects.all()
    serializer_class = UsuarioDetalleSerializer
    lookup_field = 'email'
    permission_classes = [AllowAny]

class LoginVieew(APIView):
    authentication_classes = []
    permissions_classes = [AllowAny]
    serializer_class = LoginSerializers
    def post(self, request):
        serializer=LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)

class LogoutVieew(APIView):
    authentication_classes = [TokenAuthentication,]
    def post(self,request):
        django_logout(request)
        return Response.status_code==204
        #return Response(status=204)
class PersonRecog(APIView):

    def post(self,request):
        def store_temp_file(file_object):
            temp_file_path = ".tmp/deepenstatsserver/" + file_object.name
            if not os.path.exists(os.path.dirname(temp_file_path)):
                os.makedirs(os.path.dirname(temp_file_path))
            with open(temp_file_path, 'wb+') as f:
                for chunk in file_object.chunks():
                    f.write(chunk)
            return temp_file_path
        if 'face' in request.data:
            # ### Poniendo todo junto
            # Para hacer reconocimiento facial vamos a tomar la imagen de entrada, encontrar su codificación y luego
            # ver si hay alguna codificación similar en la base de datos o no. Definimos un valor de umbral para decidir si las dos imágenes son similares
            # o no basado en la similitud de sus codificaciones.
            threshold = 0.6
            img = request.data['face']
            img_path=store_temp_file(img)
            face_found = detect(img_path)
            # if face_found==0:
            #     return Response({'La imagen debe contener un rostro de una persona.'}, status=201)
            # if face_found==2:
            #     return Response({'La imagen contiene más de un rostro. Sube una imagen que contenga un solo rostro.'}, status=201)
            if face_found:
                encoding = img_to_encoding2(img_path)
                min_dist = 99999
                # loop over all the recorded encodings in database
                for name in user_db:
                    # find the similarity between the input encodings and claimed person's encodings using L2 norm
                    dist = np.linalg.norm(np.subtract(user_db[name], encoding))
                    # check if minimum distance or not
                    if dist < min_dist:
                        min_dist = dist
                        identity = name
                if min_dist > threshold:
                    print("Esta persona no se encuentra en la base de datos.")
                    os.remove(img_path)
                    #identity = JsonResponse({'status': 'failed', 'msg': 'Persona no reconocida.'}, status=201)
                    return Response({'status': 'failed', 'msg': 'Persona no reconocida.'}, status=201)
                else:
                    comp=Person.objects.get(pk=identity)
                    print("Hi! " + str(identity) + ", L2 distance: " + str(min_dist))
                    os.remove(img_path)
                    #return Response({'status': 'successful', 'msg': "Hi! " + str(identity) + ", L2 distance: " + str(min_dist)},status=201)
                    return Response({
                        'Pertence': str(identity),
                        'Distancia': str(min_dist) ,
                        'Nombres': str(comp.Nombres),
                        'ApellidoPaterno': str(comp.ApellidoPaterno),
                        'ApellidoMaterno': str(comp.ApellidoMaterno),
                        'Ci': str(comp.Ci),
                        'Sexo': str(comp.Sexo),
                        'Edad':str(comp.Edad),
                        'facePicture': str(comp.facePicture)
                                    },status=201)
                #return min_dist, identity
            else:
                os.remove(img_path)
                return Response({'No se encontró ninguna cara en la imagen. Inténtalo de nuevo....'},status=201)
        else:
            return Response({'status': 'failed', 'msg': 'Por favor ingrese una imagen.'}, status=404)

        #return Response({'recognition':str(img)},status=status.HTTP_200_OK)
def img_to_base64(image):
    """Convete a openCV image to a base64 image"""
    image = cv2.imencode('.png', image)[1].tostring()
    base64_image = base64.b64encode(image)
    base64_image = "data:image/png;base64," + base64_image.decode("utf-8")
    return base64_image