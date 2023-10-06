import json

def print_cost_as_json(cost_data):
    print(json.dumps(cost_data, indent=4))

def print_aggregated_cost_as_json(cost_data):
    print(json.dumps(cost_data, indent=4))

def print_cost_by_tag_as_json(tag_data):
    print(json.dumps(tag_data, indent=4))