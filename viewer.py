from PIL import Image, ImageTk
import tkinter as tk
import glob
import os
import sys
import pickle

class Viewer(tk.Frame):

	def show_image(self):
		self.raw_img = Image.open(self.image_list[self.cursor]).convert('RGB')
		width_rate = self.width / self.raw_img.width()
		height_rate = self.height / self.raw_img.height()
		rate = min(width_rate, height_rate)
		self.raw_img = self.raw_img.resize(int(self.raw_img.width() * rate), int(self.raw_img.height() * rate))
		self.img = ImageTk.PhotoImage(self.raw_img)
		self.label.config(image=self.img, bg="#000000", width=self.img.width, height=self.img.height)

	def get_next(self):
		loop = 0
		while(True):
			if loop == len(self.image_list):
				raise Exception

			self.cursor += 1
			loop += 1
			if self.cursor >= len(self.image_list):
				self.cursor = 0
			if not drop_mode:
				if self.image_list[self.cursor] in self.good_list:
					continue
			if not (self.image_list[self.cursor] in self.bad_list):
				break

		show_image()
		


	def mode_drop(self):
		self.drop_mode = True

	def mode_new(self):
		self.drop_mode = False

	def leave(self):
		self.good_list += self.image_list[self.cursor]
		with open('good_list.p', mode='wb') as gl:
			pickle.dump(self.good_list, gl)
		get_next()

	def drop(self):
		self.bad_list += self.image_list[self.cursor]
		with open('bad_list.p', mode='wb') as bl:
			pickle.dump(self.bad_list, bl)
		get_next()

		def __init__(self):
			self.frame = tk.Tk()
			super().__init__(self.frame)
			self.label = tk.Label(self)
			self.label.pack()

			self.width = width
			self.height = height
			self.drop_mode = True
			self.frame.geometry(str(width) + "x" + str(height))
			self.frame.title("Viewer")

			self.frame.bind("<Key-d>", mode_drop)
			self.frame.bind("<Key-n>", mode_new)
			self.frame.bind("<Key-Enter>", leave)
			self.frame.bind("<Key-BackSpace>", drop)
			self.frame.focus_set()
			
			self.image_list = glob.glob(path + "*")
			
			with open('cursor', mode='r') as rt:
				s = rt.read()
				self.cursor = self.image_list.index(s)
			if os.path.exists('bad_list.p'):
				with open('bad_list.p', mode='rb') as bl:
					self.bad_list = pickle.load(bl)
			else:
				self.bad_list = set()

			if os.path.exists('good_list.p'):
				with open('good_list.p', mode='rb') as gl:
					self.good_list = pickle.load(gl)
			else:
				self.good_list = set()

			self.pack()


if len(sys.argv) < 2:
	print("path?")
	path = input()
else:
	path = sys.argv[1]

if os.path.exists(path):
	viewer = Viewer()
	viewer.path = path
	viewer.width = 300
	viewer.height = 300
	viewer.mainloop()
else:
	print("path does not exist!")