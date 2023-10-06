import csv
import sys

def print_cost_as_csv(cost_data):
    writer = csv.writer(sys.stdout)
    writer.writerow(["Service", "Date", "Cost"])
    for service, costs in cost_data.items():
        for date, amount in costs.items():
            writer.writerow([service, date, f"${amount:.2f}"])
