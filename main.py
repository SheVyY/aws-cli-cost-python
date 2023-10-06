import argparse
import os
from aws_cost_cli import config, account, cost
from colorama import init, Fore
from prettytable import PrettyTable

def main():
    try:
        parser = argparse.ArgumentParser(description="AWS Cost CLI in Python")
        parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
        args = parser.parse_args()
        
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Initialize colorama
        init(autoreset=True)

        # Fetch the AWS account alias
        aws_config = config.get_aws_config_from_options_or_file()
        alias_or_id = account.get_account_alias(aws_config)
        print(f"Cost report for account: {alias_or_id}\n")

        timeframes = {
            "Last month": cost.get_last_month(),
            "This month": cost.get_this_month(),
            "Last 7 days": cost.get_last_7_days(),
            "Yesterday": cost.get_yesterday()
        }

        # Display total costs using PrettyTable
        total_table = PrettyTable()
        total_table.field_names = ["Timeframe", "Total Cost"]
        for label, (start_date, end_date) in timeframes.items():
            raw_costs = cost.get_raw_cost_by_service(aws_config, start_date, end_date)
            total_cost = sum(cost.aggregate_cost_by_service(raw_costs).values())
            total_table.add_row([label, f"${total_cost:.2f}"])
        print(total_table)

        # Display service-wise breakdown using PrettyTable
        service_costs = cost.get_cost_by_service_for_timeframes(aws_config, timeframes)
        service_table = PrettyTable()
        service_table.field_names = ["Service", "Last month", "This month", "Last 7 days", "Yesterday"]
        for service, costs in service_costs.items():
            last_month_cost = costs.get('Last month', 0.00)
            this_month_cost = costs.get('This month', 0.00)
            last_7_days_cost = costs.get('Last 7 days', 0.00)
            yesterday_cost = costs.get('Yesterday', 0.00)
            
            service_table.add_row([
                service,
                f"${last_month_cost:.2f}",
                f"${this_month_cost:.2f}",
                f"${last_7_days_cost:.2f}",
                f"${yesterday_cost:.2f}"
            ])
        print(service_table)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
