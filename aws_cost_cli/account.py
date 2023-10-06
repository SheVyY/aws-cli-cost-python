import boto3
from .config import get_aws_config_from_options_or_file
from colorama import Fore

def get_account_alias(aws_config):
    iam = boto3.client('iam', **aws_config)
    
    # Try to get account alias
    aliases = iam.list_account_aliases()['AccountAliases']
    if aliases:
        return aliases[0]
    
    # If alias not found, return account ID
    sts = boto3.client('sts', **aws_config)
    account_id = sts.get_caller_identity()['Account']
    return account_id

def get_management_account_id(aws_config):
    client = boto3.client('organizations', **aws_config)
    try:
        response = client.describe_organization()
        return response['Organization']['MasterAccountId']
    except Exception as e:
        print(Fore.RED + f"Error fetching management account ID: {e}")
        return None


