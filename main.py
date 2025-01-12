import os
import random
import re
from tkinter import Tk, Canvas, Label, Button, StringVar, Listbox, Scrollbar, Frame, Toplevel, filedialog
from tkinter import OptionMenu
from PIL import Image, ImageTk

def show_credits(root):
    """Muestra los créditos al estilo Star Wars en una ventana emergente."""
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

    # Crear una nueva ventana emergente para los créditos
    credits_window = Toplevel(root)
    credits_window.title("Créditos")
    credits_window.geometry("1000x800")
    credits_window.config(bg="black")

    # Crear un lienzo para el efecto de desplazamiento de los créditos
    canvas = Canvas(credits_window, width=600, height=600, bg="black", bd=0, highlightthickness=0)
    canvas.pack()

    # Crear un texto que simula los créditos de Star Wars
    text = canvas.create_text(300, 600, text=credits_text, fill="yellow", font=("Courier", 18), anchor="center")

    # Función para mover el texto hacia arriba
    def move_text():
        canvas.move(text, 0, -2)  # Mover el texto hacia arriba
        if canvas.coords(text)[1] > -canvas.bbox(text)[3]:
            credits_window.after(20, move_text)  # Mover el texto cada 20ms
        else:
            credits_window.destroy()  # Cerrar la ventana después de que el texto salga de la pantalla

    move_text()



