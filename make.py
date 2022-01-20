import sqlite3
import os.path
from os import listdir, getcwd
import sys

from os import listdir
from os.path import isfile, join


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(BASE_DIR,"sql/")
img_dir = os.path.join(BASE_DIR,"images/")
full_dir = lambda x,y: x+y
known_faces_imgs = full_dir(img_dir,'known_faces/')
new_faces_imgs = full_dir(img_dir,'new_faces/')
imgs1 = [f for f in listdir(known_faces_imgs) if isfile(join(known_faces_imgs, f))]
imgs2 = [f for f in listdir(new_faces_imgs) if isfile(join(new_faces_imgs, f))]
#telechargi 2 images pour tester
'''
import urllib.request
def store_image(url, local_file_name):
  with urllib.request.urlopen(url) as resource:
    with open(local_file_name, 'wb') as f:
      f.write(resource.read())
store_image('https://upload.wikimedia.org/wikipedia/commons/2/25/Chris_Evans_SDCC_2014.jpg',
            '1.jpg')
store_image('https://img.buzzfeed.com/buzzfeed-static/static/2018-01/11/18/campaign_images/buzzfeed-prod-fastlane-01/chris-evans-uses-nothing-on-his-beard-its-just-th-2-20079-1515714803-5_dblbig.jpg',
            '2.jpg')
'''

def codb(db_file):
    db_file = full_dir(db_dir,db_file)
    print(db_file)
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print (db_file,"DONE")
        sql = "create table if not exists elements ("
        sql +="ID INTEGER PRIMARY KEY AUTOINCREMENT,"
        sql+="IMAGE BLOB,TYPE TEXT,NOM TEXT);"
        conn.execute(sql)
    else:
        print ("Schema exists")
        print
    return conn

def insert_picture(db,imgs):
    conn = codb(db)
    for i in imgs:
        picture_file=full_dir(full_dir(img_dir,db+"/"),i)
        with open(picture_file, 'rb') as input_file:
            ablob = input_file.read()
            base=os.path.basename(picture_file)
            afile, ext = os.path.splitext(base)
            sql = "INSERT INTO elements"
            sql+="(IMAGE, TYPE,NOM) VALUES(?, ?,?);"
            conn.execute(sql,[sqlite3.Binary(ablob), ext, afile]) 
            conn.commit()
    conn.close()
        

def make_new():
#db1
    insert_picture('known_faces',imgs1)
 #db2
    insert_picture('new_faces',imgs2)
    





