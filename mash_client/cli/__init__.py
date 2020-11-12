# -*- coding: utf-8 -*-

"""mash client CLI endpoints using click library."""

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
import logging

from mash_client.cli.auth import auth
from mash_client.cli.user import user
from mash_client.cli.account import account
from mash_client.cli.job import job
from mash_client.cli.config import config


def print_license(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('GPLv3+')
    ctx.exit()


@click.group()
@click.version_option()
@click.option(
    '--license',
    is_flag=True,
    callback=print_license,
    expose_value=False,
    is_eager=True,
    help='Show license information.'
)
@click.option(
    '-C',
    '--config-dir',
    type=click.Path(exists=True),
    help='MASH client config directory to use. Default: '
         '~/.config/mash_client/'
)
@click.option(
    '--profile',
    help='The configuration profile to use. Expected to match '
         'a config file in config directory. Example: production, '
         'for ~/.config/mash_client/production.yaml'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.option(
    '--host',
    help='Resolvable hostname for the MASH server instance. '
         'A protocol is required in the hostname: '
         'Either http:// or https://. If it is not provided '
         'the default http:// will be used.'
)
@click.option(
    '--port',
    help='The port number the MASH server is listening on.'
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
    help='Display logging info to console. (Default)'
)
@click.option(
    '--quiet',
    'log_level',
    flag_value=logging.WARNING,
    help='Disable console output.'
)
@click.pass_context
def main(context, config_dir, profile, no_color, host, port, log_level):
    """
    The command line interface allows you to interact with a MASH server.

    It provides commands to submit jobs to the MASH server pipeline or
    add/delete a user account.
    """
    if context.obj is None:
        context.obj = {}

    context.obj['config_dir'] = config_dir
    context.obj['profile'] = profile
    context.obj['no_color'] = no_color
    context.obj['host'] = host
    context.obj['port'] = port
    context.obj['log_level'] = log_level


main.add_command(job)
main.add_command(account)
main.add_command(auth)
main.add_command(user)
main.add_command(config)
