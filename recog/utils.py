# # -*- coding: utf-8 -*-
# import numpy as np
# import cv2
# from keras.models import load_model
# import tensorflow as tf
# from PIL import Image
#
# def triplet_loss(y_true, y_pred, alpha=0.2):
#     anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
#
#     # triplet formula components
#     pos_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[1])))
#     neg_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[2])))
#     basic_loss = pos_dist - neg_dist + alpha
#     loss = tf.maximum(basic_loss, 0.0)
#     return loss
# def load_FRmodel():
#     FRmodel = load_model('models/model.h5', custom_objects={'triplet_loss': triplet_loss})
#     # FRmodel = load_model('models/model.h5')
#     return FRmodel
#
#
# # def add_user_img_path(user_db, FRmodel, name, img_path):
# #     if name not in user_db:
# #         face_found = detect_face_path(img_path)
# #         if face_found:
# #             # resize_img(img_path)
# #             user_db[name] = img_to_encoding(img_path, FRmodel)
# #             # save the database
# #             with open('database/user_dict.pickle', 'wb') as handle:
# #                 pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
# #             print('User ' + name + ' added successfully')
# #         else:
# #             print('No se encontro niguna Cara. Intentalo nuevamente...........')
# #     else:
# #         print('The name is already registered! Try a different name.........')
# def add_user_img_path( img_path):
#     FRmodel=load_FRmodel()
#     image = Image.open(img_path)
#     face_found = detect_face_path(image)
#     if face_found:
#         # resize_img(img_path)
#         user_db = img_to_encoding(image, FRmodel)
#
#     else:
#         print('No se encontro niguna Cara. Intentalo nuevamente...........')
#
#
# # deploy deep learning model as an API.
# def img_to_encoding(image_path, model):
#     img1 = cv2.imread(image_path, 1)
#     img = img1[..., ::-1]
#     img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)
#     x_train = np.array([img])
#     embedding = model.predict_on_batch(x_train)
#     return embedding
#
#
# def detect_face_path(image_path):
#     #store = 'images/'
#     face_found = False
#     #image = Image.open(image_path)
#     img1 = cv2.imread(image_path)
#     face_cascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')
#     images = np.array(img1)
#     gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#     if (len(faces) == 0):
#         # return None, None
#         return False
#     else:
#         (x, y, w, h) = faces[0]
#         img = images[y:y + w, x:x + h]
#         # face_img = img_gray[y-50:y + h+100, x-50:x + w+100]
#         # return gray[y:y + w, x:x + h], faces[0]
#         img = cv2.resize(img, (96, 96))
#         cv2.imwrite(image_path, img)
#         imge = cv2.imread(image_path)
#         if imge is not None:
#             face_found = True
#         else:
#             face_found = False
#         return face_found