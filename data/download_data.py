import kagglehub
import shutil
import os

# Download latest version
path = kagglehub.dataset_download("rajanand/crime-in-india")
print("Path to dataset files:", path)

# See what files were downloaded
for f in os.listdir(path):
    print(f)

# Copy the files to your project's raw/ folder
dest = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(dest, exist_ok=True)

for f in os.listdir(path):
    shutil.copy(os.path.join(path, f), os.path.join(dest, f))

print("Files copied to backend/data/raw/")