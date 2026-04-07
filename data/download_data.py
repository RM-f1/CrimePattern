import kagglehub
import shutil
import os

path = kagglehub.dataset_download("rajanand/crime-in-india")
print("Path to dataset files:", path)

for f in os.listdir(path):
    print(f)

dest = os.path.join(os.path.dirname(__file__), "raw")
os.makedirs(dest, exist_ok=True)

for f in os.listdir(path):
    shutil.copy(os.path.join(path, f), os.path.join(dest, f))

print("Files copied to backend/data/raw/")