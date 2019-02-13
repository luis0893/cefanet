from PIL import Image, ExifTags
import cv2,pickle,os.path,h5py
import base64, json
from django.core.exceptions import ValidationError
from keras import backend as K
from keras.models import load_model
K.set_image_data_format('channels_first')
import tensorflow as tf
import numpy as np
np.set_printoptions(threshold=np.nan)
#graph = tf.get_default_graph()
def triplet_loss(y_true, y_pred, alpha=0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # triplet formula components
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[1])))
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[2])))
    basic_loss = pos_dist - neg_dist + alpha
    loss = tf.maximum(basic_loss, 0.0)
    return loss
def load_FRmodel():
    K.clear_session()
    #with graph.as_default():
    FRmodel = load_model('./recog/model.h5', custom_objects={'triplet_loss': triplet_loss})
    #FRmodel = load_model('./recog/ajuradoalfaro.h5', custom_objects={'triplet_loss': triplet_loss}, compile=False)
    # FRmodel = load_model('models/model.h5')
    #K.clear_session()
    return FRmodel
def ini_user_database():
    # check for existing database
    #user_db = {}
    if os.path.exists('./recog/database/user_dictt.pickle'):

        with open('./recog/database/user_dictt.pickle', 'rb') as handle:
            user_db = pickle.load(handle)
        #print("base de datos"+user_db)

    else:
        print('no se encontro el archivo')
        # make a new one
        # we use a dict for keeping track of mapping of each person with his/her face encoding
        user_db = {}

    return user_db
# deploy deep learning model as an API.
def img_to_encoding(image_path, model):
    print("ruta de imagen"+image_path.path)
    print("url de imagen"+image_path.url)
    img1 = cv2.imread(image_path.path,1)
    img = img1[..., ::-1]
    img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)
    x_train = np.array([img])
    embedding = model.predict_on_batch(x_train)
    print(embedding)
    return embedding

def add_user_img_path(img_path,usu,user_db,):
    FRmodel = load_FRmodel()
    print("modelo cargado")
    #user_db = {}
    #image = Image.open(img_path)
    #image = Image.open(img_path.path)
    #user_db = img_to_encoding(img_path, FRmodel)
    #op=json.dumps(user_db)
    usustr=str(usu)
    user_db[usustr] = img_to_encoding(img_path, FRmodel)
    print("codificando")
    #print('User '+user_db[usu])
    # save the database
    with open('./recog/database/user_dictt.pickle', 'wb') as handle:
        pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('User ' + usustr + ' added successfully**************************************************************')
    #return user_db

def detected_face(image_path,usu):
    user_db = ini_user_database()
    print("Se a cargado la base de datos")
    try:
        #image = Image.open(filepath)

        img1 = cv2.imread(image_path.path)
        face_cascade = cv2.CascadeClassifier('./recog/haarcascade_frontalface_default.xml')
        images = np.array(img1)
        gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        if (len(faces) == 0):
            # return None, None
            return False
        else:
            (x, y, w, h) = faces[0]
            #img = images[y:y + w, x:x + h]
            #image[y: y + h, x: x + w]
            img = images[y:y + h, x:x + w]
            # face_img = img_gray[y-50:y + h+100, x-50:x + w+100]
            # return gray[y:y + w, x:x + h], faces[0]
            img = cv2.resize(img, (96, 96))
            cv2.imwrite(image_path.path, img)
            add_user_img_path(image_path, usu, user_db)
            #print('esta es la base'+user_db)
            #imge = cv2.imread(image_path.path)


        #image.save(filepath.path,optimize=True,quality=100)
        #image.close()
        # img2 = img.resize((wsize, hsize), Image.ANTIALIAS)
        # img2.save(_file.path, quality=80)
    except (AttributeError, KeyError, IndexError):
        pass
def face_detection(image):
    print(image.name)
    if image.name != "/default.jpg":
        #cascade_path = staticfiles_storage.path('opencv/haarcascade_frontalface_default.xml')
        im = Image.open(image)
        face_cascade = cv2.CascadeClassifier('./recog/haarcascade_frontalface_default.xml')
        image = np.array(im)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) < 1:
            raise ValidationError(u'La imagen debe contener un rostro de una persona.')
        if len(faces) > 1:
            raise ValidationError(u'La imagen contiene más de un rostro. Sube una imagen que contenga un solo rostro.')
def resize_img(_file, wsize, hsize):
    img = Image.open(_file)
    try:
        if wsize < img.size[0] and hsize < img.size[1]:
            ratio = 1. * wsize / hsize
            (width, height) = img.size
            if width > height * ratio:
                newwidth = int(height * ratio)
                left = width / 2 - newwidth / 2
                right = left + newwidth
                top = 0
                bottom = height
            elif width < height * ratio:
                newheight = int(width * ratio)
                top = height / 2 - newheight / 2
                bottom = top + newheight
                left = 0
                right = width
            if width != height * ratio:
                img = img.crop((left, top, right, bottom))

            img2 = img.resize((wsize, hsize), Image.ANTIALIAS)
            img2.save(_file.path, quality=80)
    except IOError:
        print('Error ao renderizar a imagem, ', img.path)