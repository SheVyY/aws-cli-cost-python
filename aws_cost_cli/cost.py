import boto3
import datetime
from .config import get_aws_config_from_options_or_file

def get_raw_cost_by_service(aws_config):
    cost_explorer = boto3.client('ce', **aws_config)
    
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=65)
    
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

def calculate_total_cost(aggregated_cost_data):
    return sum(aggregated_cost_data.values())

def get_raw_cost_by_service(aws_config, start_date=None, end_date=None):
    cost_explorer = boto3.client('ce', **aws_config)
    
    if not end_date:
        end_date = datetime.date.today() - datetime.timedelta(days=1)
    if not start_date:
        start_date = end_date - datetime.timedelta(days=65)

def aggregate_cost_by_time_period(raw_cost_data, time_period="daily"):
    aggregated_costs = {}
    
    for service, costs in raw_cost_data.items():
        for date, amount in costs.items():
            if time_period == "monthly":
                date = date[:7]  # Extract YYYY-MM format
            elif time_period == "yearly":
                date = date[:4]  # Extract YYYY format
            
            if date not in aggregated_costs:
                aggregated_costs[date] = {}
            if service not in aggregated_costs[date]:
                aggregated_costs[date][service] = 0
            aggregated_costs[date][service] += amount

    return aggregated_costs

def get_cost_by_tag(aws_config, tag_key, start_date=None, end_date=None):
    cost_explorer = boto3.client('ce', **aws_config)
    
    if not end_date:
        end_date = datetime.date.today() - datetime.timedelta(days=1)
    if not start_date:
        start_date = end_date - datetime.timedelta(days=65)
    
    pricing_data = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'TAG',
                'Key': tag_key
            }
        ]
    )
    
    cost_by_tag = {}
    for day in pricing_data['ResultsByTime']:
        for group in day['Groups']:
            tag_value = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            cost_date = day['TimePeriod']['End']
            
            if tag_value not in cost_by_tag:
                cost_by_tag[tag_value] = {}
            cost_by_tag[tag_value][cost_date] = cost
    
    return cost_by_tag


def get_cost_forecast(aws_config, forecast_days=30):
    cost_explorer = boto3.client('ce', **aws_config)
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)  # Use a year of historical data for forecasting
    
    forecast_data = cost_explorer.get_cost_forecast(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': (end_date + datetime.timedelta(days=forecast_days)).strftime('%Y-%m-%d')
        },
        Metric='UNBLENDED_COST',
        Granularity='DAILY'
    )
    
    return forecast_data['Total']['Amount']