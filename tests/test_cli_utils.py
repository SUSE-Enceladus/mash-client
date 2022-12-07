#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MASH client additional cli_utils unit tests."""

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

from unittest.mock import Mock, patch
from pytest import raises

from mash_client.cli_utils import RequestHandler
from mash_client.cli_utils import CodeReceivedException


@patch('mash_client.cli_utils.BaseHTTPRequestHandler.end_headers')
@patch('mash_client.cli_utils.BaseHTTPRequestHandler.send_response')
@patch('mash_client.cli_utils.BaseHTTPRequestHandler.send_header')
@patch.object(RequestHandler, '__init__', lambda x: None)
def test_request_handler(mock_send_header, mock_send_response, mock_end_hdrs):
    code = '0123456789ABCDEF'
    description = 'User+is+not+assigned+to+the+client+application.'

    rh = RequestHandler()
    setattr(rh, 'wfile', Mock())
    rh.path = 'http://localhost:9000/?code={}'.format(code)

    with raises(CodeReceivedException) as e:
        rh.do_GET()

    assert (e.value.code == code)
    mock_send_response.assert_called_once_with(200)
    mock_send_header.assert_called_once_with('Content-type', 'text/html')

    mock_send_response.reset_mock()
    mock_send_header.reset_mock()
    rh.path = 'http://localhost:9000/?error_description={}'.format(description)

    with raises(CodeReceivedException) as e:
        rh.do_GET()

    assert e.value.code is None
    mock_send_response.assert_called_once_with(200)
    mock_send_header.assert_called_once_with('Content-type', 'text/html')
