import cv2
import numpy
# myimg = cv2.imread('map_img/block_3_6.jpg')[:, :, ::-1] #если надо поменять порядок на RGB
myimg = cv2.imread('map_img/block_3_6.jpg')
avg_color_per_row = numpy.average(myimg, axis=0)
avg_color = numpy.average(avg_color_per_row, axis=0)
print(avg_color)
