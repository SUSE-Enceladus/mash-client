# -*- coding: utf-8 -*-

"""mash client CLI aliyun account endpoints using click library."""

# Copyright (c) 2021 SUSE LLC. All rights reserved.
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
    handle_request_with_token,
    abort_if_false,
    echo_dict,
    echo_style
)


@click.group(context_settings=dict(token_normalize_func=str.lower))
def aliyun():
    """
    Handle mash Aliyun account requests.
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
    '--region',
    type=click.STRING,
    required=True,
    help='The region where the test instances will be launched.'
)
@click.option(
    '--security-group-id',
    type=click.STRING,
    help='The security group ID that '
         'will be used for launching test instances.'
)
@click.option(
    '--vswitch-id',
    type=click.STRING,
    help='The vswitch ID that '
         'will be used for launching test instances.'
)
@click.option(
    '--access-key',
    type=click.STRING,
    required=True,
    help='Aliyun access key.'
)
@click.option(
    '--access-secret',
    type=click.STRING,
    required=True,
    help='Aliyun access key secret.'
)
@click.pass_context
def add(
    context, name, bucket, region, security_group_id,
    vswitch_id, access_key, access_secret
):
    """
    Add a Aliyun account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {
            'account_name': name,
            'bucket': bucket,
            'credentials': {
                'access_key': access_key,
                'access_secret': access_secret
            },
            'region': region
        }

        if security_group_id:
            data['security_group_id'] = security_group_id

        if vswitch_id:
            data['vswitch_id'] = vswitch_id

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/aliyun/',
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
    Get info for a Aliyun account.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/aliyun/{name}'.format(name=name),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='list')
@click.pass_context
def list_aliyun_accounts(context):
    """
    Get a list of all Aliyun accounts.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/aliyun/',
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
           '`mash account Aliyun update`.'
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
    Delete an Aliyun account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/aliyun/{name}'.format(name=name),
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
    '--region',
    type=click.STRING,
    help='The region where the test instances will be launched.'
)
@click.option(
    '--security-group-id',
    type=click.STRING,
    help='The security group ID that '
         'will be used for launching test instances.'
)
@click.option(
    '--vswitch-id',
    type=click.STRING,
    help='The vswitch ID that '
         'will be used for launching test instances.'
)
@click.option(
    '--access-key',
    type=click.STRING,
    help='Aliyun access key.'
)
@click.option(
    '--access-secret',
    type=click.STRING,
    help='Aliyun access key secret.'
)
@click.pass_context
def update(
    context, name, bucket, region, security_group_id, vswitch_id,
    access_key, access_secret
):
    """
    Update a Aliyun account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {}

        if all([access_key, access_secret]):
            data['credentials'] = {
                'access_key': access_key,
                'access_secret': access_secret
            }
        elif any([access_key, access_secret]):
            echo_style(
                'Both access_secret and access_key are required '
                'when updating credentials.',
                config_data['no_color'],
                fg='red'
            )
            sys.exit(1)

        if bucket:
            data['bucket'] = bucket

        if region:
            data['region'] = region

        if security_group_id:
            data['security_group_id'] = security_group_id

        if vswitch_id:
            data['vswitch_id'] = vswitch_id

        if not data:
            echo_style('Nothing to update', config_data['no_color'], fg='red')
            sys.exit(1)

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/aliyun/{name}'.format(name=name),
            data
        )

        echo_dict(result, config_data['no_color'])


aliyun.add_command(add)
aliyun.add_command(get)
aliyun.add_command(list_aliyun_accounts)
aliyun.add_command(delete)
aliyun.add_command(update)
