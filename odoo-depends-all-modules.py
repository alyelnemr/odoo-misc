import os
import ast


def get_manifest_data(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
        manifest_content = manifest_file.read()
        try:
            manifest_data = ast.literal_eval(manifest_content)
            return manifest_data
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing {manifest_path}: {e}")
            return None


def build_dependency_graph(odoo_addons_path):
    dependency_graph = {}

    for root, dirs, files in os.walk(odoo_addons_path):
        if '__manifest__.py' in files:
            manifest_path = os.path.join(root, '__manifest__.py')
            manifest_data = get_manifest_data(manifest_path)
            if manifest_data:
                module_name = manifest_data.get('name', os.path.basename(root))
                dependencies = manifest_data.get('depends', [])
                dependency_graph[module_name] = dependencies

    return dependency_graph


def print_dependency_hierarchy(dependency_graph, module_name, indent=0, visited=None):
    if visited is None:
        visited = set()

    if module_name in visited:
        print(" " * indent + f"{module_name} (circular dependency)")
        return

    visited.add(module_name)
    print(" " * indent + module_name)

    for dependency in dependency_graph.get(module_name, []):
        print_dependency_hierarchy(dependency_graph, dependency, indent + 2, visited.copy())


# Define the path to your Odoo addons directory
odoo_addons_path = 'odoo\\addons'
dependency_graph = build_dependency_graph(odoo_addons_path)

print("Dependency hierarchy for all Odoo modules:")
for module in dependency_graph:
    print_dependency_hierarchy(dependency_graph, module)
