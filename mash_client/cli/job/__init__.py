# -*- coding: utf-8 -*-

"""mash client CLI job endpoints using click library."""

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

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request_with_token,
    abort_if_false,
    echo_dict,
    echo_style
)

from mash_client.cli.job.azure import azure
from mash_client.cli.job.ec2 import ec2
from mash_client.cli.job.gce import gce
from mash_client.cli.job.oci import oci


@click.group()
def job():
    """
    Submit job requests to the MASH server pipeline.
    """


@click.command(name='list')
@click.pass_context
def list_jobs(context):
    """
    List all jobs in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/jobs/',
            action='get'
        )

        echo_dict(result, config_data['no_color'])


@click.command(name='info')
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job to be removed '
         'from the MASH server pipeline.'
)
@click.pass_context
def get(context, job_id):
    """
    Get info for a job in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/jobs/{0}'.format(job_id),
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
    prompt='Are you sure you want to delete job?'
)
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job to be removed '
         'from the MASH server pipeline.'
)
@click.pass_context
def delete(context, job_id):
    """
    Delete the job with the given ID from the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = handle_request_with_token(
            config_data,
            '/jobs/{0}'.format(job_id),
            action='delete'
        )

        echo_style(result['msg'], config_data['no_color'])


job.add_command(delete)
job.add_command(get)
job.add_command(list_jobs)

job.add_command(azure)
job.add_command(ec2)
job.add_command(gce)
job.add_command(oci)
