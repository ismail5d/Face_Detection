import argparse
from config import Database
from db.fetch import fetch_images
from make.make import make_new
db_1="known_faces"
db_2="new_faces"
#new parser
parser = argparse.ArgumentParser()
#add parser
parser.add_argument('--one-to-many', type=str,
                   help='Search through db1 for the image')

parser.add_argument('--make-dbs',
                   help='Make new databases')
parser.add_argument('--detect-face',
                   help='Detecting face')
parser.add_argument('--face-only',
                   help='Detecting face')
#get args Namespace
args = parser.parse_args()

#with vars() we can get properties of a Namespace

if vars(args)['one_to_many'] is not None:
  print("Got ONE_TO_MANY = ",args.one_to_many)
  db = Database(db_1,db_2,args.one_to_many)
  db.one_to_many()
elif vars(args)['make_dbs'] is not None:
  print("Making new databases...")
  make_new()
  print("Done")
elif vars(args)['detect_face'] is not None:
  db=Database(db_1,db_2,args.detect_face)
  db.detect_faces()
elif vars(args)['face_only'] is not None:
  db=Database(db_1,db_2,args.face_only)
  db.face_only()
else:
  print("Got Not arg! MANY_TO_MANY will be applied")
  db = Database(db_1,db_2,None)
  db.many_to_many()
