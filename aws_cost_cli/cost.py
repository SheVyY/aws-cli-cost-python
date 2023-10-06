import boto3
import datetime

def is_cost_from_entire_organization(aws_config):
    cost_explorer = boto3.client('ce', **aws_config)
    
    # Use a sample date range to check the linkedAccount dimension
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=1)
    
    pricing_data = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'LINKED_ACCOUNT'
            }
        ]
    )
    
    # If there are multiple linked accounts, it means the costs are from the entire organization
    return len(pricing_data['ResultsByTime'][0]['Groups']) > 1

def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday, today

def get_last_month():
    end_date = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    start_date = end_date.replace(day=1)
    return start_date, end_date

def get_this_month():
    start_date = datetime.date.today().replace(day=1)
    end_date = datetime.date.today()
    return start_date, end_date

def get_last_7_days():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    return start_date, end_date

def get_raw_cost_by_service(aws_config, start_date=None, end_date=None):
    cost_explorer = boto3.client('ce', **aws_config)
    
    if not end_date:
        end_date = datetime.date.today()
    if not start_date:
        start_date = end_date - datetime.timedelta(days=30)  # Default to 30 days back
    
    pricing_data = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    
    cost_by_service = {}
    for day in pricing_data['ResultsByTime']:
        for group in day['Groups']:
            service_name = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            cost_date = day['TimePeriod']['End']
            
            if service_name not in cost_by_service:
                cost_by_service[service_name] = {}
            cost_by_service[service_name][cost_date] = cost
    
    return cost_by_service



def aggregate_cost_by_service(raw_cost_data):
    aggregated_costs = {}
    for service, costs in raw_cost_data.items():
        total_cost = sum(costs.values())
        aggregated_costs[service] = total_cost
    return aggregated_costs

def get_cost_by_service_for_timeframes(aws_config, timeframes):
    service_costs = {}

    for timeframe, (start_date, end_date) in timeframes.items():
        raw_costs = get_raw_cost_by_service(aws_config, start_date, end_date)
        aggregated_costs = aggregate_cost_by_service(raw_costs)

        for service, cost in aggregated_costs.items():
            if service not in service_costs:
                service_costs[service] = {}
            service_costs[service][timeframe] = cost

    return service_costs