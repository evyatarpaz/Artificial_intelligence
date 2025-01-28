import os
import subprocess

# Get the directory above the current one
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

check_script = os.path.join(current_dir, "check.py")

# Iterate over files in the parent directory
for filename in os.listdir(parent_dir):
    if filename.endswith("vector.npz"):
        # Construct the output file name
        output_file = os.path.join(parent_dir, f"{filename}.txt")
        
        # Run check.py and redirect output
        with open(output_file, 'w') as outfile:
            subprocess.run(["python", check_script, filename], stdout=outfile)