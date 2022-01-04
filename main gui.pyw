import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *

from PIL import ImageTk
from PIL import Image
import random

class theGui:

	def __init__(self, root):
		root.resizable(True, True)
		root.title('Colora 1.0')
		root.iconbitmap('E:\Colora\icon.ico')

		wrapper = LabelFrame(root, text="Settings", width=500)
		wrapper.pack(fill="y", side="left", padx=20, pady=20)
		self.wrapper = wrapper

		wrapper2 = LabelFrame(root, text="Image", width=500)
		wrapper2.pack(fill="y", expand="true", padx=20, pady=20)
		self.wrapper2 = wrapper2

		self.hue, self.sat, self.val = 127, 127, 127

		self.setLayout()

	def enable(self,x):
		self.show()

	def change(self):
		self.show()

	def packer(self, text_label, low=0, high=255, kind="scale"):
		var = IntVar()
		thingy = Label(self.wrapper, text=text_label)
		thingy.pack()
		if (kind=="scale"):
			thingy2 = Scale(self.wrapper, variable=var, orient='horizontal', from_=low, to=high, length=200, command=self.enable)
			thingy2.pack()
		elif (kind=="check"):
			thingy2 = Checkbutton(self.wrapper, variable=var, justify="left", command=self.change)
			thingy2.pack()
		return var

	def save_img(self):
		path = filedialog.asksaveasfilename(title = "Select file",filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')),defaultextension='.jpg')
		if len(path) > 0:
			cv2.imwrite(path, cv2.cvtColor(self.output,cv2.COLOR_BGR2RGB))

	def reset_bars(self):
		self.mode.set(0)
		self.lvl.set(0)
		self.en_col.set(0)
		self.h.set(0)
		self.s.set(0)
		self.v.set(0)
		self.en_over.set(0)
		self.thresh1.set(0)
		self.thresh2.set(0)
		self.thick.set(0)
		self.show()
		
	def randomize(self):
		self.mode.set(0)
		self.lvl.set(random.randint(50,200))
		self.en_col.set(random.randint(0,1))
		self.h.set(random.randint(50,200))
		self.s.set(random.randint(50,200))
		self.v.set(random.randint(50,200))
		self.en_over.set(random.randint(0,1))
		self.thresh1.set(random.randint(50,200))
		self.thresh2.set(random.randint(50,200))
		self.thick.set(random.randint(0,3))
		self.show()

	def setLayout(self):
		self.mode = self.packer("Mode", low=0, high=4)
		self.lvl = self.packer("Level")
		self.en_col = self.packer("Enable Color Manipulation", kind="check")
		self.h = self.packer("H")
		self.s = self.packer("S")
		self.v = self.packer("V")
		self.en_over = self.packer("Overlay Edges", kind="check")
		self.thresh1 = self.packer("Stroke_L")
		self.thresh2 = self.packer("Stroke_U")
		self.thick = self.packer("Thickness", low=0, high=3)

		self.load = Button(self.wrapper, text="Load", justify="center", command=self.select_image)
		self.load.pack(anchor="sw", padx=5, pady=5)

		self.save = Button(self.wrapper, text="Save", justify="center", command=self.save_img)
		self.save.pack(side="right", padx=5, pady=5)
		
		self.reset = Button(self.wrapper, text="Reset", justify="center", command=self.reset_bars)
		self.reset.pack(side="right", padx=5, pady=5)
		
		self.reset = Button(self.wrapper, text="Randomize", justify="center", command=self.randomize)
		self.reset.pack(side="right", padx=5, pady=5)
		
		self.panelA = Label(self.wrapper2)
		self.panelA.pack(side="left", padx=20, pady=20)

	def select_image(self):
		path = filedialog.askopenfilename()

		if len(path) > 0:
			self.img = cv2.imread(path)
			self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
			(self.width, self.height, _) = self.img.shape
			self.show()
				
	def show(self):
		_ , self.output = cv2.threshold(self.img, self.lvl.get() , 255, self.mode.get())

		if (self.en_col.get() == 1):
			self.output = cv2.cvtColor(self.output, cv2.COLOR_RGB2HSV)
			self.hue,self.sat,self.val = cv2.split(self.output)
			self.hue += self.h.get() % 256
			self.sat += self.s.get() % 256
			self.val += self.v.get() % 256
			self.output = cv2.merge((self.hue,self.sat,self.val))
			self.output = cv2.cvtColor(self.output, cv2.COLOR_HSV2RGB)

		if (self.en_over.get() == 1):
			can = cv2.Canny(self.img, self.thresh1.get(), self.thresh2.get())
			can = cv2.dilate(can, (3,3), iterations=self.thick.get())
			can = cv2.bitwise_not(cv2.cvtColor(can, cv2.COLOR_GRAY2RGB))
			self.output = cv2.bitwise_and(can, self.output)

		self.display = ImageTk.PhotoImage(image=Image.fromarray(cv2.resize(self.output, (round(self.height/2),round(self.width/2)))))
		self.panelA.configure(image=self.display)
		self.panelA.image = self.output

def main():
	root = Tk()
	gui = theGui(root)
	root.mainloop()

if __name__ == "__main__":
	main()