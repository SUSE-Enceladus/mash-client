# -*- coding: utf-8 -*-

"""mash client CLI token endpoints using click library."""

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
    echo_dict,
    echo_style,
    refresh_token,
    handle_request_with_token
)


@click.group()
def token():
    """
    Submit token requests.
    """


@click.command()
@click.pass_context
def refresh(context):
    """
    Handle token refresh.

    Get a new access token using current refresh token.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        refresh_token(config_data)
        echo_style('Token refreshed.', config_data['no_color'])


@click.command(name='list')
@click.pass_context
def token_list(context):
    """
    Return a list of JWT tokens for user.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/auth/token',
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='info')
@click.option(
    '--jti',
    type=click.STRING,
    required=True,
    help='The token jti UUID.'
)
@click.pass_context
def get(context, jti):
    """
    Return information for token matching jti.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/auth/token/{jti}'.format(jti=jti),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command()
@click.option(
    '--jti',
    type=click.STRING,
    help='The token jti UUID.'
)
@click.pass_context
def delete(context, jti):
    """
    If no jti is provided delete all tokens.

    Otherwise delete token matching the jti.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        if jti:
            result = handle_request_with_token(
                config_data,
                '/v1/auth/token/{jti}'.format(jti=jti),
                action='delete'
            )
        elif click.confirm('Are you sure you want to delete all tokens?'):
            result = handle_request_with_token(
                config_data,
                '/v1/auth/token',
                action='delete'
            )
        else:
            echo_style('No tokens deleted', config_data['no_color'], fg='red')
            sys.exit(1)

        echo_style(result['msg'], config_data['no_color'])


token.add_command(delete)
token.add_command(get)
token.add_command(token_list)
token.add_command(refresh)
