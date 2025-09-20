import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2
import time

class CameraApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Fotobox Kamera")
		self.camera = Picamera2()
		self.camera.start()
		self.preview_label = tk.Label(root)
		self.preview_label.pack()
		# Transparenter Button oben links
		self.capture_button = tk.Button(root, text="capture", command=self.capture_image, bg="white", fg="white", activebackground="white", activeforeground="white", borderwidth=0, highlightthickness=0)
		self.capture_button.place(x=0, y=0, width=80, height=40)
		self.update_preview()

	def update_preview(self):
		# Bild von der Kamera holen
		frame = self.camera.capture_array()
		image = Image.fromarray(frame)
		image = image.resize((640, 480))
		photo = ImageTk.PhotoImage(image=image)
		self.preview_label.configure(image=photo)
		self.preview_label.image = photo
		self.root.after(30, self.update_preview)

	def capture_image(self):
		filename = f"foto_{int(time.time())}.jpg"
		self.camera.capture_file(filename)
		print(f"Foto gespeichert: {filename}")

if __name__ == "__main__":
	root = tk.Tk()
	app = CameraApp(root)
	root.mainloop()
