# -*- coding: utf-8 -*-

"""mash client CLI Azure account endpoints using click library."""

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
def azure():
    """
    Handle mash azure account requests.
    """


@click.command()
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to create.'
)
@click.option(
    '--region',
    type=click.STRING,
    required=True,
    help='The region where the test instance will be launched.'
)
@click.option(
    '--source-container',
    type=click.STRING,
    required=True,
    help='The name of the container that images will be'
         ' uploaded to and tested.'
)
@click.option(
    '--source-resource-group',
    type=click.STRING,
    required=True,
    help='The name of the resource group where '
         'the source storage account exists.'
)
@click.option(
    '--source-storage-account',
    type=click.STRING,
    required=True,
    help='The name of the ARM based storage account '
         'where the source container exists.'
)
@click.option(
    '--credentials',
    type=click.Path(exists=True),
    required=True,
    help='The JSON service account credentials file.'
)
@click.pass_context
def add(
    context, name, region, source_container,
    source_resource_group, source_storage_account,
    credentials
):
    """
    Add an Azure account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(credentials) as credentials_file:
            creds = json.load(credentials_file)

        data = {
            'account_name': name,
            'credentials': creds,
            'region': region,
            'source_container': source_container,
            'source_resource_group': source_resource_group,
            'source_storage_account': source_storage_account
        }

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/azure/',
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
    Get info for an Azure account.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/azure/{name}'.format(name=name),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='list')
@click.pass_context
def list_azure_accounts(context):
    """
    Get a list of all Azure accounts.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/azure/',
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
           '`mash account azure update`.'
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
    Delete an azure account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/azure/{name}'.format(name=name),
            action='delete'
        )

        echo_style(result['msg'], config_data['no_color'])


@click.command()
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to create.'
)
@click.option(
    '--region',
    type=click.STRING,
    help='The region where the test instance will be launched.'
)
@click.option(
    '--source-container',
    type=click.STRING,
    help='The name of the container that images will be'
         ' uploaded to and tested.'
)
@click.option(
    '--source-resource-group',
    type=click.STRING,
    help='The name of the resource group where '
         'the source storage account exists.'
)
@click.option(
    '--source-storage-account',
    type=click.STRING,
    help='The name of the ARM based storage account '
         'where the source container exists.'
)
@click.option(
    '--credentials',
    type=click.Path(exists=True),
    help='The JSON service account credentials file.'
)
@click.pass_context
def update(
    context, name, region, source_container,
    source_resource_group, source_storage_account,
    credentials
):
    """
    Update an Azure account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {}

        if credentials:
            with open(credentials) as credentials_file:
                creds = json.load(credentials_file)

            data['credentials'] = creds

        if region:
            data['region'] = region

        if source_container:
            data['source_container'] = source_container

        if source_resource_group:
            data['source_resource_group'] = source_resource_group

        if source_storage_account:
            data['source_storage_account'] = source_storage_account

        if not data:
            echo_style('Nothing to update', config_data['no_color'], fg='red')
            sys.exit(1)

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/azure/{name}'.format(name=name),
            data
        )

        echo_dict(result, config_data['no_color'])


azure.add_command(add)
azure.add_command(get)
azure.add_command(list_azure_accounts)
azure.add_command(delete)
azure.add_command(update)
