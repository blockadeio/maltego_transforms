#! /usr/bin/env python

"""Maltego interface for Blockade."""
import json
import requests
from flask import Flask
from common.response import error_response
from common.response import maltego_response
from common.const import MALTEGO_PHRASE
from bxforms.common.utilities import safe_symbols
from bxforms import load_maltego

app = Flask(__name__)


def post_indicators(kwargs):
    """Send indicators to the blockade cloud node."""
    headers = {'Content-Type': 'application/json'}
    indicator = kwargs.get('INDICATOR')
    data = {'indicators': [indicator], 'email': kwargs.get('CLOUD_USER'),
            'api_key': kwargs.get('CLOUD_KEY')}
    url = "{}/admin/add-indicators".format(kwargs.get('CLOUD_HOST'))
    try:
        args = {'url': url, 'headers': headers, 'data': json.dumps(data),
                'timeout': 120}
        response = requests.post(**args)
    except Exception, e:
        message = "Error Posting: %s" % str(e)
        return {'success': False, 'error': message, 'writeCount': 0}
    if response.status_code not in range(200, 299):
        message = "Error: {}".format(response.content)
        return {'success': False, 'error': message, 'writeCount': 0,
                'http_code': response.status_code}
    loaded = json.loads(response.content)
    return loaded


@app.route('/add_indicator', method="ANY")
@load_maltego(debug=False)
def add_indicator(trx, context):
    """Add an indicator to a cloud node."""
    username = context.getTransformSetting('username')
    api_key = context.getTransformSetting('api_key')
    host = context.getTransformSetting('cloud_host')
    indicator = context.getTransformSetting('indicator')

    # Make the request
    params = {'CLOUD_HOST': host, 'CLOUD_USER': username,
              'CLOUD_KEY': api_key, 'INDICATOR': indicator}
    response = post_indicators(**params)
    if not response['success']:
        return error_response(trx, response)
    trx.addEntity(MALTEGO_PHRASE, safe_symbols(response['message']))
    return maltego_response(trx)
