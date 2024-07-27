import os
import ast

def parse_manifest(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
        manifest_content = manifest_file.read()
        try:
            return ast.literal_eval(manifest_content)
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing {manifest_path}: {e}")
            return None

def get_module_dependencies(module_name, odoo_addons_path):
    module_path = os.path.join(odoo_addons_path, module_name)
    manifest_path = os.path.join(module_path, '__manifest__.py')
    if os.path.exists(manifest_path):
        manifest_data = parse_manifest(manifest_path)
        if manifest_data:
            return manifest_data.get('depends', [])
    return []

def find_all_dependencies(module_name, odoo_addons_path, all_dependencies=None):
    if all_dependencies is None:
        all_dependencies = set()
    direct_dependencies = get_module_dependencies(module_name, odoo_addons_path)
    for dep in direct_dependencies:
        if dep not in all_dependencies:
            all_dependencies.add(dep)
            find_all_dependencies(dep, odoo_addons_path, all_dependencies)
    return all_dependencies

# Define the path to your Odoo addons directory
odoo_addons_path = 'D:\\ACS\\MasterData'

# Start with the main module
main_module = 'eit_freight_MasterData'
all_dependencies = find_all_dependencies(main_module, odoo_addons_path)

# Check if 'project' is in the dependencies
project_in_dependencies = 'appointment' in all_dependencies

print(f"All dependencies of {main_module}:")
print(all_dependencies)
print(f"\nDoes {main_module} depend on 'project'?: {'Yes' if project_in_dependencies else 'No'}")
