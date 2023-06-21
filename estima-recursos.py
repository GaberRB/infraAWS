import boto3
import json


def get_service_code(service_name):

    return 'Amazon' + service_name


def get_estimated_cost(resource):
    pricing_client = boto3.client('pricing', region_name='us-east-1')

    resource_type = resource.get('ResourceType')
    service_code = get_service_code(resource_type.split('AWS::')[1].strip().split(':')[0].strip())
    if not service_code:
        return None
    if resource_type.startswith("AWS::EC2"):
        instance_type = resource.get("InstanceType")
        FLT = '[{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},' \
              '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}}]'

        f = FLT.format(t=instance_type, r='US East (N. Virginia)')
        response = pricing_client.get_products(ServiceCode=service_code, Filters=json.loads(f))
    elif resource_type.startswith("AWS::RDS"):
        service_code = get_service_code(resource_type.split('AWS::')[1].strip().split(':')[0].strip())
        db_instance_class = resource.get("DBInstanceClass")
        FLT = '[{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},' \
              '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}}]'

        f = FLT.format(t=db_instance_class, r='US East (N. Virginia)')
        response = pricing_client.get_products(ServiceCode=service_code, Filters=json.loads(f))
    else:
        service_code = get_service_code(resource_type.split('AWS::')[1].strip().split(':')[0].strip())
        FLT = '[{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}}]'

        f = FLT.format(r='US East (N. Virginia)')
        response = pricing_client.get_products(ServiceCode=service_code, Filters=json.loads(f))


    if 'PriceList' in response:
        try:
            price_list = response['PriceList'][0]
            price_list_json = json.loads(price_list)
            terms = price_list_json['terms']
            on_demand_terms = terms['OnDemand']

            for term_key in on_demand_terms:
                term = on_demand_terms[term_key]
                price_dimensions = term['priceDimensions']
                for price_dimension_key in price_dimensions:
                    price_dimension = price_dimensions[price_dimension_key]
                    price_per_unit = price_dimension['pricePerUnit']['USD']
                    return price_per_unit
        except Exception as e:
            print(f"Erro ao buscar o preco do {resource}: ex: {e}")
            return None

    return None


def load_resource_info():
    with open("resource_info.json", "r") as file:
        resource_info = json.load(file)
    return resource_info


total = 0

for resource in load_resource_info():
    estimated_cost = get_estimated_cost(resource)
    total = total + float(estimated_cost)
    with open('resources_cost.txt', 'a') as file:
        file.write(f'\n{resource}: {estimated_cost} ')

with open('resources_cost.txt', 'a') as file:
    file.write(f'\nTotal: {str(total)} P/dia')


