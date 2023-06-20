import ruamel.yaml
import re
import os

template_path = os.path.join(os.getcwd(), '/infra/template.yml')

with open(template_path, 'r') as file:
    template = file.read()

def sub_variavel(match)
    value = match.group(1)
    return 'value'

pattern = r'\$\{([^]+)\}'

def replace_variavel(template):
    while True:
        trocar_template, num_subs = re.subn(pattern, sub_variavel, template)
        if num_subs == 0:
            break
        template = trocar_template
    return trocar_template

yaml = ruamel.yaml.YAML()
parsed_template = yaml.load(replace_variavel(template))

resources = parsed_template.get('Resources', {})
resources_types = [resource['Type'].split('AWS::')[1].strip().split(':')[0].strip() for resource in resources.values()]

with open('resorces.txt', 'w') as file:
    file.write('\n'.join(resources_types))