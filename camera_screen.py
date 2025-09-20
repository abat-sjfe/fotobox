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
		# Button oben links: transparent, weißer Rand, schwarzer Text, Text 'Foto'
		self.capture_button = tk.Button(
			root,
			text="Foto",
			command=self.capture_image,
			bg=self.root['bg'],  # Hintergrund wie Fenster
			fg="black",
			activebackground=self.root['bg'],
			activeforeground="black",
			borderwidth=2,
			highlightthickness=2,
			highlightbackground="white",
			highlightcolor="white",
			font=("Arial", 14, "bold")
		)
		self.capture_button.place(x=0, y=0, width=90, height=44)
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
