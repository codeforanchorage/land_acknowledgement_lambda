import os
import json

from chalicelib.errors import APIError, LocationNotFound, ConfigurationError
from chalicelib.http import session

# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "MAPBOX_TOKEN"
    region_name = "us-west-2"

    session = boto3.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret.get('MAPBOX_TOKEN')
            


API_BASE = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'

MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN') or get_secret()

if MAPBOX_TOKEN is None:
    raise ConfigurationError("The env MAPBOX_TOKEN is missing from the environment.")

'''
Things that can go wrong with user input:
Blank input — check before querrying
Too short - can a query shorted than three characters ever be meaningful
Too broad - 'Canada' can't provide a meaningful result
'''


def geolocate(raw_str):
    query = {
        'access_token': MAPBOX_TOKEN,
        'type': 'place'
    }
    url = API_BASE + raw_str + '.json'
    resp = session.request('GET', url, fields=query)
    
    if resp.status == 404:
        raise LocationNotFound
    elif resp.status != 200:
        raise APIError(resp.reason)

    data = json.loads(resp.data.decode('utf-8'))
    return location_from_collection(data)


def location_from_collection(json_data):
    '''
    Returns the best feature from the collection of features
    returned by api. Best is determined by sorting by relevance then type in
    a way that favors places over less desireable results like POI.
    Raises LocationNotFound if the API returns an empty collection.
    '''

    priorities = {
        'place': 10,
        'postcode': 10,
        'locality': 9,
        'address': 8,
        'region': 7,
        'country': 6,
        'district': 5,
        'neighborhood': 5,
        'poi': 4
    }

    features = json_data['features']
    if len(features) == 0:
        raise LocationNotFound("Not found")
    return max(features, key=lambda f: (f['relevance'], priorities.get(f['place_type'][0], 0)))
