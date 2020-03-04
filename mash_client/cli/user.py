# -*- coding: utf-8 -*-

"""mash client CLI user endpoints using click library."""

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
    update_config,
    handle_errors,
    handle_request,
    handle_request_with_token,
    echo_dict,
    echo_style
)
from mash_client.mash_client_exceptions import MashClientException


@click.group()
def user():
    """
    Submit user requests.
    """


@click.command(name='create')
@click.option(
    '--email',
    type=click.STRING,
    required=True,
    help='The email address for the mash user.'
)
@click.pass_context
def create_user(context, email):
    """
    Handle mash user creation requests.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        pass1 = click.prompt('Enter password', type=str, hide_input=True)
        pass2 = click.prompt('Confirm password', type=str, hide_input=True)

        if pass1 != pass2:
            raise MashClientException('Passwords do not match!')

        job_data = {'email': email, 'password': pass1}
        result = handle_request(
            config_data,
            '/user/',
            job_data=job_data,
            action='post'
        )

        echo_dict(result, config_data['no_color'])

        if result.get('id'):
            update_config(context.obj, 'email', email)


@click.command(name='info')
@click.pass_context
def get_user(context):
    """
    Get mash user info.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/user/',
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='delete')
@click.pass_context
def delete_user(context):
    """
    Handle mash user deletion requests.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        if click.confirm('Are you sure you want to delete user?'):
            result = handle_request_with_token(
                config_data,
                '/user/',
                action='delete'
            )

            echo_style(
                result['msg'],
                config_data['no_color']
            )
        else:
            echo_style('Aborted', config_data['no_color'], fg='red')
            sys.exit(1)


user.add_command(create_user)
user.add_command(get_user)
user.add_command(delete_user)
