import os
import json
import sys

def has_java_files(dir_path):
    for root, _, files in os.walk(dir_path):
        if any(f.endswith('.java') or f.endswith('.jar') for f in files):
            return True
    return False

if __name__ == "__main__":
    repo_dir = sys.argv[1]
    output_file = sys.argv[2]
    has_java = has_java_files(os.path.join(repo_dir, 'resources/java'))
    with open(output_file, 'w') as f:
        json.dump({"has_java": has_java}, f)