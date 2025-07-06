import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import cv2
import numpy as np

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")
        self.image_path = None
        self.original_image = None
        self.modified_image = None

        # Create a frame for the controls
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Create a load image button
        self.load_button = tk.Button(control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create sliders
        self.blur_slider = tk.Scale(control_frame, from_=0, to=10, orient=tk.HORIZONTAL, label="Blurriness", command=self.update_image)
        self.blur_slider.pack(side=tk.LEFT, padx=5, pady=5)

        self.contrast_slider = tk.Scale(control_frame, from_=1, to=3, orient=tk.HORIZONTAL, label="Contrast", command=self.update_image)
        self.contrast_slider.pack(side=tk.LEFT, padx=5, pady=5)

        self.sharpness_slider = tk.Scale(control_frame, from_=0, to=10, orient=tk.HORIZONTAL, label="Sharpness", command=self.update_image)
        self.sharpness_slider.pack(side=tk.LEFT, padx=5, pady=5)

        self.canny_slider_low = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Canny Low Threshold", command=self.update_image)
        self.canny_slider_low.pack(side=tk.LEFT, padx=5, pady=5)

        self.canny_slider_high = tk.Scale(control_frame, from_=100, to=200, orient=tk.HORIZONTAL, label="Canny High Threshold", command=self.update_image)
        self.canny_slider_high.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a save button
        self.save_button = tk.Button(control_frame, text="Save as PDF", command=self.save_as_pdf)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a frame to hold the image
        self.image_frame = tk.Label(self)
        self.image_frame.pack(expand=True, fill=tk.BOTH)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)
            self.display_image(self.original_image)
            self.modified_image = self.original_image.copy()

    def display_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_frame.config(image=img)
        self.image_frame.image = img

    def update_image(self, *args):
        if self.original_image is None:
            return
        # Convert to grayscale
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), self.blur_slider.get())
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, self.canny_slider_low.get(), self.canny_slider_high.get())
        
        # Invert the image to create a white background
        inverted = cv2.bitwise_not(edges)
        
        # Convert the inverted image to RGB for display
        img_rgb = cv2.cvtColor(inverted, cv2.COLOR_GRAY2RGB)
        
        # Apply additional image enhancements
        img_pil = Image.fromarray(img_rgb)
        img_pil = ImageEnhance.Contrast(img_pil).enhance(self.contrast_slider.get())
        img_pil = ImageEnhance.Sharpness(img_pil).enhance(self.sharpness_slider.get())
        
        self.modified_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        self.display_image(self.modified_image)

    def save_as_pdf(self):
        if self.modified_image is None:
            return
        save_path = self.image_path.replace(".jpg", "_cb_output.pdf").replace(".png", "_cb_output.pdf")
        cv2.imwrite(save_path.replace(".pdf", ".jpg"), self.modified_image)
        img = Image.open(save_path.replace(".pdf", ".jpg"))
        img.save(save_path, "PDF", resolution=100.0)
        print(f"PDF saved as {save_path}")

if __name__ == "__main__":
    app = ImageEditor()
    app.mainloop()
