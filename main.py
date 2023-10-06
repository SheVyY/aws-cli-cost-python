import os
import argparse
from aws_cost_cli import config, account, cost
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable
from aws_cost_cli import slack_notifier

def main():
    # Initialize colorama
    init(autoreset=True)

    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser(description="AWS Cost CLI in Python")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--summary", action="store_true", help="Display only the total cost summary")
    parser.add_argument("-S", "--slack-token", help="Slack token for the slack message")
    parser.add_argument("-C", "--slack-channel", help="Slack channel to post the message to")
    args = parser.parse_args()

    # Fetch the AWS account alias
    aws_config = config.get_aws_config_from_options_or_file()
    alias_or_id = account.get_account_alias(aws_config)

    # Check if the costs are from the entire organization
    if cost.is_cost_from_entire_organization(aws_config):
        master_account_id = account.get_management_account_id(aws_config)
        print(Fore.CYAN + Style.BRIGHT + f"Cost report for the entire organization (Management account ID: {master_account_id})\n")
    else:
        print(Fore.CYAN + Style.BRIGHT + f"Cost report for account: {alias_or_id}\n")

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
    print(Fore.GREEN + total_table.get_string())

    # If --summary flag is not provided, display service-wise breakdown
    if not args.summary:
        service_costs = cost.get_cost_by_service_for_timeframes(aws_config, timeframes)
        service_table = PrettyTable()
        service_table.field_names = ["Service", "Last month", "This month", "Last 7 days", "Yesterday"]

        # Ensure 'Tax' is the first row
        if 'Tax' in service_costs:
            tax_costs = service_costs.pop('Tax')
            service_table.add_row([
                Fore.BLUE + "Tax" + Style.RESET_ALL,
                f"${tax_costs.get('Last month', 0.00):.2f}",
                f"${tax_costs.get('This month', 0.00):.2f}",
                f"${tax_costs.get('Last 7 days', 0.00):.2f}",
                f"${tax_costs.get('Yesterday', 0.00):.2f}"
            ])

        for service, costs in service_costs.items():
            last_month_cost = costs.get('Last month', 0.00)
            this_month_cost = costs.get('This month', 0.00)
            last_7_days_cost = costs.get('Last 7 days', 0.00)
            yesterday_cost = costs.get('Yesterday', 0.00)
            
            service_table.add_row([
                Fore.BLUE + service + Style.RESET_ALL,
                f"${last_month_cost:.2f}",
                f"${this_month_cost:.2f}",
                f"${last_7_days_cost:.2f}",
                f"${yesterday_cost:.2f}"
            ])

        print(service_table)
    
    # Check if Slack arguments are provided
    if args.slack_token and args.slack_channel:
        # Convert the PrettyTable object to a string for the Slack message
        cost_report_message = str(summary_table) + "\n" + str(service_table)
        slack_notifier.send_slack_notification(args.slack_token, args.slack_channel, cost_report_message)

if __name__ == "__main__":
    main()
