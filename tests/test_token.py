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


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_token_refresh(mock_requests, mock_time):
    """Test mash token refresh."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = tokens
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    with runner.isolated_filesystem():
        os.makedirs('tests/data/')
        with open('tests/data/default_tokens.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        result = runner.invoke(
            main,
            [
                '-C', 'tests/data/', 'auth', 'token', 'refresh'
            ]
        )
    assert result.exit_code == 0
    assert 'Token refreshed.' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_get_token(mock_requests, mock_time):
    """Test mash get token."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'jti': '23fc826b-f6f5-4fbe-947d-52dcd097f0b',
        'token_type': 'access',
        'expires': '2019-09-13T16:34:22.901Z'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'auth', 'token', 'info',
            '--jti', '23fc826b-f6f5-4fbe-947d-52dcd097f0b'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0b' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_token_list(mock_requests, mock_time):
    """Test mash token list."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'jti': '23fc826b-f6f5-4fbe-947d-52dcd097f0b',
        'token_type': 'access',
        'expires': '2019-09-13T16:34:22.901Z'
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'auth', 'token', 'list'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0b' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_token_delete(mock_requests, mock_time):
    """Test mash token delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Token revoked'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'auth', 'token', 'delete',
            '--jti', '23fc826b-f6f5-4fbe-947d-52dcd097f0b'
        ]
    )
    assert result.exit_code == 0
    assert 'Token revoked' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_token_delete_all(mock_requests, mock_time):
    """Test mash token delete all."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Successfully deleted 2 tokens'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'auth', 'token', 'delete'
        ],
        input='y\n'
    )
    assert result.exit_code == 0
    assert 'Successfully deleted 2 tokens' in result.output
