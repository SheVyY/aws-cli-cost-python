import os
import boto3

def get_aws_config_from_options_or_file(profile=None, access_key=None, secret_key=None, session_token=None, region=None):
    # If access_key and secret_key are provided, use them
    if access_key and secret_key:
        return {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'aws_session_token': session_token,
            'region_name': region
        }
    
    # If profile_name is provided, use it
    if profile:
        return {
            'profile_name': profile,
            'region_name': region
        }
    
    # Check for environment variables
    if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY'):
        return {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'aws_session_token': os.environ.get('AWS_SESSION_TOKEN'),
            'region_name': region
        }
    
    # If neither profile nor environment variables are set, use the default profile
    return {
        'profile_name': 'default',
        'region_name': region
    }
