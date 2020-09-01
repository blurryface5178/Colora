import cv2
import numpy as np

def change(x):
	pass

img = cv2.imread('Abhijan.jpg',cv2.IMREAD_UNCHANGED)
img_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

(height, width, _) = img.shape

img = cv2.resize(img, (round(width/2), round(height/2)))
img_bw = cv2.resize(img_bw, (round(width/2), round(height/2)))

cv2.namedWindow('Settings')
cv2.createTrackbar('Level', 'Settings', 0, 255, change)
cv2.createTrackbar('Smooth', 'Settings', 1, 3, change)
cv2.createTrackbar('Enable Color Manipulation', 'Settings', 0, 1, change)
cv2.createTrackbar('H', 'Settings', 0, 255, change)
cv2.createTrackbar('S', 'Settings', 0, 255, change)
cv2.createTrackbar('V', 'Settings', 0, 255, change)
cv2.createTrackbar('Overlay Edges', 'Settings', 0, 1, change)
cv2.createTrackbar('Threshold', 'Settings', 0, 255, change)

cv2.imshow('Input', img)

while True: 
	lvl = cv2.getTrackbarPos('Level', 'Settings')
	_ , output = cv2.threshold(img, lvl, 255, 0)

	smth = cv2.getTrackbarPos('Smooth', 'Settings')
	output = cv2.blur(output, (smth*2 + 1, smth*2 + 1 ))

	if (cv2.getTrackbarPos('Enable Color Manipulation', 'Settings') == 1):
		output = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
		hue,sat,val = cv2.split(output)
		hue += cv2.getTrackbarPos('H', 'Settings') % 255
		sat += cv2.getTrackbarPos('S', 'Settings') % 255
		val += cv2.getTrackbarPos('V', 'Settings') % 255
		output = cv2.merge((hue,sat,val))

	if (cv2.getTrackbarPos('Overlay Edges', 'Settings') == 1):
		thresh = cv2.getTrackbarPos('Threshold', 'Settings')
		can = cv2.Canny(img, thresh, 255)
		can = cv2.bitwise_not(can)
		can = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
		output = cv2.bitwise_and(output, can)

	cv2.imshow('Output', output)

	#cunt, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#img_bw = cv2.drawContours(img_bw, cunt, -1, (255,255,255), 3)
	
	if cv2.waitKey(1) == ord('q') & 0xff:
		break

cv2.destroyAllWindows()

if __name__ == "__main__":
	main()

