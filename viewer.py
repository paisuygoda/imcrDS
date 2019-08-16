from PIL import Image, ImageTk
import tkinter as tk
import glob
import os
import sys
import pickle


PATH = ""
WIDTH = 300
HEIGHT = 300

class Viewer(tk.Frame):

	def show_image(self):
		self.raw_img = Image.open(self.image_list[self.cursor]).convert('RGB')
		width_rate = self.width / self.raw_img.width
		height_rate = self.height / self.raw_img.height
		rate = min(width_rate, height_rate)
		self.raw_img = self.raw_img.resize((int(self.raw_img.width * rate), int(self.raw_img.height * rate)), resample=0)
		self.img = ImageTk.PhotoImage(self.raw_img)
		self.label.config(image=self.img, bg="#000000")

	def get_next(self):
		loop = 0
		while(True):
			if loop == len(self.image_list):
				raise Exception

			self.cursor += 1
			loop += 1
			if self.cursor >= len(self.image_list):
				self.cursor = 0
			if self.good_mode:
				if self.image_list[self.cursor] in self.good_set:
					break
			else:
				if not self.drop_mode:
					if self.image_list[self.cursor] in self.good_set:
						continue
				if not (self.image_list[self.cursor] in self.bad_set):
					break

		self.history.append(self.cursor)
		self.show_image()
		
	def prev(self, event):
		if len(self.history) < 2:
			return

		self.history = self.history[:-1]
		self.cursor = self.history[-1]
		self.show_image()

	def mode_drop(self, event):
		self.drop_mode = True
		self.good_mode = False

	def mode_new(self, event):
		self.drop_mode = False
		self.good_mode = False

	def mode_good(self, event):
		self.good_mode = True
		self.drop_mode = False

	def quit(self, event):
		self.frame.quit()

	def leave(self, event):
		if self.image_list[self.cursor] in self.bad_set:
			self.bad_set.remove(self.image_list[self.cursor])
		self.good_set.add(self.image_list[self.cursor])
		with open('data/good_set.p', mode='wb') as gl:
			pickle.dump(self.good_set, gl)
		try:
			self.get_next()
		except:
			self.frame.quit()

	def drop(self, event):
		if self.image_list[self.cursor] in self.good_set:
			self.good_set.remove(self.image_list[self.cursor])
		self.bad_set.add(self.image_list[self.cursor])
		with open('data/bad_set.p', mode='wb') as bl:
			pickle.dump(self.bad_set, bl)
		try:
			self.get_next()
		except:
			self.frame.quit()

	def __init__(self):
		self.frame = tk.Tk()
		super().__init__(self.frame)
		self.label = tk.Label(self)
		self.label.pack()

		self.width = WIDTH
		self.height = HEIGHT
		self.drop_mode = True
		self.good_mode = False
		self.frame.geometry(str(WIDTH) + "x" + str(HEIGHT))
		self.frame.title("Viewer")
		self.history = []

		self.frame.bind("<Key-d>", self.mode_drop)
		self.frame.bind("<Key-n>", self.mode_new)
		self.frame.bind("<Left>", self.prev)
		self.frame.bind("<Escape>", self.quit)
		self.frame.bind("<Return>", self.leave)
		self.frame.bind("<BackSpace>", self.drop)
		self.frame.focus_set()
		
		self.image_list = glob.glob(PATH + "/*")
		
		if os.path.exists('data/cursor'):
			with open('data/cursor', mode='r') as rt:
				s = rt.read()
				self.cursor = self.image_list.index(s)
		else:
			self.cursor = 0

		if os.path.exists('data/bad_set.p'):
			with open('data/bad_set.p', mode='rb') as bl:
				self.bad_set = pickle.load(bl)
		else:
			self.bad_set = set()

		if os.path.exists('data/good_set.p'):
			with open('data/good_set.p', mode='rb') as gl:
				self.good_set = pickle.load(gl)
		else:
			self.good_set = set()

		self.pack()


if len(sys.argv) < 2:
	print("path?")
	PATH = input()
else:
	PATH = sys.argv[1]

if os.path.exists(PATH):
	viewer = Viewer()
	viewer.mainloop()
else:
	print("path does not exist!")