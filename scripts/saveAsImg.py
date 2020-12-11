
import os
import h5py
import argparse
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser("Script to save images out of a hdf5 files")

parser.add_argument('hdf5', nargs='*', help='Path to hdf5 file/s')

args = parser.parse_args()

if args.hdf5 is None:
	print(parser.format_help())
	exit(0)

def process_img(img, key):
	if 'depth' in key or 'seg' in key:
		img = img.astype(np.float)
		img -= np.min(img)
		max_val = np.max(img)
		if max_val != np.inf:
			img /= max_val 
		else:
			img /= np.max(img[img != np.inf])
		if len(img.shape) == 3:
			img = img[:,:,0]
	return img

def visFile(filePath):
	if os.path.exists(filePath):
		if os.path.isfile(filePath):
			with h5py.File(filePath, 'r') as data:
				keys = [key for key in data.keys()]
				for key in keys:
					val = np.array(data[key])
					file_path = '{}_{}.jpg'.format(key, str(os.path.basename(filePath)).split('.')[0]) 
					if len(val.shape) == 2 or len(val.shape) == 3 and val.shape[2] == 3:
						val = process_img(val, key)
						if len(val.shape) == 2 or len(val.shape) == 3 and val.shape[2] == 1:
							plt.imsave(file_path, val, cmap='jet')
						else:
							plt.imsave(file_path, val)
		else:
			print("The path is not a file")
	else:
		print("The file does not exist: {}".format(args.hdf5))

if isinstance(args.hdf5, basestring):
	visFile(args.hdf5)	
elif isinstance(args.hdf5, list):
	for file in args.hdf5:
		visFile(file)
else:
	print("Input must be a path")
