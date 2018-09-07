# -*- coding: utf-8 -*-

"""mash client CLI endpoints using click library."""

# Copyright (c) 2018 SUSE LLC
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
import logging

from mash_client.cli_utils import (
    get_config, handle_errors, handle_request
)


def print_license(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('GPLv3+')
    ctx.exit()


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
@click.version_option()
@click.option(
    '--license',
    is_flag=True,
    callback=print_license,
    expose_value=False,
    is_eager=True,
    help='Show license information and exit.'
)
@click.option(
    '-C',
    '--config',
    type=click.Path(exists=True),
    help='mash client config file location. Default: ~/.config/mash/config'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '--host',
    help='Host for the MASH server instance.'
)
@click.option(
    '--port',
    help='Port for the MASH host.'
)
@click.option(
    '--debug',
    'log_level',
    flag_value=logging.DEBUG,
    help='Display debug level logging to console.'
)
@click.option(
    '--verbose',
    'log_level',
    flag_value=logging.INFO,
    default=True,
    help='(Default) Display logging info to console.'
)
@click.option(
    '--quiet',
    'log_level',
    flag_value=logging.WARNING,
    help='Silence logging information on test run.'
)
@click.pass_context
def main(context, config, no_color, host, port, log_level):
    """
    mash client provides a command line interface to access mash servers.
    """
    if context.obj is None:
        context.obj = {}

    context.obj['config'] = config
    context.obj['no_color'] = no_color
    context.obj['host'] = host
    context.obj['port'] = port
    context.obj['log_level'] = log_level


@click.group()
def job():
    """
    Handle mash job requests.
    """


@click.command()
@click.argument(
    'document',
    type=click.Path(exists=True)
)
@click.pass_context
def add(context, document):
    """
    Send add job request to mash server based on provided json document.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(document) as job_file:
            job_data = json.load(job_file)

        handle_request(config_data, '/add_job', job_data)


@click.command()
@click.option(
    '--delete',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete job?'
)
@click.argument(
    'job_id',
    type=click.UUID
)
@click.pass_context
def delete(context, job_id):
    """
    Delete a job given the UUID.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        handle_request(config_data, '/delete_job/{0}'.format(job_id))


@click.group()
def account():
    """
    Handle mash account requests.
    """


@click.command(name='delete')
@click.option(
    '--delete',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete account?'
)
@click.argument(
    'account_name',
    type=click.STRING
)
@click.argument(
    'provider',
    type=click.STRING
)
@click.argument(
    'requesting_user',
    type=click.STRING
)
@click.pass_context
def delete_account(context, account_name, provider, requesting_user):
    """
    Delete account given the provided args.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        job_data = {
            'account_name': account_name,
            'provider': provider,
            'requesting_user': requesting_user
        }
        handle_request(config_data, '/delete_account', job_data)


@click.group(name='add')
def add_account():
    """
    Handle mash account add requests.
    """


@click.command(name='ec2')
@click.option(
    '--additional-regions',
    is_flag=True,
    help='Add additional regions for account.'
)
@click.option(
    '--group',
    type=click.STRING,
    help='Group name to place account in.'
)
@click.argument(
    'account_name',
    type=click.STRING
)
@click.argument(
    'partition',
    type=click.STRING
)
@click.argument(
    'requesting_user',
    type=click.STRING
)
@click.argument(
    'access_key_id',
    type=click.STRING
)
@click.argument(
    'secret_access_key',
    type=click.STRING
)
@click.pass_context
def add_ec2_account(
    context, additional_regions, group, account_name, partition,
    requesting_user, access_key_id, secret_access_key
):
    """
    Add EC2 account given the provided args.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        data = {
            'account_name': account_name,
            'credentials': {
                'access_key_id': access_key_id,
                'secret_access_key': secret_access_key
            },
            'partition': partition,
            'provider': 'ec2',
            'requesting_user': requesting_user
        }

        if additional_regions:
            regions = []

            while True:
                if click.confirm('Add an additional region?'):
                    name = click.prompt('Enter the region name', type=str)
                    helper_image = click.prompt(
                        'Enter the helper image id',
                        type=str
                    )

                    regions.append({
                        'name': name,
                        'helper_image': helper_image
                    })
                else:
                    break

            data['additional_regions'] = regions

        if group:
            data['group'] = group

        handle_request(config_data, '/add_account', data)


@click.command(name='azure')
@click.option(
    '--group',
    type=click.STRING,
    help='Group name to place account in.'
)
@click.argument(
    'account_name',
    type=click.STRING
)
@click.argument(
    'container_name',
    type=click.STRING
)
@click.argument(
    'region',
    type=click.STRING
)
@click.argument(
    'requesting_user',
    type=click.STRING
)
@click.argument(
    'resource_group',
    type=click.STRING
)
@click.argument(
    'storage_account',
    type=click.STRING
)
@click.argument(
    'credentials_path',
    type=click.Path(exists=True)
)
@click.pass_context
def add_azure_account(
    context, group, account_name, container_name, region,
    requesting_user, resource_group, storage_account, credentials_path
):
    """
    Add Azure account given the provided args.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(credentials_path) as credentials_file:
            credentials = json.load(credentials_file)

        data = {
            'account_name': account_name,
            'container_name': container_name,
            'credentials': credentials,
            'provider': 'azure',
            'region': region,
            'requesting_user': requesting_user,
            'resource_group': resource_group,
            'storage_account': storage_account
        }

        if group:
            data['group'] = group

        handle_request(config_data, '/add_account', data)


job.add_command(add)
job.add_command(delete)
main.add_command(job)
account.add_command(delete_account)
add_account.add_command(add_ec2_account)
add_account.add_command(add_azure_account)
account.add_command(add_account)
main.add_command(account)
