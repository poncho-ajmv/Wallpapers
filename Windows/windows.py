#Windows version

import os
import random
import re
import platform
from tkinter import Tk, Canvas, Label, Button, StringVar, Listbox, Scrollbar, Frame, Toplevel, OptionMenu, filedialog
from PIL import Image, ImageTk

# === CONFIGURACIÓN DE RUTA PARA CARGAR IMÁGENES DESDE /imagenes EN NIVEL SUPERIOR ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_FOLDER = os.path.join(BASE_DIR, "imagenes")
os.makedirs(IMAGES_FOLDER, exist_ok=True)

def show_credits(root):
    credits_text = """
    Créditos de la Aplicación:

    Desarrollador: poncho_ajmv
    Licencia: MIT License
    Condiciones de uso:
    - Se permite el uso, copia, modificación 
    y distribución del software, siempre que 
    se incluya este aviso de licencia.
    - No se permite el uso del software para 
    fines comerciales.

    Agradecemos profundamente su preferencia 
    por esta aplicación.

    Todos los derechos reservados.
    """

    credits_window = Toplevel(root)
    credits_window.title("Créditos")
    credits_window.geometry("1000x800")
    credits_window.config(bg="black")

    canvas = Canvas(credits_window, width=600, height=600, bg="black", bd=0, highlightthickness=0)
    canvas.pack()

    text = canvas.create_text(300, 600, text=credits_text, fill="yellow", font=("Courier", 18), anchor="center")

    def move_text():
        canvas.move(text, 0, -2)
        if canvas.coords(text)[1] > -canvas.bbox(text)[3]:
            credits_window.after(20, move_text)
        else:
            credits_window.destroy()

    move_text()

