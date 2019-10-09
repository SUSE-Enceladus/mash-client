# -*- coding: utf-8 -*-

"""mash client CLI auth endpoints using click library."""

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
import sys

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request,
    echo_style,
    save_tokens_to_file,
    get_tokens_file,
    get_tokens_from_file
)
from mash_client.cli.auth.token import token


@click.group()
def auth():
    """
    Submit authentication requests.
    """


@click.command()
@click.option(
    '--username',
    type=click.STRING,
    required=True,
    help='The username for the mash user.'
)
@click.pass_context
def login(context, username):
    """
    Handle mash user login.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        password = click.prompt('Enter password', type=str, hide_input=True)

        job_data = {'username': username, 'password': password}
        tokens = handle_request(
            config_data,
            '/auth/login',
            job_data=job_data,
            action='post'
        )

        tokens_file = get_tokens_file(
            config_data['config_dir'],
            config_data['profile']
        )
        save_tokens_to_file(tokens_file, tokens)
        echo_style('Login successful.', config_data['no_color'])


@click.command()
@click.pass_context
def logout(context):
    """
    Handle mash user logout.

    Deletes the current refresh token.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        tokens_file = get_tokens_file(
            config_data['config_dir'],
            config_data['profile']
        )

        tokens = get_tokens_from_file(tokens_file)
        refresh_token = tokens.get('refresh_token')

        if not refresh_token:
            echo_style(
                'No refresh token, unable to logout.',
                config_data['no_color'],
                fg='red'
            )
            sys.exit(1)

        tokens = {}  # Clear local sessions
        save_tokens_to_file(tokens_file, tokens)

        result = handle_request(
            config_data,
            '/auth/logout',
            action='delete',
            token=refresh_token
        )

        echo_style(result['msg'], config_data['no_color'])


auth.add_command(login)
auth.add_command(logout)
auth.add_command(token)
