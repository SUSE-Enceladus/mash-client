# -*- coding: utf-8 -*-

"""mash client CLI config file endpoints using click library."""

# Copyright (c) 2020 SUSE LLC. All rights reserved.
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
import logging
import os
import yaml

from mash_client.cli_utils import (
    default_config_dir,
    get_config,
    echo_dict,
    handle_errors
)


@click.group()
def config():
    """
    Provides commands to setup and view client configuration file.
    """


@click.command(name='setup')
@click.option(
    '--config-dir',
    type=click.STRING,
    default=default_config_dir,
    show_default=True,
    prompt='Enter Mash client config directory',
    help='Mash client config directory to use. It is recommended that this'
         ' is left empty and to use the default directory'
         ' [~/.config/mash_client/]. If you use a custom configuration'
         ' directory it is required in every command using'
         ' `-C/--config-dir` option.'
)
@click.option(
    '--profile',
    type=click.STRING,
    default='default',
    show_default=True,
    prompt='Enter profile',
    help='The profile for config file. The config file will'
         ' be saved as {profile}.yaml in the ~/.config/mash_client/'
         ' directory.'
)
@click.option(
    '--email',
    type=click.STRING,
    prompt='Enter email address',
    default='',
    help='The email address for your Mash user. This can be left blank'
         ' if you are using OIDC login.'
)
@click.option(
    '--host',
    type=click.STRING,
    default='http://127.0.0.1',
    show_default=True,
    prompt='Enter Mash server host',
    help='The host URI for the Mash server.'
)
@click.option(
    '--port',
    type=click.STRING,
    show_default=True,
    default='',
    prompt='Enter Mash server port',
    help='The port for the Mash server API. This is optional'
         ' and can be left blank if the server uses a default'
         ' port such as 80 for http and 443 for https.'
)
@click.option(
    '--log-level',
    type=click.INT,
    default=logging.INFO,
    show_default=True,
    prompt='Enter log level',
    help='The Python log level integer see Python docs for more info:'
         ' https://docs.python.org/3/library/logging.html#levels.'
)
@click.option(
    '--color',
    is_flag=True,
    default=True,
    show_default=True,
    prompt='Style output with ANSI color?',
    help='If Y command line output may be styled with ANSI color.'
)
@click.option(
    '--verify',
    is_flag=True,
    default=True,
    show_default=True,
    prompt='Verify SSL Cert?',
    help='Whether to verify SSL Certificate. If True You can optionally'
         ' provide the path to a CA_BUNDLE file.'
)
def setup_config(
    config_dir, profile, email, host, port, log_level, color, verify
):
    """
    Create a configuration file for the mash command line tool

    For details see man 5 mash_client.conf
    """
    no_color = not color  # Value is stored as no_color in config file

    if verify:
        path_to_cert = click.prompt(
            'Enter path to cert (optional)',
            type=str,
            default='',
            show_default=True
        )
        if path_to_cert:
            verify = path_to_cert

    config_values = {
        'host': host,
        'log_level': log_level,
        'no_color': no_color,
        'verify': verify
    }

    if email:
        config_values['email'] = email

    if port:
        config_values['port'] = port

    config_dir = os.path.expanduser(config_dir)
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    config_file_path = os.path.join(config_dir, profile + '.yaml')

    with handle_errors(log_level, no_color):
        with open(config_file_path, 'w') as config_file:
            yaml.dump(config_values, config_file, default_flow_style=False)

    echo_dict(config_values, no_color)


@click.command(name='show')
@click.pass_context
def show_config(context):
    """
    Prints a dictionary from the client config file based on profile.
    """
    config_data = get_config(context.obj)
    config_file_path = os.path.join(
        config_data['config_dir'],
        config_data['profile'] + '.yaml'
    )

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(config_file_path, 'r') as config_file:
            config_values = yaml.safe_load(config_file)

    echo_dict(config_values, config_data['no_color'])


config.add_command(setup_config)
config.add_command(show_config)
