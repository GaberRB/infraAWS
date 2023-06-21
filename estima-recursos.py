import boto3
import json


def get_service_code(service_name):

    return  'Amazon' + service_name


def get_estimated_cost(resource):
    pricing_client = boto3.client('pricing', region_name='us-east-1')
    service_code = get_service_code(resource)

    if not service_code:
        return None
    print(service_code)
    response = pricing_client.get_products(
        ServiceCode=service_code,
        Filters=[
            {
                'Type': 'TERM_MATCH',
                'Field': 'location',
                'Value': 'US East (N. Virginia)'
            }
        ],
        MaxResults=100
    )

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

with open('resources.txt', 'r') as file:
    resources = file.read().splitlines()

total = 0

for resource in resources:
    estimated_cost = get_estimated_cost(resource)
    total = total + float(estimated_cost)
    with open('resources_cost.txt', 'a') as file:
        file.write(f'\n{resource}: {estimated_cost} ')

with open('resources_cost.txt', 'a') as file:
    file.write(f'\nTotal: {str(total)} P/dia')

