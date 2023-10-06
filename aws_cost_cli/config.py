import boto3

def get_aws_config_from_options_or_file(profile='default', access_key=None, secret_key=None, session_token=None, region=None):
    if access_key and secret_key:
        return {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'aws_session_token': session_token,
            'region_name': region
        }
    
    # If not provided, boto3 will automatically load from standard locations
    return {
        'profile_name': profile,
        'region_name': region
    }
