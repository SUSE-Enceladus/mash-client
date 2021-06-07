from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_add_ec2(mock_requests, mock_time):
    """Test mash account add ec2."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'partition': 'aws',
        'region': 'us-east-1',
        'subnet': 'subnet-123456789',
        'additional_regions': {
            'id': '1',
            'name': 'us-east-5',
            'helper_image': 'ami-12345'
        }
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'add',
            '--additional-regions', '--name', 'acnt1', '--partition', 'aws',
            '--region', 'us-east-1', '--subnet',
            'subnet-123456789', '--access-key-id', '123456',
            '--secret-access-key', '654321'
        ],
        input='y\n'
              'us-east-5\n'
              'ami-12345\n'
              'n'
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_delete_ec2(mock_requests, mock_time):
    """Test mash account delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'EC2 account deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'delete',
            '--name', 'acnt1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'EC2 account deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_ec2_account_info(mock_requests, mock_time):
    """Test mash ec2 account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'partition': 'aws',
        'region': 'us-east-1',
        'subnet': 'subnet-123456789',
        'additional_regions': {
            'id': '1',
            'name': 'us-east-5',
            'helper_image': 'ami-12345'
        }
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'info', '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_ec2_account_list(mock_requests, mock_time):
    """Test mash ec2 account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'name': 'acnt1',
        'partition': 'aws',
        'region': 'us-east-1',
        'subnet': 'subnet-123456789',
        'additional_regions': {
            'id': '1',
            'name': 'us-east-5',
            'helper_image': 'ami-12345'
        }
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'list'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_update_ec2(mock_requests, mock_time):
    """Test mash account update ec2."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'partition': 'aws',
        'region': 'us-east-1',
        'subnet': 'subnet-123456789',
        'additional_regions': {
            'id': '1',
            'name': 'us-east-5',
            'helper_image': 'ami-12345'
        }
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'update',
            '--additional-regions', '--name', 'acnt1',
            '--region', 'us-east-1', '--subnet',
            'subnet-123456789', '--access-key-id', '123456',
            '--secret-access-key', '654321'
        ],
        input='y\n'
              'us-east-5\n'
              'ami-12345\n'
              'n'
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output

    # Assert exit if only one credential value provided
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'update',
            '--name', 'acnt1', '--secret-access-key', '654321'
        ]
    )
    assert result.exit_code == 1
    assert 'Both secret_access_key and access_key_id' in result.output

    # No updates
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'ec2', 'update',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 1
    assert 'Nothing to update' in result.output
