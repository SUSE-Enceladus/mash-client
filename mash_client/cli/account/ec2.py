# -*- coding: utf-8 -*-

"""mash client CLI ec2 account endpoints using click library."""

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
    EC2_PARTITIONS,
    get_config,
    handle_errors,
    handle_request_with_token,
    abort_if_false,
    echo_dict,
    echo_style,
    additional_regions_repl
)


@click.group(context_settings=dict(token_normalize_func=str.lower))
def ec2():
    """
    Handle mash ec2 account requests.
    """


@click.command()
@click.option(
    '--additional-regions',
    is_flag=True,
    help='Invoke region addition process to specify information '
         'for additional regions'
)
@click.option(
    '--group',
    type=click.STRING,
    help='Group name to associate the account with.'
)
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to create.'
)
@click.option(
    '--partition',
    type=click.Choice(EC2_PARTITIONS),
    required=True,
    help='The location of the EC2 account. ["aws", "aws-cn", "aws-us-gov"]'
)
@click.option(
    '--region',
    type=click.STRING,
    required=True,
    help='The target region for image upload and testing.'
)
@click.option(
    '--subnet',
    type=click.STRING,
    help='An optional subnet id for image upload and testing.'
)
@click.option(
    '--access-key-id',
    type=click.STRING,
    required=True,
    help='AWS access key.'
)
@click.option(
    '--secret-access-key',
    type=click.STRING,
    required=True,
    help='AWS secret access key.'
)
@click.pass_context
def add(
    context, additional_regions, group, name, partition,
    region, subnet, access_key_id, secret_access_key
):
    """
    Add an EC2 account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {
            'account_name': name,
            'credentials': {
                'access_key_id': access_key_id,
                'secret_access_key': secret_access_key
            },
            'partition': partition,
            'region': region
        }

        if additional_regions:
            data['additional_regions'] = additional_regions_repl()

        if group:
            data['group'] = group

        if subnet:
            data['subnet'] = subnet

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/ec2/',
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
    Get info for an ec2 account.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/ec2/{name}'.format(name=name),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='list')
@click.pass_context
def list_ec2_accounts(context):
    """
    Get a list of all ec2 accounts.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/ec2/',
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
           '`mash account ec2 update`.'
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
    Delete an ec2 account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/ec2/{name}'.format(name=name),
            action='delete'
        )

        echo_style(result['msg'], config_data['no_color'])


@click.command()
@click.option(
    '--additional-regions',
    is_flag=True,
    help='Invoke region addition process to specify information '
         'for additional regions'
)
@click.option(
    '--group',
    type=click.STRING,
    help='Group name to associate the account with.'
)
@click.option(
    '--name',
    type=click.STRING,
    required=True,
    help='Name for the account to create.'
)
@click.option(
    '--region',
    type=click.STRING,
    help='The target region for image upload and testing.'
)
@click.option(
    '--subnet',
    type=click.STRING,
    help='An optional subnet id for image upload and testing.'
)
@click.option(
    '--access-key-id',
    type=click.STRING,
    help='AWS access key.'
)
@click.option(
    '--secret-access-key',
    type=click.STRING,
    help='AWS secret access key.'
)
@click.pass_context
def update(
    context, additional_regions, group, name,
    region, subnet, access_key_id, secret_access_key
):
    """
    Update an EC2 account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {}

        if all([access_key_id, secret_access_key]):
            data['credentials'] = {
                'access_key_id': access_key_id,
                'secret_access_key': secret_access_key
            }
        elif any([access_key_id, secret_access_key]):
            echo_style(
                'Both secret_access_key and access_key_id are required '
                'when updating credentials.',
                config_data['no_color'],
                fg='red'
            )
            sys.exit(1)

        if additional_regions:
            regions = additional_regions_repl()

            if regions:
                data['additional_regions'] = regions

        if group:
            data['group'] = group

        if region:
            data['region'] = region

        if subnet:
            data['subnet'] = subnet

        if not data:
            echo_style('Nothing to update', config_data['no_color'], fg='red')
            sys.exit(1)

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/ec2/{name}'.format(name=name),
            data
        )

        echo_dict(result, config_data['no_color'])


ec2.add_command(add)
ec2.add_command(get)
ec2.add_command(list_ec2_accounts)
ec2.add_command(delete)
ec2.add_command(update)
