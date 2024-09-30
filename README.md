# Generador de README.md para Wallpapers

# Definir el número total de imágenes
total_imagenes = 219  # Cambia esto al número total de imágenes que tienes

# Crear el contenido del README.md
contenido = "# Wallpapers\nEverything Wallpapers personal\n"

# Generar las entradas de imágenes
for i in range(1, total_imagenes + 1):
    # Suponiendo que las imágenes están en el formato 'i.jpg' o 'i.png'
    jpg = f"{i}.jpg"
    png = f"{i}.png"
    
    # Agregar la entrada para el formato JPG
    contenido += f"{i}. ![Descripción de la imagen {i}]({jpg})\n"
    
    # Si hay un archivo PNG correspondiente, agregar también
    if i % 20 == 0:  # Ejemplo para incluir PNGs cada 20 imágenes
        contenido += f"{i + 1}. ![Descripción de la imagen {i + 1}]({png})\n"

# Guardar el contenido en README.md
with open("README.md", "w") as archivo:
    archivo.write(contenido)

print("README.md ha sido generado.")
