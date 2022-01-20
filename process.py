from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
from matplotlib.patches import Rectangle
import PIL
from numpy import asarray

def detect_faces(img):
  image=plt.imread(img)
  detector = MTCNN()
  faces = detector.detect_faces(image)
  return (image,faces)

def highlight_faces(image_path, faces):
  # display image
    image = plt.imread(image_path)
    plt.imshow(image)

    ax = plt.gca()

    # for each face, draw a rectangle based on coordinates
    for face in faces:
        x, y, width, height = face['box']
        face_border = Rectangle((x, y), width, height,fill=False, color='blue')
        ax.add_patch(face_border)
    plt.show()
    

def get_face(img_path, required_size=(224, 224)):

  image, faces = detect_faces(img_path)

  # getting the bounding box of the face from the image
  x1, y1, w, h = faces[0]['box']
  x2, y2 = x1 + w, y1 + h

  # extract the face
  face_boundary = image[y1:y2, x1:x2]

  # resize pixels (224,224) for the model
  face_image = PIL.Image.fromarray(face_boundary)
  face_image = face_image.resize(required_size)
  face_array = asarray(face_image)
  #face_images.append(face_array)

  return face_array

def face_rec(img):
    face = detect_faces(img)[1]
    print("Face: ",face)
    highlight_faces(img,face)
  
def face_only(img):
  get__face = get_face(img)
  # result of get_face
  plt.imshow(get__face)
  plt.show()
