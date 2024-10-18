from PIL import Image, ImageTk  # To handle background images

# Base class for image handling
class ImageHandler:
    """Base class for managing images."""

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None

    def load_image(self):
        """Load and resize the image. This is an abstract method."""
        raise NotImplementedError("Subclasses should implement this!")

# Derived class to handle background images for the GUI
class BackgroundImage(ImageHandler):
    def __init__(self, image_path):
        super().__init__(image_path)  # Call the parent constructor to set image_path

    def load_image(self):
        """Load the background image and resize it."""
        try:
            background_image = Image.open(self.image_path)
            bg_img_resized = background_image.resize((1920, 1080), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(bg_img_resized)
        except FileNotFoundError:
            raise Exception("Background image not found.")
        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")
