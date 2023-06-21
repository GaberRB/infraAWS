import ruamel.yaml
import json
import os

template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "infraAWS", "infra", "template.yml"))
output_file = "resource_info.json"

def extract_resource_info(resources):
    data = []
    for resource_id, resource in resources.items():
        resource_type = resource.get("Type")
        resource_type.split('AWS::')[1].strip().split(':')[0].strip()
        if resource_type.startswith("AWS::RDS"):
            db_instance_class = resource.get("Properties", {}).get("DBInstanceClass")
            if db_instance_class:
                data.append({"ResourceType": resource_type, "DBInstanceClass": db_instance_class})
        elif resource_type.startswith("AWS::EC2"):
            instance_type = resource.get("Properties", {}).get("InstanceType")
            if instance_type:
                data.append({"ResourceType": resource_type, "InstanceType": instance_type})
        else:
            data.append({"ResourceType": resource_type, "InstanceType": None})
    return data

def save_resource_info(resource_info):
    with open(output_file, "w") as file:
        json.dump(resource_info, file, indent=4)

yaml = ruamel.yaml.YAML()
with open(template_path, "r") as file:
    parsed_template = yaml.load(file)

resources = parsed_template.get("Resources", {})
resource_info = extract_resource_info(resources)
save_resource_info(resource_info)
