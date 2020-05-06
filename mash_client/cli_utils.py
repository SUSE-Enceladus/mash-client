# -*- coding: utf-8 -*-

"""Utility methods for mash client cli endpoints."""

# Copyright (c) 2019 SUSE LLC. All rights reserved.
#
# This file is part of mash_client. mash_client provides a command line
# utility for interfacing with a MASH server.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import click
import json
import jwt
import logging
import os
import requests
import socket
import sys
import time
import yaml

from collections import ChainMap
from contextlib import contextmanager, suppress
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from mash_client.mash_client_exceptions import MashClientException

default_config_dir = os.path.expanduser('~/.config/mash_client/')
default_profile = 'default'
defaults = {
    'config_dir': default_config_dir,
    'profile': default_profile,
    'host': 'http://127.0.0.1',
    'log_level': logging.INFO,
    'no_color': False,
    'verify': True
}
EC2_PARTITIONS = ('aws', 'aws-cn', 'aws-us-gov')


def echo_dict(data, no_color):
    """
    Echoes a dictionary pretty-print style to terminal.
    """
    echo_style(json.dumps(data, indent=4), no_color)


def echo_style(message, no_color, fg='yellow'):
    """
    Echo stylized output to terminal depending on no_color.
    """
    if no_color:
        click.echo(message)
    else:
        click.secho(message, fg=fg)


def get_config(cli_context):
    """
    Process mash client config.

    Use ChainMap to build config values based on
    command line args, config and defaults.
    """
    config_dir = cli_context['config_dir'] or default_config_dir
    profile = cli_context['profile'] or default_profile

    config_values = {}
    config_file_path = os.path.join(config_dir, profile + '.yaml')

    try:
        with open(config_file_path) as config_file:
            config_values = yaml.safe_load(config_file)
    except FileNotFoundError:
        echo_style(
            'Config file: {config_file_path} not found. Using default '
            'configuration values. See `mash config setup` for info on '
            'setting up a config file for this profile.'.format(
                config_file_path=config_file_path
            ),
            no_color=True
        )

    cli_values = {
        key: value for key, value in cli_context.items() if value is not None
    }
    data = ChainMap(cli_values, config_values, defaults)

    if 'port' in data:
        data['url'] = ':'.join([data['host'], str(data['port'])])
    else:
        data['url'] = data['host']

    return data


def update_config(cli_context, key, value):
    """
    Update a key in the current config profile.
    """
    config_dir = cli_context['config_dir'] or default_config_dir
    profile = cli_context['profile'] or default_profile
    config_path = config_dir + profile + '.yaml'

    config_values = {}
    with suppress(Exception):
        with open(config_path) as config_file:
            config_values = yaml.safe_load(config_file)

    config_values[key] = value

    with open(config_path, 'w') as config_file:
        yaml.dump(config_values, config_file, default_flow_style=False)


@contextmanager
def handle_errors(log_level, no_color):
    """
    Context manager to handle exceptions and echo error msg.
    """
    try:
        yield
    except Exception as error:
        if log_level == logging.DEBUG:
            raise

        echo_style(
            "{}: {}".format(type(error).__name__, error),
            no_color,
            fg='red'
        )
        sys.exit(1)


def handle_request(
    config_data,
    endpoint,
    job_data=None,
    action='post',
    token=None
):
    """
    Post request based on endpoint and data.

    If response is successful return the json data.
    Otherwise raise exception.
    """
    method = getattr(requests, action)

    headers = {}
    if job_data:
        headers = {'content-type': 'application/json'}
        job_data = json.dumps(job_data)

    if token:
        headers['authorization'] = 'Bearer {token}'.format(token=token)

    try:
        response = method(
            ''.join([config_data['url'], endpoint]),
            data=job_data,
            headers=headers,
            verify=config_data['verify']
        )
    except requests.ConnectionError:
        raise MashClientException(
            'Failed to establish connection with MASH server at: '
            '{url}'.format(url=config_data['url'])
        )

    if response.status_code in (200, 201):
        return response.json()
    elif response.status_code == 400:
        try:
            error = '\n'.join(response.json()['errors'].values())
        except KeyError:
            error = response.json()['msg']

        raise MashClientException(error)
    elif response.status_code == 401:
        raise MashClientException(
            response.json()['msg'] + '. Please login again.'
        )
    elif response.status_code == 404:
        try:
            msg = response.json()['msg']
        except (json.decoder.JSONDecodeError, KeyError):
            msg = 'The requested URL was not found on the server:' \
                  ' {url}'.format(
                      url=''.join([config_data['url'], endpoint])
                  )

        raise MashClientException(msg)
    elif response.status_code in (403, 409):
        raise MashClientException(response.json()['msg'])
    else:
        response.raise_for_status()


