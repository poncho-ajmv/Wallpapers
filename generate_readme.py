import os
import re

def rename_images(directory):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    renamed_files = []

    # Contador para la numeración de imágenes
    count = 1

    for filename in os.listdir(directory):
        if filename.lower().endswith(image_extensions):
            # Crear nuevo nombre para la imagen
            new_name = f'{count}{os.path.splitext(filename)[1]}'
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            renamed_files.append(new_name)
            count += 1

    return renamed_files

def generate_readme(directory, images):
    with open(os.path.join(directory, 'README.md'), 'w') as readme:
        readme.write('# Galería de Imágenes\n\n')
        readme.write('Este repositorio contiene una colección de imágenes renombradas automáticamente.\n\n')
        for image in images:
            # Obtener el número de imagen (sin la extensión)
            image_number = os.path.splitext(image)[0]
            readme.write(f'## Imagen {image_number}\n')  # Añadir el número de imagen como encabezado
            readme.write(f'![{image}](./{image})\n\n')

if __name__ == '__main__':
    # Establece la ruta del directorio de imágenes
    directory = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual del script
    renamed_files = rename_images(directory)

    if renamed_files:
        generate_readme(directory, renamed_files)
        print(f'Imágenes renombradas: {renamed_files}')
        print('README.md generado correctamente.')
    else:
        print('No se encontraron imágenes en el directorio especificado.')
