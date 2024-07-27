import re
from pathlib import Path

def humanize_class_name(name):
    """Convert CamelCase to human-readable string"""
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', name).replace('_', ' ').capitalize()

def add_description_to_model(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    model_found = False
    description_added = False

    for line in lines:
        class_match = re.match(r'class (\w+)\(models\.Model\):', line)
        if class_match:
            model_found = True
            class_name = class_match.group(1)
            human_readable_name = humanize_class_name(class_name)
            modified_lines.append(line)
        elif model_found and (re.search(r'^\s*_name\s*=', line) or re.search(r'^\s*_inherit\s*=', line)):
            modified_lines.append(line)
            if not description_added:
                modified_lines.append(f"    _description = \"{human_readable_name}\"\n")
                description_added = True
        else:
            modified_lines.append(line)

    if model_found and not description_added:
        for i, line in enumerate(modified_lines):
            if re.match(r'class \w+\(models\.Model\):', line):
                modified_lines.insert(i + 1, f"    _description = \"{human_readable_name}\"\n")
                break

    if model_found:
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
        print(f"Updated {file_path}")

# Define the directory to search for Python files
models_directory = Path('D:\\ACS\\acslogco17\\eit_freight_MasterData\\models')

# List all Python files in the directory without checking for __init__.py
extracted_files = [str(file) for file in models_directory.rglob('*.py')]

# Process all Python files in the models directory
for file_path in extracted_files:
    if file_path.endswith('.py'):
        add_description_to_model(file_path)
