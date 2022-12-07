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
    get_oauth2_code,
    get_free_port
)
from mash_client.cli.auth.token import token
from mash_client.mash_client_exceptions import MashClientException
from mash_client.controller import login_with_pass, logout_session


@click.group()
def auth():
    """
    Submit authentication requests.
    """


@click.command()
@click.option(
    '--email',
    type=click.STRING,
    help='The email for the mash user (default taken from config).'
)
@click.option(
    '--no-expiry',
    is_flag=True,
    help='Creates a refresh token with no expiration '
         '(default expiry is 30 days).'
)
@click.pass_context
def login(context, email, no_expiry):
    """
    Handle mash user login.
    """
    config_data = get_config(context.obj)

    if not email:
        email = config_data.get('email')

    if not email:
        echo_style(
            'No --email parameter and no email in config.',
            config_data['no_color'],
            fg='red'
        )
        sys.exit(1)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        password = click.prompt('Enter password', type=str, hide_input=True)
        result = login_with_pass(
            config_data,
            email,
            password,
            no_expiry=no_expiry
        )
        echo_style(result['msg'], config_data['no_color'])


@click.command()
@click.pass_context
def logout(context):
    """
    Handle mash user logout.

    Deletes the current refresh token.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = logout_session(config_data)
        echo_style(result['msg'], config_data['no_color'])


@click.command()
@click.pass_context
def oidc(context):
    """
    Handle mash OpenID Connect authentication.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request(
            config_data,
            '/v1/auth/oauth2',
            action='get'
        )

        redirect_port = get_free_port(result['redirect_ports'])
        if not redirect_port:
            raise MashClientException('No redirect port available')

        auth_url = '{}&redirect_uri=http%3A%2F%2Flocalhost%3A{}'.format(
            result['auth_url'], redirect_port
        )

        # display authentication message
        echo_style(
            '{}: {}'.format(result['msg'], auth_url),
            config_data['no_color']
        )
        click.launch(auth_url)

        auth_code = get_oauth2_code(redirect_port)

        if not auth_code:
            echo_style(
                'Failed login: No authentication code received.',
                config_data['no_color'],
                fg='red'
            )
            sys.exit(1)

        job_data = {
            'auth_code': auth_code,
            'state': result['state'],
            'redirect_port': redirect_port
        }

        tokens = handle_request(
            config_data,
            '/v1/auth/oauth2',
            job_data=job_data,
            action='post'
        )

        tokens_file = get_tokens_file(
            config_data['config_dir'],
            config_data['profile']
        )
        save_tokens_to_file(tokens_file, tokens)
        echo_style('Login successful.', config_data['no_color'])


auth.add_command(login)
auth.add_command(logout)
auth.add_command(token)
auth.add_command(oidc)
