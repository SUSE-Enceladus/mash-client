# -*- coding: utf-8 -*-

"""mash client CLI OCI account endpoints using click library."""

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
def oci():
    """
    Handle mash OCI account requests.
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
    '--availability-domain',
    type=click.STRING,
    required=True,
    help='The availability domain that '
         'will be used for launching test instances.'
)
@click.option(
    '--compartment-id',
    type=click.STRING,
    required=True,
    help='The compartment ID where the images will stored.'
)
@click.option(
    '--oci-user-id',
    type=click.STRING,
    required=True,
    help='The ID for the OCI user.'
)
@click.option(
    '--tenancy',
    type=click.STRING,
    required=True,
    help='The OCI tenancy where the user exists.'
)
@click.option(
    '--signing-key-file',
    type=click.Path(exists=True),
    required=True,
    help='The path to the private signing key'
         ' used for validating OCI API calls.'
)
@click.pass_context
def add(
    context, name, bucket, region, availability_domain,
    compartment_id, oci_user_id, tenancy, signing_key_file
):
    """
    Add a OCI account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(signing_key_file) as key_file:
            signing_key = key_file.read()

        data = {
            'account_name': name,
            'bucket': bucket,
            'region': region,
            'availability_domain': availability_domain,
            'compartment_id': compartment_id,
            'oci_user_id': oci_user_id,
            'tenancy': tenancy,
            'signing_key': signing_key
        }

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/oci/',
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
    Get info for a OCI account.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/oci/{name}'.format(name=name),
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='list')
@click.pass_context
def list_oci_accounts(context):
    """
    Get a list of all oci accounts.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/oci/',
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
           '`mash account oci update`.'
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
    Delete an OCI account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/v1/accounts/oci/{name}'.format(name=name),
            action='delete'
        )

        echo_style(result['msg'], config_data['no_color'])


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
    help='The storage bucket where images will be uploaded.'
)
@click.option(
    '--region',
    type=click.STRING,
    help='The region where the test instances will be launched.'
)
@click.option(
    '--availability-domain',
    type=click.STRING,
    help='The availability domain that '
         'will be used for launching test instances.'
)
@click.option(
    '--compartment-id',
    type=click.STRING,
    help='The compartment ID where the images will stored.'
)
@click.option(
    '--oci-user-id',
    type=click.STRING,
    help='The ID for the OCI user.'
)
@click.option(
    '--tenancy',
    type=click.STRING,
    help='The OCI tenancy where the user exists.'
)
@click.option(
    '--signing-key-file',
    type=click.Path(exists=True),
    help='The path to the private signing key'
         ' used for validating OCI API calls.'
)
@click.pass_context
def update(
    context, name, bucket, region, availability_domain,
    compartment_id, oci_user_id, tenancy, signing_key_file
):
    """
    Update a OCI account in the user name space on the MASH server.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {}

        if signing_key_file:
            with open(signing_key_file) as key_file:
                signing_key = key_file.read()

            data['signing_key'] = signing_key

        if bucket:
            data['bucket'] = bucket

        if region:
            data['region'] = region

        if availability_domain:
            data['availability_domain'] = availability_domain

        if compartment_id:
            data['compartment_id'] = compartment_id

        if oci_user_id:
            data['oci_user_id'] = oci_user_id

        if tenancy:
            data['tenancy'] = tenancy

        if not data:
            echo_style('Nothing to update', config_data['no_color'], fg='red')
            sys.exit(1)

        result = handle_request_with_token(
            config_data,
            '/v1/accounts/oci/{name}'.format(name=name),
            data
        )

        echo_dict(result, config_data['no_color'])


oci.add_command(add)
oci.add_command(get)
oci.add_command(list_oci_accounts)
oci.add_command(delete)
oci.add_command(update)
