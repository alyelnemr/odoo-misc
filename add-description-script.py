import re
from pathlib import Path


def add_description_to_model(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    model_found = False

    for line in lines:
        if re.match(r'class \w+\(models\.Model\):', line):
            model_found = True
            modified_lines.append(line)
            modified_lines.append("    \"\"\"Description: Model description here\"\"\"\n")
        else:
            modified_lines.append(line)

    if model_found:
        with open(file_path, 'w') as file:
            file.writelines(modified_lines)
        print(f"Updated {file_path}")

odoo_addons_path = 'odoo\\addons'
models_directory = Path('/mnt/data/models/models/')

# List all Python files in the directory
extracted_files = [str(file) for file in models_directory.rglob('*.py') if '__init__' not in str(file)]

# Process all Python files in the models directory
for file_path in extracted_files:
    if file_path.endswith('.py') and '__init__' not in file_path:
        add_description_to_model(file_path)
