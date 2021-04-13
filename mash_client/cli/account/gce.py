# -*- coding: utf-8 -*-

"""mash client CLI gce account endpoints using click library."""

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
import sys

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request_with_token,
    abort_if_false,
    echo_dict,
    echo_style
)


@click.group(context_settings=dict(token_normalize_func=str.lower))
def gce():
    """
    Handle mash gce account requests.
    """


@click.command()
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to add.'
)
@click.option(
    '--bucket',
    type=click.STRING,
    required=True,
    help='The storage bucket where images will be uploaded.'
)
@click.option(
    '--zone',
    type=click.STRING,
    required=True,
    help='The zone where the test instances will be launched.'
)
@click.option(
    '--testing-account',
    type=click.STRING,
    help='The name of the testing account that '
         'will be used for launching test instances.'
)
@click.option(
    '--is-publishing-account',
    is_flag=True,
    help='The new account is a publishing account.'
)
@click.option(
    '--credentials',
    type=click.Path(exists=True),
    required=True,
    help='The JSON service account credentials file.'
)
@click.pass_context
def add(
    context, name, bucket, zone, testing_account,
    is_publishing_account, credentials
):
    """
    Add a GCE account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(credentials) as credentials_file:
            creds = json.load(credentials_file)

        data = {
            'account_name': name,
            'bucket': bucket,
            'credentials': creds,
            'region': zone
        }

        if testing_account:
            data['testing_account'] = testing_account

        if is_publishing_account:
            data['is_publishing_account'] = True

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/gce/',
            data
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='info')
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name of the account.'
)
@click.pass_context
def get(context, name):
    """
    Get info for a gce account.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/gce/{name}'.format(name=name),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='list')
@click.pass_context
def list_gce_accounts(context):
    """
    Get a list of all gce accounts.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/gce/',
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command()
@click.option(
    '--force',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    help='Force deletion without prompt.',
    prompt='Are you sure you want to delete account? '
           'You can make account updates instead using '
           '`mash account gce update`.'
)
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name of the account to be deleted.'
)
@click.pass_context
def delete(context, name):
    """
    Delete an gce account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/gce/{name}'.format(name=name),
            action='delete'
        )

        echo_style(result['msg'], config_data['no_color'])


@click.command()
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to update.'
)
@click.option(
    '--bucket',
    type=click.STRING,
    help='The storage bucket where images will be uploaded.'
)
@click.option(
    '--zone',
    type=click.STRING,
    help='The zone where the test instances will be launched.'
)
@click.option(
    '--testing-account',
    type=click.STRING,
    help='The name of the testing account that '
         'will be used for launching test instances.'
)
@click.option(
    '--credentials',
    type=click.Path(exists=True),
    help='The JSON service account credentials file.'
)
@click.pass_context
def update(
    context, name, bucket, zone, testing_account, credentials
):
    """
    Update a GCE account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {}

        if credentials:
            with open(credentials) as credentials_file:
                creds = json.load(credentials_file)

            data['credentials'] = creds

        if bucket:
            data['bucket'] = bucket

        if zone:
            data['region'] = zone

        if testing_account:
            data['testing_account'] = testing_account

        if not data:
            echo_style('Nothing to update', config_data['no_color'], fg='red')
            sys.exit(1)

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/gce/{name}'.format(name=name),
            data
        )

        echo_dict(result, config_data['no_color'])


gce.add_command(add)
gce.add_command(get)
gce.add_command(list_gce_accounts)
gce.add_command(delete)
gce.add_command(update)
