import sqlite3
from db.fetch import fetch_images
from facial.scores import get_model_score, is_match
import os
from make.make import BASE_DIR,full_dir
from matplotlib import pyplot as plt

IMAGE_TESTING_DIR = full_dir(BASE_DIR,"/images/testing/")

import ntpath
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def compare_many_to_many(db1,db2):
  data1 = fetch_images(db1)
  data2 = fetch_images(db2)
  for new_face in data2:
    face1 = "%s_new%s" % (new_face[0],new_face[2])
    face1 = full_dir(IMAGE_TESTING_DIR,face1)
    with open(face1,'wb') as f:
      f.write(new_face[1])
    for known_face in data1:
      face2 = "%s_known%s" % (known_face[0],known_face[2])
      face2 = full_dir(IMAGE_TESTING_DIR,face2)
      print(path_leaf(face1),"vs",path_leaf(face2))
      with open(face2,'wb') as f:
        f.write(known_face[1])
      filenames = [face1,face2]
      # proba
      embeddings = get_model_score(filenames)
      # verifyyy
      score, thresh, comp=is_match(embeddings[0],embeddings[1])
  
      if comp:
        print('>Les visages sont les memes (%.3f <= %.3f)' % (score, thresh))
        
        f, imgss = plt.subplots(1,2)
        
        f1, f2 = plt.imread(filenames[0]), plt.imread(filenames[1])
        
        imgss[0].imshow(f1) # l'image lwla
        imgss[0].set_title(path_leaf(filenames[0]))
        
        
        imgss[1].imshow(f2) # hadi tanya
        imgss[1].set_title(path_leaf(filenames[1]))
        plt.show()
        os.remove(face2)
        break
      else:
        print("Pas les memes")
      os.remove(face2)
    os.remove(face1)
