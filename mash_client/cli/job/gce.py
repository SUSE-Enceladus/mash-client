# -*- coding: utf-8 -*-

"""mash client CLI gce job endpoints using click library."""

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

from mash_client.cli_utils import (
    get_config,
    handle_errors,
    handle_request_with_token,
    echo_dict
)


@click.group()
def gce():
    """
    Submit GCE job requests.
    """


@click.command()
@click.argument(
    'document',
    type=click.Path(exists=True)
)
@click.pass_context
def add(context, document):
    """
    Send add gce job request to mash server based on provided json document.
    """
    config_data = get_config(context.obj)

    with handle_errors(config_data['log_level'], config_data['no_color']):
        with open(document) as job_file:
            job_data = json.load(job_file)

        result = handle_request_with_token(
            config_data,
            '/jobs/gce/',
            job_data
        )
        echo_dict(result, config_data['no_color'])


gce.add_command(add)
