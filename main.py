import argparse
from aws_cost_cli import config, account, cost, printers
import boto3

def main():
    try:
        parser = argparse.ArgumentParser(description="AWS Cost CLI in Python")
        parser.add_argument("--format", choices=["text", "json", "fancy", "slack", "csv"], default="text", help="Output format")
        parser.add_argument("--slack-webhook-url", help="Slack webhook URL for sending cost data to Slack")
        parser.add_argument("--start-date", help="Start date for cost data (format: YYYY-MM-DD)")
        parser.add_argument("--end-date", help="End date for cost data (format: YYYY-MM-DD)")
        parser.add_argument("--time-period", choices=["daily", "monthly", "yearly"], default="daily", help="Time period to aggregate costs by")
        parser.add_argument("--tag-key", help="AWS tag key to break down costs by")
        parser.add_argument("--forecast", type=int, help="Number of days to forecast future costs")
        args = parser.parse_args()


        # Fetch the AWS account alias
        aws_config = config.get_aws_config_from_options_or_file()
        alias_or_id = account.get_account_alias(aws_config)
        print(f"Account Alias/ID: {alias_or_id}")
        
        # Fetch raw cost by service with date filters
        raw_costs = cost.get_raw_cost_by_service(aws_config, args.start_date, args.end_date)

        # Aggregate costs and calculate total
        aggregated_costs = cost.aggregate_cost_by_service(raw_costs)
        total_cost = cost.calculate_total_cost(aggregated_costs)
        print(f"\nTotal Cost: ${total_cost:.2f}")

        # Aggregate costs by chosen time period
        aggregated_costs_by_time = cost.aggregate_cost_by_time_period(raw_costs, args.time_period)

        if args.tag_key:
            cost_by_tag = cost.get_cost_by_tag(aws_config, args.tag_key, args.start_date, args.end_date)
        
        # Print based on the chosen format
        if args.tag_key:
            if args.format == "text":
                printers.text.print_cost_by_tag_as_text(cost_by_tag)
            elif args.format == "json":
                printers.json_printer.print_cost_by_tag_as_json(cost_by_tag)
            elif args.format == "fancy":
                printers.fancy.print_cost_by_tag_as_fancy(cost_by_tag)
            elif args.format == "csv":
                printers.csv_printer.print_cost_as_csv(raw_costs)
            elif args.format == "slack":
                if not args.slack_webhook_url:
                    print("Error: Slack webhook URL is required for Slack format.")
                    return
                printers.slack.send_cost_to_slack(raw_costs, args.slack_webhook_url)
        
        # Fetch cost forecast if forecast option is provided
        if args.forecast:
            forecasted_cost = cost.get_cost_forecast(aws_config, args.forecast)
            print(f"Forecasted Cost for next {args.forecast} days: ${forecasted_cost:.2f}")
            
    except boto3.exceptions.Boto3Error as e:
        print(f"AWS Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()