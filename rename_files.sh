#!/bin/bash

# Set the directory path
directory="/run/media/poncho/NEW VOLUME/"

# Change to the directory
cd "$directory"

# Counter for renaming
counter=144

# Loop through each file in the directory
for file in *; do
  # Check if it's a regular file
   if [ -f "$file" ] && [ "$file" != "README.md" ]&& [ "$file" != "rename-files.md" ]; then
    # Get the file extension
    extension="${file##*.}"
    
    # Create the new file name with the counter and original extension
    new_name="$counter.$extension"
    
    # Rename the file
    mv "$file" "$new_name"
    
    # Increment the counter
    ((counter++))
  fi
done

echo "Files have been renamed."

