# -*- coding: utf-8 -*-

"""mash client CLI gce job endpoints using click library."""

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
import json

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request_with_token,
    echo_dict,
    echo_style,
    get_job_schema_by_cloud
)


@click.group()
def gce():
    """
    Submit GCE job requests.
    """


@click.command()
@click.option(
    '--dry-run',
    is_flag=True,
    help='Validate job document but do not create job.'
)
@click.argument(
    'document',
    type=click.Path(exists=True)
)
@click.pass_context
def add(context, dry_run, document):
    """
    Send add gce job request to mash server based on provided json document.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(document) as job_file:
            job_data = json.load(job_file)

        if dry_run:
            job_data['dry_run'] = True

        result = handle_request_with_token(
            config_data,
            '/jobs/gce/',
            job_data
        )

        if 'msg' in result:
            echo_style(result['msg'], config_data['no_color'])
        else:
            echo_dict(result, config_data['no_color'])


@click.command(name='schema')
@click.option(
    '--json',
    'output_style',
    flag_value='json',
    help='Prints an example json dictionary with example values.'
)
@click.option(
    '--raw',
    'output_style',
    flag_value='raw',
    help='Prints a raw jsonschema dictionary.'
)
@click.option(
    '--annotated',
    'output_style',
    flag_value='annotated',
    default=True,
    help='Prints a raw jsonschema dictionary.'
)
@click.pass_context
def get_schema(context, output_style):
    """
    Get the an annotated json dictionary for a GCE job.
    """
    get_job_schema_by_cloud(context, output_style, 'gce')


gce.add_command(add)
gce.add_command(get_schema)
