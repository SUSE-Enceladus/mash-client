#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MASH client cli unit tests."""

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

from mash_client.cli import main

from click.testing import CliRunner


def test_client_help():
    """Confirm mash --help is successful."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'The command line interface allows you to interact with a ' \
           'MASH server.' in result.output


def test_print_license():
    runner = CliRunner()
    result = runner.invoke(main, ['--license'])
    assert result.exit_code == 0
    assert result.output == 'GPLv3+\n'
