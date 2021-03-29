# -*- coding: utf-8 -*-

"""mash client CLI account endpoints using click library."""

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

from mash_client.cli.account.azure import azure
from mash_client.cli.account.ec2 import ec2
from mash_client.cli.account.gce import gce
from mash_client.cli.account.oci import oci
from mash_client.cli.account.aliyun import aliyun


@click.group()
def account():
    """
    Submit account requests to the MASH server.
    """


account.add_command(azure)
account.add_command(ec2)
account.add_command(gce)
account.add_command(oci)
account.add_command(aliyun)
