# # -*- coding: utf-8 -*-
#
# from keras.models import load_model
# from .utils import *
# import os.path
# import tensorflow as tf
# import numpy as np
#
#
# def triplet_loss(y_true, y_pred, alpha=0.2):
#     """
#     Implementation of the triplet loss as defined by formula (3)
#
#     Arguments:
#     y_true -- true labels, required when you define a loss in Keras, you don't need it in this function.
#     y_pred -- python list containing three objects:
#             anchor -- the encodings for the anchor images, of shape (None, 128)
#             positive -- the encodings for the positive images, of shape (None, 128)
#             negative -- the encodings for the negative images, of shape (None, 128)
#
#     Returns:
#     loss -- real number, value of the loss
#     """
#
#     anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
#
#     # Step 1: Compute the (encoding) distance between the anchor and the positive
#     pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)))
#     # Step 2: Compute the (encoding) distance between the anchor and the negative
#     neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)))
#     # Step 3: subtract the two previous distances and add alpha.
#     basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
#     # Step 4: Take the maximum of basic_loss and 0.0. Sum over the training examples.
#     loss = tf.reduce_mean(tf.maximum(basic_loss, 0.0))
#
#     return loss
#
#
# def load_FRmodel():
#     # FRmodel = load_model('models/model.h5', custom_objects={'triplet_loss': triplet_loss})
#     FRmodel = load_model('ajuradoalfaro.h5', custom_objects={'triplet_loss': triplet_loss})
#     return FRmodel
#
# def verify(image_path, identity, database, model):
#     """
#     Function that verifies if the person on the "image_path" image is "identity".
#
#     Arguments:
#     image_path -- path to an image
#     identity -- string, name of the person you'd like to verify the identity. Has to be a resident of the Happy house.
#     database -- python dictionary mapping names of allowed people's names (strings) to their encodings (vectors).
#     model -- your Inception model instance in Keras
#
#     Returns:
#     dist -- distance between the image_path and the image of "identity" in the database.
#     door_open -- True, if the door should open. False otherwise.
#     """
#
#     # Step 1: Compute the encoding for the image. Use img_to_encoding() see example above. (≈ 1 line)
#     encoding = img_to_encoding(image_path, model)
#
#     # Step 2: Compute distance with identity's image (≈ 1 line)
#     dist = np.linalg.norm(encoding - database[identity])
#
#     # Step 3: Open the door if dist < 0.7, else don't open (≈ 3 lines)
#     if dist < 0.7:
#         print("Eres " + str(identity) + ", bienvenido")
#         door_open = True
#     else:
#         print("No eres " + str(identity) + ", por favor márchate")
#         door_open = False
#
#     return dist, door_open
#
#
# def who_is_it(image_path, database, model):
#     """
#     Implements face recognition for the happy house by finding who is the person on the image_path image.
#
#     Arguments:
#     image_path -- path to an image
#     database -- database containing image encodings along with the name of the person on the image
#     model -- your Inception model instance in Keras
#
#     Returns:
#     min_dist -- the minimum distance between image_path encoding and the encodings from the database
#     identity -- string, the name prediction for the person on image_path
#     """
#
#     ## Step 1: Compute the target "encoding" for the image. Use img_to_encoding() see example above. ## (≈ 1 line)
#     encoding = img_to_encoding(image_path, model)
#
#     ## Step 2: Find the closest encoding ##
#
#     # Initialize "min_dist" to a large value, say 100 (≈1 line)
#     min_dist = 100
#
#     # Loop over the database dictionary's names and encodings.
#     for (name, db_enc) in database.items():
#
#         # Compute L2 distance between the target "encoding" and the current "emb" from the database. (≈ 1 line)
#         dist = np.linalg.norm(encoding - database[name])
#
#         # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. (≈ 3 lines)
#         if dist < min_dist:
#             min_dist = dist
#             identity = name
#
#     if min_dist > 0.7:
#         print("No esta en la base de datos.")
#     else:
#         print("Eres " + str(identity) + ", la distancia es " + str(min_dist) + ", bienvenido")
#
#     return min_dist, identity
#
#
# def main():
#     FRmodel = load_FRmodel()
#     print('\n\nModel loaded...')
#     database = {}
#     database["danielle"] = img_to_encoding("images/danielle.png", FRmodel)
#     database["younes"] = img_to_encoding("images/younes.jpg", FRmodel)
#     database["tian"] = img_to_encoding("images/tian.jpg", FRmodel)
#     database["andrew"] = img_to_encoding("images/andrew.jpg", FRmodel)
#     database["kian"] = img_to_encoding("images/kian.jpg", FRmodel)
#     database["dan"] = img_to_encoding("images/dan.jpg", FRmodel)
#     database["sebastiano"] = img_to_encoding("images/sebastiano.jpg", FRmodel)
#     database["bertrand"] = img_to_encoding("images/bertrand.jpg", FRmodel)
#     database["kevin"] = img_to_encoding("images/kevin.jpg", FRmodel)
#     database["felix"] = img_to_encoding("images/felix.jpg", FRmodel)
#     database["benoit"] = img_to_encoding("images/benoit.jpg", FRmodel)
#     database["arnaud"] = img_to_encoding("images/arnaud.jpg", FRmodel)
#     ch = 'y'
#     while (ch == 'y' or ch == 'Y'):
#         user_input = input(
#             '\nEnter choice \n1. Add\n2. Recognize face\n3. Verify face\n4. Quit\n')
#
#         if user_input == '1':
#             img_path = input('Enter the image name with extension stored in images/\n')
#             # add_user_img_path(user_db, FRmodel, name, 'images/' + img_path)
#
#         elif user_input == '2':
#             verify("images/camera_0.jpg", "younes", database, FRmodel)
#             verify("images/camera_2.jpg", "kian", database, FRmodel)
#
#         elif user_input == '3':
#             who_is_it("images/camera_0.jpg", database, FRmodel)
#
#         elif user_input == '4':
#             return
#
#         else:
#             print('Invalid choice....\nTry again?\n')
#
#         ch = input('Continue ? y or n\n')
#         # clear the screen
#         os.system('cls' if os.name == 'nt' else 'clear')
#
#
# if __name__ == main():
#     main()