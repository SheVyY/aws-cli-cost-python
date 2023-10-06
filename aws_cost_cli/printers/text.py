def print_cost_as_text(cost_data):
    for service, costs in cost_data.items():
        print(f"\nService: {service}")
        for date, amount in costs.items():
            print(f"  {date}: ${amount:.2f}")

def print_aggregated_cost_as_text(cost_data):
    for date, services in cost_data.items():
        print(f"\nDate: {date}")
        for service, amount in services.items():
            print(f"  {service}: ${amount:.2f}")

def print_cost_by_tag_as_text(tag_data):
    for tag_value, costs in tag_data.items():
        print(f"\nTag Value: {tag_value}")
        for date, amount in costs.items():
            print(f"  {date}: ${amount:.2f}")