def handle_request_with_token(
    config_data,
    endpoint,
    job_data=None,
    action='post'
):
    """
    Submit request to API with access token.

    If access token is past expiration date attempt to refresh token.
    """
    tokens_file = get_tokens_file(
        config_data['config_dir'],
        config_data['profile']
    )
    tokens = get_tokens_from_file(tokens_file)

    if 'access_token' not in tokens:
        refresh_token(config_data)
    else:
        access_token = jwt.decode(tokens['access_token'], verify=False)
        now = int(time.time())

        if access_token.get('exp') and now >= access_token['exp']:
            refresh_token(config_data)

    tokens = get_tokens_from_file(tokens_file)

    result = handle_request(
        config_data,
        endpoint,
        job_data=job_data,
        action=action,
        token=tokens['access_token']
    )

    return result


def refresh_token(config_data):
    tokens_file = get_tokens_file(
        config_data['config_dir'],
        config_data['profile']
    )
    tokens = get_tokens_from_file(tokens_file)

    if 'refresh_token' not in tokens:
        echo_style(
            'No refresh token, please login (mash auth login).',
            config_data['no_color'],
            fg='red'
        )
        sys.exit(1)

    result = handle_request(
        config_data,
        '/auth/token/refresh',
        action='post',
        token=tokens['refresh_token']
    )

    tokens['access_token'] = result['access_token']

    tokens_file = get_tokens_file(
        config_data['config_dir'],
        config_data['profile']
    )

    save_tokens_to_file(tokens_file, tokens)


def get_tokens_file(config_dir, profile):
    return ''.join([config_dir, profile, '_tokens.json'])


def get_tokens_from_file(tokens_path):
    try:
        with open(tokens_path) as tokens_file:
            tokens = json.load(tokens_file)
    except FileNotFoundError:
        raise MashClientException(
            'No tokens available, please login (mash auth login).'
        )

    return tokens


def save_tokens_to_file(tokens_path, tokens):
    with open(tokens_path, 'w') as tokens_file:
        json.dump(tokens, tokens_file, indent=2)
        tokens_file.write('\n')


def style_string(message, no_color, fg='yellow'):
    """
    Add color style to string if no_color is False.
    """
    if no_color:
        return message
    else:
        return click.style(message, fg=fg)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def additional_regions_repl():
    regions = []

    while True:
        if click.confirm('Add an additional region?'):
            name = click.prompt('Enter the region name', type=str)
            helper_image = click.prompt(
                'Enter the helper image id',
                type=str
            )

            regions.append({
                'name': name,
                'helper_image': helper_image
            })
        else:
            break

    return regions


def get_free_port(ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_addr = socket.gethostbyname('localhost')
    for port in ports:
        try:
            sock.bind((local_addr, port))
            sock.close()
            return port
        except Exception:
            pass
    return None


class CodeReceivedException(BaseException):
    def __init__(self, code):
        self.code = code


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        params = parse_qs(urlparse(self.path).query)
        if not params.get('code'):
            bg_color = 'FF8E77'
            msg = 'ERROR: No authentication code received.'

            if params.get('error_description', []):
                msg += ' '
                msg += params['error_description'][0]
        else:
            msg = 'Authentication code received.'
            bg_color = '7AD4AA'

        msg += ' You may close this tab.'
        exception = CodeReceivedException(params.get('code', [None])[0])
        self.wfile.write(bytes(
            '<html><body><div style="background-color:#{};width:50%;'
            'margin:auto;padding:10px;border-radius:10px;text-align:center;'
            'border-color:#0C322C;border-width:2px;border-style:solid;">'
            '<h3>{}</h3></div></body></html>'.format(bg_color, msg),
            'utf-8'
        ))
        raise exception

    def log_message(self, *args):
        # supress logging of requests
        pass


def get_oauth2_code(port):
    httpd = HTTPServer(('localhost', port), RequestHandler)
    code = None
    try:
        httpd.serve_forever()
    except CodeReceivedException as e:
        code = e.code
    finally:
        httpd.shutdown()
        httpd.server_close()
    return code


def get_annotated_property(key, value, required):
    annotated_keys = (
        'description', 'type', 'example', 'enum', 'format', 'pattern'
    )
    annotated_value = {
        key: value[key] for key in value if key in annotated_keys
    }

    if key in required:
        annotated_value['required'] = True

    if value['type'] == 'array':
        nested_type = value['items']['type']
        annotated_value['type'] = 'list of {nested_type}s'.format(
            nested_type=nested_type
        )

        if nested_type == 'object':
            properties = {}

            for obj_key, obj_value in value['items']['properties'].items():
                properties[obj_key] = get_annotated_property(
                    obj_key,
                    obj_value,
                    value['items'].get('required', tuple())
                )

            annotated_value['properties'] = properties

    return annotated_value


def get_job_schema_by_cloud(context, output_style, cloud):
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request(
            config_data,
            '/jobs/{cloud}/'.format(cloud=cloud),
            action='get'
        )

    if output_style == 'json':
        json_result = {}
        for key, value in result['properties'].items():
            json_result[key] = '' if value['type'] == 'string' else None

        result = json_result
    elif output_style == 'annotated':
        annotated_result = {}
        for key, value in result['properties'].items():
            annotated_result[key] = get_annotated_property(
                key,
                value,
                result.get('required', tuple())
            )

        result = annotated_result

    echo_dict(result, config_data['no_color'])
