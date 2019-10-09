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
import sys
import time
import yaml

from collections import ChainMap
from contextlib import contextmanager, suppress

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
    with suppress(Exception):
        with open(config_dir + profile + '.yaml') as config_file:
            config_values = yaml.safe_load(config_file)

    cli_values = {
        key: value for key, value in cli_context.items() if value is not None
    }
    data = ChainMap(cli_values, config_values, defaults)

    if 'port' in data:
        data['url'] = ':'.join([data['host'], str(data['port'])])
    else:
        data['url'] = data['host']

    return data


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
    elif response.status_code == 409:
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
