#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MASH client cli unit tests."""

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

import vcr

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


@vcr.use_cassette('tests/cassettes/job_add_invalid.yml')
def test_job_add_invalid():
    """Test mash job add invalid job."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'job', 'add',
            'tests/data/invalid_job.json'
        ]
    )
    assert result.exit_code == 1
    assert "'utctime' is a required property" in result.output


@vcr.use_cassette('tests/cassettes/job_add.yml')
def test_job_add():
    """Test mash job add valid job."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        ['-C', 'tests/data/.config', 'job', 'add', 'tests/data/job.json']
    )
    assert result.exit_code == 0
    assert 'Add job request submitted.' in result.output


@vcr.use_cassette('tests/cassettes/job_delete.yml')
def test_job_delete():
    """Test mash job delete."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'job', 'delete', '--job-id',
            '12345678-1234-1234-1234-123456789012', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'Delete job request submitted.' in result.output


@vcr.use_cassette('tests/cassettes/account_delete.yml')
def test_account_delete():
    """Test mash account delete."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'account', 'delete', '--cloud', 'ec2',
            '--name', 'acnt1', '--mash-user', 'user1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'Delete account request submitted.' in result.output


@vcr.use_cassette('tests/cassettes/account_add_ec2.yml')
def test_account_add_ec2():
    """Test mash account add ec2."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'account', 'add', 'ec2',
            '--additional-regions', '--name', 'acnt1', '--partition', 'aws',
            '--mash-user', 'user1', '--access-key-id', '123456',
            '--secret-access-key', '654321'
        ],
        input='y\n'
              'us-east-5\n'
              'ami-12345\n'
              'n'
    )
    assert result.exit_code == 0
    assert 'Add account request submitted.' in result.output


@vcr.use_cassette('tests/cassettes/account_add_azure.yml')
def test_account_add_azure():
    """Test mash account add azure."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'account', 'add', 'azure',
            '--name', 'acnt1', '--region', 'westus', '--mash-user', 'user1',
            '--source-container', 'sc1', '--source-resource-group', 'srg1',
            '--source-storage-account', 'ssa', '--destination-container',
            'dc1', '--destination-resource-group', 'drg1',
            '--destination-storage-account', 'dsa1', '--credentials',
            'tests/data/azure_creds.json'
        ]
    )
    assert result.exit_code == 0
    assert 'Add account request submitted.' in result.output


@vcr.use_cassette('tests/cassettes/account_add_gce.yml')
def test_account_add_gce():
    """Test mash account add gce."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/.config', 'account', 'add', 'gce',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--zone', 'us-west1-a', '--mash-user', 'user1', '--credentials',
            'tests/data/gce_creds.json'
        ]
    )
    assert result.exit_code == 0
    assert 'Add account request submitted.' in result.output
