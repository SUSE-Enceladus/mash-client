#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
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

import json
import os

from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner

tokens = {
    'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                    'eyJpYXQiOjE1NjgxNDk1ODIsIm5iZiI6MTU2OD'
                    'E0OTU4MiwianRpIjoiMzZiZGEzZTgtNzZhNC00M'
                    'Dc4LWEzZjQtMDI3ZDUxNmIzMTIxIiwiZXhwIjoxN'
                    'TY4MTUwNDgyLCJpZGVudGl0eSI6InVzZXIxIiwiZn'
                    'Jlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.'
                    'BazKmbCFHJVjjhl82g48CErDwYcvaD5VwdrJwTcW19w',
    'refresh_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                     'eyJpYXQiOjE1NjgxNDk1ODIsIm5iZiI6MTU2ODE0OTU4Miw'
                     'ianRpIjoiZmY0MTE1YzQtZDMwZi00YThmLWE0OGEtOGY1NTI'
                     '1MmQ2YTMzIiwiZXhwIjoxNTcwNzQxNTgyLCJpZGVudGl0eSI6'
                     'InVzZXIxIiwidHlwZSI6InJlZnJlc2gifQ.'
                     'qtjLm5-atYFWlBRHcsiahIVcYRRGdPEJYIZfaSLTVvE'
}


@patch('mash_client.cli_utils.requests')
def test_auth_login(mock_requests):
    """Test mash auth login."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = tokens
    mock_requests.post.return_value = response

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'auth', 'login', '--username', 'user1'
        ],
        input='secretpassword123\n'
    )
    assert result.exit_code == 0
    assert 'Login successful' in result.output


@patch('mash_client.cli_utils.requests')
def test_auth_logout(mock_requests):
    """Test mash auth login."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Logout successful'}
    mock_requests.delete.return_value = response

    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs('tests/data/')
        with open('tests/data/default_tokens.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        result = runner.invoke(main, ['-C', 'tests/data/', 'auth', 'logout'])

    assert result.exit_code == 0
    assert 'Logout successful' in result.output
