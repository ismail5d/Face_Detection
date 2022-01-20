from db.fetch import *
from make.make import BASE_DIR,db_dir, full_dir

from compare.one_to_many import *
from compare.many_to_many import *
from facial.process import face_rec, face_only
import os.path

IMAGE_TESTING_DIR = full_dir(BASE_DIR,"/images/testing/")

class Database:
    def __init__(self,db_1,db_2,image):
        self.db_1 = db_1
        self.db_2 = db_2
        self.image = image
    
    
    @property
    def db_1(self):
        return self._db_1
        
    @db_1.setter
    def db_1(self,db_1):
        db_1 = full_dir(db_dir,db_1)
        try:
            with open(db_1) as f:
                self._db_1 = db_1
        except IOError as ex:
            print(ex)
            self._db_2 = None
    
    @property
    def db_2(self):
        return self._db_2
    
    @db_2.setter
    def db_2(self,db_2):
        db_2 = full_dir(db_dir,db_2)
        try:
            with open(db_2) as f:
                self._db_2 = db_2
        except IOError as ex:
            print(ex)
            self._db_2 = None
    
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self,image):
        if image is not None:
            data = get_image_by_name(image,self.db_2)
            if data:
                img = full_dir(IMAGE_TESTING_DIR,"%s_new%s"%(image,data[1]))
                with open(img,'wb') as f:
                    f.write(data[0])
                self._image=img
            else:
                print("No image with that name! ")
                self._image = None
    def delete_image(self):
        if self._image is not None and os.path.exists(self._image):
            os.remove(self._image)

    def one_to_many(self):
      if self.image is not None:
        compare_one_to_many(self.image,self.db_1,self.db_2)

    def many_to_many(self):
        compare_many_to_many(self.db_1,self.db_2)


    def detect_faces(self):
      face_rec(self.image)
    
    def face_only(self):
      face_only(self.image)
  

