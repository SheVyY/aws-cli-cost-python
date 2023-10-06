from prettytable import PrettyTable

def print_cost_as_fancy(cost_data):
    table = PrettyTable()
    table.field_names = ["Service", "Date", "Cost"]
    for service, costs in cost_data.items():
        for date, amount in costs.items():
            table.add_row([service, date, f"${amount:.2f}"])
    print(table)

def print_aggregated_cost_as_fancy(cost_data):
    table = PrettyTable()
    table.field_names = ["Date", "Service", "Cost"]
    for date, services in cost_data.items():
        for service, amount in services.items():
            table.add_row([date, service, f"${amount:.2f}"])
    print(table)
    
def print_cost_by_tag_as_fancy(tag_data):
    table = PrettyTable()
    table.field_names = ["Tag Value", "Date", "Cost"]
    for tag_value, costs in tag_data.items():
        for date, amount in costs.items():
            table.add_row([tag_value, date, f"${amount:.2f}"])
    print(table)