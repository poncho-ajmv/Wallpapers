import os

# Define the path where your images are stored
path = '.'  # Change this to your image directory if needed

# Get all image files
image_files = [f for f in os.listdir(path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Create the README.md content
readme_content = "# Wallpapers\nEverything Wallpapers personal\n"

for i, image in enumerate(image_files, start=1):
    readme_content += f"{i}. ![Descripción de la imagen {i}]({image})\n"

# Write to README.md
with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)

print("README.md generated successfully!")