def display_images():
    formats = (".png", ".jpg")
    images = [file for file in os.listdir(IMAGES_FOLDER) if file.lower().endswith(formats)]

    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    images.sort(key=extract_number)
    if not images:
        print("No hay imágenes en la carpeta 'imagenes'.")
        return

    def show_image(index):
        if 0 <= index < len(images):
            image_path = os.path.join(IMAGES_FOLDER, images[index])
            img = Image.open(image_path)
            original_width, original_height = img.size

            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            # Default fallback if sizes are not ready
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 800
                canvas_height = 600

            if img_size.get() == "Grande":
                img_ratio = original_width / original_height
                canvas_ratio = canvas_width / canvas_height

                if img_ratio > canvas_ratio:
                    new_width = canvas_width
                    new_height = int(canvas_width / img_ratio)
                else:
                    new_height = canvas_height
                    new_width = int(canvas_height * img_ratio)

            elif img_size.get() == "Mediano":
                new_width = int(original_width * 0.7)
                new_height = int(original_height * 0.7)

            elif img_size.get() == "Pequeño":
                new_width = int(original_width * 0.4)
                new_height = int(original_height * 0.4)

            else:
                new_width, new_height = original_width, original_height

            # Validación para evitar resize con valores inválidos
            new_width = max(1, new_width)
            new_height = max(1, new_height)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor="center")
            canvas.image = img_tk
            label.config(text=f"{images[index]} ({index + 1}/{len(images)})")
            listbox.selection_clear(0, "end")
            listbox.selection_set(index)


    def on_listbox_select(event):
        selected = listbox.curselection()
        if selected:
            show_image(selected[0])
            nonlocal current_index
            current_index = selected[0]

    def next_image():
        nonlocal current_index
        if current_index < len(images) - 1:
            current_index += 1
            show_image(current_index)

    def prev_image():
        nonlocal current_index
        if current_index > 0:
            current_index -= 1
            show_image(current_index)

    def toggle_mode():
        if mode.get() == "Claro":
            mode.set("Oscuro")
            apply_dark_mode()
        else:
            mode.set("Claro")
            apply_light_mode()

    def apply_dark_mode():
        root.config(bg="black")
        frame.config(bg="black")
        canvas.config(bg="black")
        label.config(bg="black", fg="white")
        listbox.config(bg="black", fg="white")

    def apply_light_mode():
        root.config(bg="white")
        frame.config(bg="white")
        canvas.config(bg="white")
        label.config(bg="white", fg="black")
        listbox.config(bg="white", fg="black")

    def open_settings():
        settings_window = Toplevel(root)
        settings_window.title("Configuraciones")
        settings_window.geometry("500x750")
        settings_window.config(bg="black")

        label_font = ("Helvetica", 14, "bold")
        button_font = ("Helvetica", 13, "bold")

        Label(settings_window, text="Orden de visualización:", bg="black", fg="white", font=label_font).pack(pady=5)
        OptionMenu(settings_window, display_order, *["Alfabético", "Aleatorio", "Por Fecha", "Numérico"]).pack(pady=5)

        Label(settings_window, text="Tamaño de imagen:", bg="black", fg="white", font=label_font).pack(pady=5)
        OptionMenu(settings_window, img_size, *["Pequeño", "Mediano", "Grande"]).pack(pady=5)

        Label(settings_window, text="Filtrar imágenes por formato:", bg="black", fg="white", font=label_font).pack(pady=5)
        OptionMenu(settings_window, img_format, *["PNG", "JPG", "Ambos"]).pack(pady=5)

        for text, command in [
            ("Alternar Modo", toggle_mode),
            ("Ver Créditos", lambda: show_credits(root)),
            ("Aplicar", apply_settings),
            ("Cerrar", settings_window.destroy)
        ]:
            Button(settings_window, text=text, command=command, font=button_font, height=2, width=20,
                   bg="#444444", fg="white", activebackground="#666666", activeforeground="white").pack(pady=10)

    def apply_settings():
        nonlocal images
        selected_format = img_format.get()
        if selected_format == "PNG":
            images = [img for img in images if img.endswith(".png")]
        elif selected_format == "JPG":
            images = [img for img in images if img.endswith(".jpg")]
        else:
            images = [file for file in os.listdir(IMAGES_FOLDER) if file.lower().endswith(formats)]

        if display_order.get() == "Aleatorio":
            random.shuffle(images)
        elif display_order.get() == "Por Fecha":
            images.sort(key=lambda x: os.path.getmtime(os.path.join(IMAGES_FOLDER, x)))
        elif display_order.get() == "Numérico":
            images.sort(key=extract_number)

        listbox.delete(0, "end")
        for img in images:
            listbox.insert("end", img)
        show_image(0)

    def add_new_images():
        nonlocal images
        file_paths = filedialog.askopenfilenames(
            title="Selecciona imágenes",
            filetypes=[("Imágenes", "*.png *.jpg")]
        )
        if not file_paths:
            return

        existing_numbers = [extract_number(img) for img in images]
        max_number = max(existing_numbers) if existing_numbers else 0

        for i, file_path in enumerate(file_paths):
            new_number = max_number + i + 1
            ext = os.path.splitext(file_path)[1]
            new_name = f"{new_number}{ext}"
            new_path = os.path.join(IMAGES_FOLDER, new_name)
            os.rename(file_path, new_path)

        images = [file for file in os.listdir(IMAGES_FOLDER) if file.lower().endswith(formats)]
        images.sort(key=extract_number)

        listbox.delete(0, "end")
        for img in images:
            listbox.insert("end", img)
        show_image(0)

    def generate_readme():
        with open(os.path.join(BASE_DIR, "README.md"), "w", encoding="utf-8") as readme:
            readme.write("# Wallpapers\nLista de fondos de pantalla:\n\n")
            for i, image in enumerate(images, start=1):
                readme.write(f"{i}. ![Descripción de la imagen {i}](imagenes/{image})\n")
        print("README.md generado correctamente.")

    root = Tk()
    root.title("Visor de Imágenes")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")

    mode = StringVar(value="Oscuro")
    display_order = StringVar(value="Numérico")
    img_size = StringVar(value="Grande")
    img_format = StringVar(value="Ambos")

    current_index = 0

    frame = Frame(root, bg="black")
    frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    canvas = Canvas(frame, bg="black")
    canvas.pack(side="left", expand=True, fill="both", padx=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(frame, yscrollcommand=scrollbar.set, height=25, bg="black", fg="white")
    listbox.pack(side="right", fill="y")
    scrollbar.config(command=listbox.yview)

    for img in images:
        listbox.insert("end", img)

    listbox.bind("<<ListboxSelect>>", on_listbox_select)

    label = Label(root, text="", bg="black", fg="white")
    label.pack(pady=10)

    button_style = {
        "height": 3,
        "width": 25,
        "font": ("Helvetica", 14, "bold"),
        "bg": "#444444",
        "fg": "white",
        "activebackground": "#666666",
        "activeforeground": "white"
    }

    Button(root, text="<< Anterior", command=prev_image, **button_style).pack(side="left", padx=10)
    Button(root, text="Siguiente >>", command=next_image, **button_style).pack(side="right", padx=10)
    Button(root, text="\u2699 Configuraciones", command=open_settings, **button_style).pack(pady=10)

    button_frame = Frame(root, bg="black")
    button_frame.pack(pady=10)

    small_button_style = {
        "height": 2,
        "width": 25,
        "font": ("Helvetica", 13, "bold"),
        "bg": "#444444",
        "fg": "white",
        "activebackground": "#666666",
        "activeforeground": "white"
    }

    Button(button_frame, text="Agregar Fondos de Pantalla", command=add_new_images, **small_button_style).pack(side="left", padx=10)
    Button(button_frame, text="Generar README.md", command=generate_readme, **small_button_style).pack(side="left", padx=10)

    apply_dark_mode()
    root.update_idletasks()
    show_image(current_index)
    root.mainloop()

if __name__ == "__main__":
    display_images()
