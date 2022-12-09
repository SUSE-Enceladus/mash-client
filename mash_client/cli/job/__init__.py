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
import sys
import time

from contextlib import suppress

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request_with_token,
    abort_if_false,
    echo_dict,
    echo_style,
    echo_results
)
from mash_client.controller import (
    delete_job,
    get_job,
    list_user_jobs,
    get_job_status,
    get_job_test_results
)

from mash_client.cli.job.azure import azure
from mash_client.cli.job.ec2 import ec2
from mash_client.cli.job.gce import gce
from mash_client.cli.job.oci import oci
from mash_client.cli.job.aliyun import aliyun


@click.group()
def job():
    """
    Submit job requests to the MASH server pipeline.
    """


@click.command(name='list')
@click.option(
    '--page',
    type=click.INT,
    help='The page number of results to return.'
)
@click.option(
    '--per-page',
    type=click.INT,
    help='The number of results to return per page.'
)
@click.option(
    '--api-version',
    type=click.Choice(['v1']),
    help='The version of the API to use for request. '
         'Defaults to the latest API version based on '
         'client version.'
)
@click.pass_context
def list_jobs(context, api_version, per_page, page):
    """
    List all jobs in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        kwargs = {}
        if page:
            kwargs['page'] = page
        if per_page:
            kwargs['per_page'] = per_page
        if api_version:
            kwargs['api_version'] = api_version

        result = list_user_jobs(config_data, **kwargs)
        echo_dict(result, config_data['no_color'])


@click.command(name='info')
@click.option(
    '--show-data',
    is_flag=True,
    help='Include all status info for the job.'
)
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job to retrieve.'
)
@click.pass_context
def get(context, job_id, show_data):
    """
    Get info for a job in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result = get_job(config_data, job_id)

        if not show_data:
            with suppress(KeyError):
                del result['data']
        elif 'test_results' in result['data']:
            # Retrieved via `mash job test-results` command
            del result['data']['test_results']

        echo_dict(result, config_data['no_color'])


@click.command()
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job for the status query.'
)
@click.pass_context
def status(context, job_id):
    """
    Get basic status for a job in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        status_info = get_job_status(config_data, job_id)
        echo_dict(status_info, config_data['no_color'])


@click.command()
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job to wait for a finished state.'
)
@click.option(
    '-t',
    '--wait-time',
    type=click.IntRange(min=60),
    default=300,
    help='The time to wait before checking job status again (seconds).'
)
@click.pass_context
def wait(context, wait_time, job_id):
    """
    Wait for job to arrive at finished or failed status.

    By default waits 5 minutes between status queries.
    """
    config_data = get_config(context.obj)
    state = 'undefined'

    while True:
        with handle_errors(config_data['log_level'], config_data['no_color']):
            result = handle_request_with_token(
                config_data,
                '/v1/jobs/{0}'.format(job_id),
                action='get'
            )

        state = result['state']

        if state not in ('running', 'undefined'):
            break

        time.sleep(wait_time)

    click.echo(state)


@click.command(name='test-results')
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    help='Display each test and subsequent result. '
         'By default only the summary is displayed.'
)
@click.option(
    '--job-id',
    type=click.UUID,
    required=True,
    help='The UUID of the job for test results query.'
)
@click.pass_context
def test_results(context, job_id, verbose):
    """
    Display test results for a job in the MASH server pipeline.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        result_data = get_job_test_results(config_data, job_id)

        if 'msg' in result_data:
            msg = ' '.join([
                result_data['msg'],
                'The data can be viewed using: '
                '"mash job info --job-id {job_id} --show-data".'
            ])
            click.secho(msg, fg='red')
            sys.exit(1)

        echo_results(
            result_data,
            config_data['no_color'],
            verbose
        )


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
        result = delete_job(config_data, job_id)
        echo_style(result['msg'], config_data['no_color'])


job.add_command(delete)
job.add_command(get)
job.add_command(list_jobs)
job.add_command(status)
job.add_command(wait)
job.add_command(test_results)

job.add_command(azure)
job.add_command(ec2)
job.add_command(gce)
job.add_command(oci)
job.add_command(aliyun)
