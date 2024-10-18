import tkinter as tk
from tkinter import ttk, messagebox
from image_handler import BackgroundImage  # Import the BackgroundImage class
from translator import Translator  # Import the Translator class

class TranslationApp(tk.Tk):
    """This is the main application class for language translation."""
    
    def __init__(self):
        super().__init__()  # Call parent class constructor
        self.title("SYD194_Language Translation App")
        self.geometry("600x500")
        self.configure(bg="#f0f8ff")  # Default background color
        
        # Load and display the background image
        self.bg_image_handler = BackgroundImage('resources/translator_assets/nepal3.jpg')
        try:
            self.bg_image_handler.load_image()
            self.bg_label = tk.Label(self, image=self.bg_image_handler.image)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", str(e))
            self.destroy()  # Close the application if image loading fails
        
        # Title label with custom font and color
        self.title_label = tk.Label(self, text="Language Translation", font=("Helvetica", 46, "bold"), bg="black", fg="White")
        self.title_label.pack(pady=20)

        # Input text label
        self.input_label = tk.Label(self, text="Enter text to translate:", font=("Helvetica", 20), bg="#f0f8ff", fg="#333333")
        self.input_label.pack(pady=5)

        # Input text box
        self.input_text = tk.Text(self, height=8, width=60, relief=tk.GROOVE, bd=2, font=("Helvetica", 20))
        self.input_text.pack(pady=10)

        # Language selection label
        self.language_label = tk.Label(self, text="Select target language:", font=("Helvetica", 20), bg="#f0f8ff", fg="#333333")
        self.language_label.pack(pady=10)

        # Dropdown menu for different languages
        self.languages = ['fr', 'es', 'de', 'it', 'pt', 'zh', 'ja', 'hi', 'ar']
        self.language_names = {lang: name for lang, name in zip(self.languages, 
                             ['French', 'Spanish', 'German', 'Italian', 'Portuguese', 
                              'Chinese', 'Japanese', 'Hindi', 'Arabic'])}

        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self, textvariable=self.language_var, 
                                               values=list(self.language_names.values()), 
                                               font=("Helvetica", 20))
        self.language_dropdown.pack(pady=20)
        self.language_dropdown.current(0)  # Default language

        # Translate button
        self.translate_button = tk.Button(self, text="Translate", 
                                           font=("Helvetica", 20, "bold"), bg="#2a9df4", 
                                           fg="black", relief=tk.RAISED, bd=5, 
                                           command=self.translate_text)
        self.translate_button.pack(pady=15)
        self.translate_button.bind("<Enter>", self.on_hover)  # Change cursor on hover
        self.translate_button.bind("<Leave>", self.on_leave)

        # Output label
        self.output_label = tk.Label(self, text="Translated text:", font=("Helvetica", 20), bg="#f0f8ff", fg="#333333")
        self.output_label.pack(pady=10)

        # Output text box
        self.output_text = tk.Text(self, height=8, width=60, state=tk.DISABLED, relief=tk.GROOVE, bd=2, font=("Helvetica", 20))
        self.output_text.pack(pady=10)

    def on_hover(self, event):
        """This changes the cursor to a pointer when hovering over the translate button."""
        self.translate_button.config(cursor="hand2")

    def on_leave(self, event):
        """This reverts the cursor back to default when leaving the translate button."""
        self.translate_button.config(cursor="")

    def translate_text(self):
        """This translates the input text to the selected language."""
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()

            if not input_text:
                messagebox.showwarning("Input Error", "Please enter text to translate!")
                return

            selected_language = self.languages[self.language_dropdown.current()]
            translated_text = Translator.translate(input_text, selected_language)  # Use the Translator class

            # Display the translated text
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)
            self.output_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Translation Error", f"Error occurred during translation: {str(e)}")
