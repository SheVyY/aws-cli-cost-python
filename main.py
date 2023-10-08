import os
import argparse
from aws_cost_cli import config, account, cost, slack_notifier
from colorama import init, Fore, Style
from prettytable import PrettyTable

def get_timeframes():
    """
    Get predefined timeframes for cost data.

    Returns:
        dict: A dictionary containing timeframe labels as keys and date ranges as values.
    """
    return {
        "Last month": cost.get_last_month(),
        "This month": cost.get_this_month(),
        "Last 7 days": cost.get_last_7_days(),
        "Yesterday": cost.get_yesterday()
    }

def fetch_costs(aws_config, start_date, end_date):
    """
    Fetch raw cost data for a specified date range.

    Args:
        aws_config (dict): AWS configuration.
        start_date (str): Start date for cost data.
        end_date (str): End date for cost data.

    Returns:
        dict: Raw cost data.
    """
    try:
        return cost.get_raw_cost_by_service(aws_config, start_date, end_date)
    except Exception as e:
        print(Fore.RED + f"Error fetching costs: {e}")
        return {}

def display_header(aws_config):
    """
    Display account or organization information in the header.

    Args:
        aws_config (dict): AWS configuration.
    """
    alias_or_id = account.get_account_alias(aws_config)
    if cost.is_cost_from_entire_organization(aws_config):
        master_account_id = account.get_management_account_id(aws_config)
        print(Fore.CYAN + Style.BRIGHT + f"Cost report for the entire organization (Management account ID: {master_account_id})\n")
    else:
        print(Fore.CYAN + Style.BRIGHT + f"Cost report for account: {alias_or_id}\n")

def display_total_costs(aws_config):
    """
    Display total costs for predefined timeframes.

    Args:
        aws_config (dict): AWS configuration.
    """
    timeframes = get_timeframes()
    total_table = PrettyTable()
    total_table.field_names = ["Timeframe", "Total Cost"]
    for label, (start_date, end_date) in timeframes.items():
        raw_costs = fetch_costs(aws_config, start_date, end_date)
        total_cost = sum(cost.aggregate_cost_by_service(raw_costs).values())
        total_table.add_row([label, f"${total_cost:.2f}"])
    print(Fore.GREEN + total_table.get_string())
    return total_table

def display_service_costs(aws_config, timeframes):
    """
    Display service-wise costs for specified timeframes.

    Args:
        aws_config (dict): AWS configuration.
        timeframes (dict): Dictionary containing timeframe labels and date ranges.
    """
    service_costs = cost.get_cost_by_service_for_timeframes(aws_config, timeframes)
    service_table = PrettyTable()
    service_table.field_names = ["Service", "Last month", "This month", "Last 7 days", "Yesterday"]

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
    return service_table

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="AWS Cost CLI in Python")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--summary", action="store_true", help="Display only the total cost summary")
    parser.add_argument("-S", "--slack-token", help="Slack token for the slack message")
    parser.add_argument("-C", "--slack-channel", help="Slack channel to post the message to")
    return parser.parse_args()

def main():
    """
    Main function to run the AWS Cost CLI.
    """
    init(autoreset=True)
    os.system('cls' if os.name == 'nt' else 'clear')

    args = parse_arguments()
    aws_config = config.get_aws_config_from_options_or_file()
    
    display_header(aws_config)
    total_table = display_total_costs(aws_config)

    if not args.summary:
        timeframes = get_timeframes()
        service_table = display_service_costs(aws_config, timeframes)

    if args.slack_token and args.slack_channel:
        cost_report_message = str(total_table) + "\n" + str(service_table)
        slack_notifier.send_slack_notification(args.slack_token, args.slack_channel, cost_report_message)

if __name__ == "__main__":
    main()
