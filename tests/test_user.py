from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.requests')
def test_user_create(mock_requests):
    """Test mash user creation."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'email': 'user1@fake.com'
    }
    mock_requests.post.return_value = response

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'user', 'create', '--email', 'user1@fake.com'
        ],
        input='secretpassword\n'
              'secretpassword\n'
    )
    assert result.exit_code == 0
    assert 'user1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_user_info(mock_requests, mock_time):
    """Test mash user get info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'email': 'user1@fake.com'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'user', 'info'
        ]
    )
    assert result.exit_code == 0
    assert 'user1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_user_delete(mock_requests, mock_time):
    """Test mash user delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'User deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'user', 'delete'
        ],
        input='y\n'
    )
    assert result.exit_code == 0
    assert 'User deleted' in result.output