def display_images():
    """Muestra las imágenes en una ventana gráfica con botones de navegación, lista y configuración."""
    formats = (".png", ".jpg")
    images = [file for file in os.listdir(os.getcwd()) if file.lower().endswith(formats)]

    # Ordenar las imágenes por número en el nombre (por ejemplo, 1.png, 2.jpg)
    def extract_number(filename):
        """Extrae el número de la imagen a partir de su nombre para ordenarlo numéricamente."""
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    images.sort(key=extract_number)

    if not images:
        print("No hay imágenes en la carpeta actual.")
        return

    def show_image(index):
        """Muestra la imagen seleccionada en el lienzo."""
        if 0 <= index < len(images):
            image_path = os.path.join(os.getcwd(), images[index])
            img = Image.open(image_path)

            # Redimensionar la imagen para un formato más grande
            img = img.resize((img_width, img_height))

            img_tk = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor="center")
            canvas.image = img_tk
            label.config(text=f"{images[index]} ({index + 1}/{len(images)})")
            listbox.selection_clear(0, "end")
            listbox.selection_set(index)

    def on_listbox_select(event):
        """Muestra la imagen seleccionada desde la lista."""
        selected = listbox.curselection()
        if selected:
            show_image(selected[0])
            nonlocal current_index
            current_index = selected[0]

    def next_image():
        """Muestra la siguiente imagen."""
        nonlocal current_index
        if current_index < len(images) - 1:
            current_index += 1
            show_image(current_index)

    def prev_image():
        """Muestra la imagen anterior."""
        nonlocal current_index
        if current_index > 0:
            current_index -= 1
            show_image(current_index)

    def toggle_mode():
        """Alterna entre modo claro y oscuro."""
        if mode.get() == "Claro":
            mode.set("Oscuro")
            root.config(bg="black")
            frame.config(bg="black")
            canvas.config(bg="black")
            label.config(bg="black", fg="white")
            listbox.config(bg="black", fg="white")
        else:
            mode.set("Claro")
            root.config(bg="white")
            frame.config(bg="white")
            canvas.config(bg="white")
            label.config(bg="white", fg="black")
            listbox.config(bg="white", fg="black")

    def open_settings():
        """Abre la ventana de configuraciones."""
        settings_window = Toplevel(root)
        settings_window.title("Configuraciones")
        settings_window.geometry("300x300")

        # Opciones de visualización
        display_option_label = Label(settings_window, text="Orden de visualización:")
        display_option_label.pack()

        # Opciones de orden
        display_option_menu = OptionMenu(settings_window, display_order, *["Alfabético", "Aleatorio", "Por Fecha", "Numérico"])
        display_option_menu.pack()

        # Opciones de tamaño
        size_label = Label(settings_window, text="Tamaño de imagen:")
        size_label.pack()

        size_option_menu = OptionMenu(settings_window, img_size, *["Pequeño", "Mediano", "Grande"])
        size_option_menu.pack()

        # Filtro de formato
        format_label = Label(settings_window, text="Filtrar imágenes por formato:")
        format_label.pack()

        format_option_menu = OptionMenu(settings_window, img_format, *["PNG", "JPG", "Ambos"])
        format_option_menu.pack()

        # Alternar modo oscuro
        dark_mode_button = Button(settings_window, text="Alternar Modo", command=toggle_mode)
        dark_mode_button.pack(pady=10)

        # Mostrar créditos
        credits_button = Button(settings_window, text="Ver Créditos", command=lambda: show_credits(root))
        credits_button.pack(pady=10)

        # Aplicar cambios
        apply_button = Button(settings_window, text="Aplicar", command=apply_settings)
        apply_button.pack(pady=10)

        # Cerrar configuración
        Button(settings_window, text="Cerrar", command=settings_window.destroy).pack(pady=10)

    def apply_settings():
        """Aplica la configuración de orden, tamaño y formato."""
        nonlocal images, img_width, img_height
        # Obtener formato
        selected_format = img_format.get()
        if selected_format == "PNG":
            images = [img for img in images if img.endswith(".png")]
        elif selected_format == "JPG":
            images = [img for img in images if img.endswith(".jpg")]
        else:
            # Si el formato seleccionado es "Ambos", tomamos todas las imágenes
            images = [file for file in os.listdir(os.getcwd()) if file.lower().endswith(formats)]

        # Aplicar el orden de visualización
        if display_order.get() == "Aleatorio":
            random.shuffle(images)
        elif display_order.get() == "Por Fecha":
            images.sort(key=lambda x: os.path.getmtime(x))
        elif display_order.get() == "Numérico":
            images.sort(key=extract_number)

        # Ajustar tamaño de las imágenes
        if img_size.get() == "Pequeño":
            img_width, img_height = 200, 200
        elif img_size.get() == "Mediano":
            img_width, img_height = 400, 400
        else:
            img_width, img_height = 1200, 675  # Tamaño grande en formato horizontal

        # Actualizar lista de imágenes
        listbox.delete(0, "end")
        for img in images:
            listbox.insert("end", img)
        show_image(0)

    def add_new_images():
        """Agrega nuevas imágenes a la carpeta y las renombra según el siguiente número disponible."""
        nonlocal images
        file_paths = filedialog.askopenfilenames(title="Selecciona imágenes", filetypes=[("Imágenes", "*.png *.jpg")])
        if not file_paths:
            return

        # Obtener el número más alto existente
        existing_numbers = [extract_number(img) for img in images]
        max_number = max(existing_numbers) if existing_numbers else 0

        # Copiar las nuevas imágenes con el siguiente número disponible
        for i, file_path in enumerate(file_paths):
            new_number = max_number + i + 1
            ext = os.path.splitext(file_path)[1]
            new_name = f"{new_number}{ext}"
            new_path = os.path.join(os.getcwd(), new_name)
            os.rename(file_path, new_path)

        # Actualizar la lista de imágenes
        images = [file for file in os.listdir(os.getcwd()) if file.lower().endswith(formats)]
        images.sort(key=extract_number)

        listbox.delete(0, "end")
        for img in images:
            listbox.insert("end", img)
        show_image(0)

    def generate_readme():
        """Genera un archivo README.md con la lista de imágenes."""
        with open("README.md", "w", encoding="utf-8") as readme:
            readme.write("# Wallpapers\n")
            readme.write("Lista de fondos de pantalla:\n\n")
            for i, image in enumerate(images, start=1):
                readme.write(f"{i}. ![Descripción de la imagen {i}]({image})\n")
        print("README.md generado correctamente.")

    current_index = 0
    img_width, img_height = 1200, 675  # Tamaño predeterminado grande
    canvas_width, canvas_height = 1200, 655  # Tamaño del lienzo

    root = Tk()
    root.title("Visor de Imágenes")
    root.geometry("1400x800")  # Ventana más grande para acomodar el formato

    mode = StringVar(value="Claro")  # Modo inicial: Claro
    display_order = StringVar(value="Numérico")  # Orden de visualización predeterminado: "Numérico"
    img_size = StringVar(value="Grande")  # Tamaño de imagen por defecto: "Grande"
    img_format = StringVar(value="Ambos")  # Filtro de formato

    # Marco superior para el lienzo y los botones
    frame = Frame(root, bg="white")
    frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    # Lienzo para mostrar la imagen
    canvas = Canvas(frame, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(side="left", padx=10)

    # Lista de imágenes con barra de desplazamiento
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    listbox = Listbox(frame, yscrollcommand=scrollbar.set, height=25, bg="white", fg="black")
    listbox.pack(side="right", fill="y")
    scrollbar.config(command=listbox.yview)

    # Añade imágenes a la lista
    for img in images:
        listbox.insert("end", img)

    # Muestra la imagen seleccionada al hacer clic en la lista
    listbox.bind("<<ListboxSelect>>", on_listbox_select)

    # Etiqueta con el nombre de la imagen actual
    label = Label(root, text="", bg="white", fg="black")
    label.pack(pady=10)

    # Botones de navegación
    Button(root, text="<< Anterior", command=prev_image).pack(side="left", padx=10)
    Button(root, text="Siguiente >>", command=next_image).pack(side="right", padx=10)

    # Botón de configuraciones
    Button(root, text="Configuraciones", command=open_settings).pack()

    # Crear un marco horizontal para los botones "Agregar Fondos de Pantalla" y "Generar README.md"
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Botón para agregar nuevas imágenes
    Button(button_frame, text="Agregar Fondos de Pantalla", command=add_new_images).pack(side="left", padx=10)

    # Botón para generar README.md
    Button(button_frame, text="Generar README.md", command=generate_readme).pack(side="left", padx=10)

    show_image(current_index)
    root.mainloop()

if __name__ == "__main__":
    display_images()
