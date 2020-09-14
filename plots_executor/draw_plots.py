from vizualization_stuff.distplots import make_distplot_gif, dist_to_3d, dist_of_array
from vizualization_stuff.graph_3d import make_my_plot
from vizualization_stuff.analytics_of_errors import sub_deviance, deviance, matrix_voltage_error, sub_meas, meas, sub_distance_meas
from vizualization import show_plots

from amplitude import meas_to_x
from mammo_packets import read_from_file_binary, parse_mammograph_raw_data, parse_uncompressed_mammograph_packets

import time
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from zipfile import ZipFile

BINSDIR = 'vizualizations/bins'

class MammographMatrix:
    def __init__(self):
        self.matrix = np.zeros((18, 18), dtype=np.int32) - 1
        self.matrix_inverse = np.zeros((18, 18), dtype=np.int32) + 1
        gen = iter(range(256))

        for i in range(6, 18 - 6):
            self.matrix[0, i] = next(gen)

        for i in range(4, 18 - 4):
            self.matrix[1, i] = next(gen)

        for i in range(3, 18 - 3):
            self.matrix[2, i] = next(gen)

        for i in range(2, 18 - 2):
            self.matrix[3, i] = next(gen)

        for j in range(2):
            for i in range(1, 18 - 1):
                self.matrix[4 + j, i] = next(gen)

        for j in range(6):
            for i in range(18):
                self.matrix[6 + j, i] = next(gen)

        for j in range(2):
            for i in range(1, 18 - 1):
                self.matrix[12 + j, i] = next(gen)

        for i in range(2, 18 - 2):
            self.matrix[14, i] = next(gen)

        for i in range(3, 18 - 3):
            self.matrix[15, i] = next(gen)

        for i in range(4, 18 - 4):
            self.matrix[16, i] = next(gen)

        for i in range(6, 18 - 6):
            self.matrix[17, i] = next(gen)

        for i in range(18):
            for j in range(18):
                if self.matrix[i, j] != -1:
                    self.matrix_inverse[i, j] = 0

mammograph_matrix = MammographMatrix().matrix

def txt_file_to_x(path, mammograph_matrix):
	with open(path, encoding='cp1251') as f:
		need_check = True
		lst = []
		for line in f.readlines():
			if need_check and line.count('0;') != 0:
				need_check = False
			elif not need_check:
				pass
			else:
				continue

			one_x = np.zeros((18, 18))
			line = line[:-2].split(';')

			for i in range(18):
				for j in range(18):
					one_x[i, j] = int(line[i * 18 + j])
				lst.append(one_x)

		x = np.zeros((18, 18, 18, 18))

		for i in range(18):
			for j in range(18):
				if mammograph_matrix[i, j] != -1:
					x[i, j] = lst[mammograph_matrix[i, j] - 1]
	return x


def draw_plots(fname):

	parser = parse_mammograph_raw_data
	if (fname[-4:]) == '.bin':
		data = read_from_file_binary(BINSDIR + f'/{fname}')
		arr = parser(data)
		x = meas_to_x(arr)
		x = x[0][0]
	elif (fname[-4:]) == '.txt':
		x = txt_file_to_x(BINSDIR + f'/{fname}', mammograph_matrix)

	#make_my_plot(x, figursize = (20,20), toSave = True, 
   # 	filename = f'vizualizations/images/{fname}/3dplot', euclid_colors = True)

	fig = plt.figure(figsize=(10,10))
	plt.imshow(matrix_voltage_error(x, mammograph_matrix), cmap = 'hot')
	plt.savefig(f'vizualizations/images/{fname}/matrix_voltage_error.jpg')
	plt.close()

	for act in ['l', 'g']:
		for i in range(18):
			for j in range(18):
				if (act == 'l'):
					img1 = x[i, j, :, :]

				else:
					img1 = x[:, :, i, j]

				# возможно стоит поменять аргументы
				img2 = deviance(x, mammograph_matrix, (i, j, act), rank = 1)
				img3 = meas(x, mammograph_matrix, (i, j, act), rank =1)


				fig = plt.figure(figsize=(5,5))
				plt.imshow(img1, cmap = 'hot')
				plt.title('slice')
				plt.savefig(f'vizualizations/images/{fname}/slice{i}_{j}_{act}.jpg')
				plt.close()

				fig = plt.figure(figsize=(5,5))
				plt.imshow(img2, cmap = 'hot')
				plt.title('deviance')
				plt.savefig(f'vizualizations/images/{fname}/deviance{i}_{j}_{act}.jpg')
				plt.close()

				fig = plt.figure(figsize=(5,5))
				plt.imshow(img3, cmap = 'hot')
				plt.title('meas')
				plt.savefig(f'vizualizations/images/{fname}/meas{i}_{j}_{act}.jpg')	
				plt.close()

	IMGSNAMES = os.listdir(f'vizualizations/images/{fname}')
	with ZipFile(f'vizualizations/images/{fname}/{fname[:-4]}.zip', 'w') as zipObj:
		for imgname in IMGSNAMES:
			zipObj.write(f'vizualizations/images/{fname}/{imgname}', fname + '/' + imgname)


def isnew(list_of_files):

	dif = np.setdiff1d(os.listdir(BINSDIR), list_of_files)
	if len(dif) > 0:
		print('i have new file' + str(dif))
		for el in dif:
	  		os.mkdir('vizualizations/images/' + el)
	  		draw_plots(el)
	  		list_of_files.append(el)
 
list_of_files = [] 
list_of_files = list_of_files + os.listdir('vizualizations/images')
while(True):
	isnew(list_of_files)
	time.sleep(1)
