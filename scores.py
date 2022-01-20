from scipy.spatial.distance import cosine
from tensorflow.keras.applications.resnet50 import preprocess_input
from .process import get_face
from numpy import asarray
from .get_score import RESNET50_extra

def get_model_score(filenames):
	# extract faces
	faces = [get_face(f) for f in filenames]
	# convert into an array using numpy's array
	samples = asarray(faces, 'float32')
	# prepare the face for the model, ex: centr
	samples = preprocess_input(samples)
	# create a RESNET50 model to get the scores
	model = RESNET50_extra()
	return model.predict(samples)

# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
  # calculate cosinus distance between the rows of matrixs of each embedding
  #(Cosine Similarity)
  score = cosine(known_embedding, candidate_embedding)
  return (score,thresh,score <= thresh)
