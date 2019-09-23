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
import logging
import os
import requests
import sys
import yaml

from collections import ChainMap
from contextlib import contextmanager, suppress

from mash_client.mash_client_exceptions import MashClientException

default_config_dir = os.path.expanduser('~/.config/mash_client/')
defaults = {
    'config_dir': default_config_dir,
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

    config_values = {}
    with suppress(Exception):
        with open(config_dir + 'config.yaml') as config_file:
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


def handle_request(config_data, endpoint, job_data=None, action='post'):
    """
    Post request based on endpoint and data.

    If response is successful echo the dictionary status.
    Otherwise raise exception.
    """
    method = getattr(requests, action)

    headers = {}
    if job_data:
        headers = {'content-type': 'application/json'}
        job_data = json.dumps(job_data)

    response = method(
        ''.join([config_data['url'], endpoint]),
        data=job_data,
        headers=headers,
        verify=config_data['verify']
    )

    if response.status_code in (200, 201):
        echo_dict(response.json(), config_data['no_color'])
    elif response.status_code == 400:
        error = '\n'.join(response.json()['errors'].values())
        raise MashClientException(error)
    else:
        response.raise_for_status()


def style_string(message, no_color, fg='yellow'):
    """
    Add color style to string if no_color is False.
    """
    if no_color:
        return message
    else:
        return click.style(message, fg=fg)
