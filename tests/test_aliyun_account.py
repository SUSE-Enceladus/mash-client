from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_delete_aliyun(mock_requests, mock_time):
    """Test mash account delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Aliyun account deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'delete',
            '--name', 'acnt1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'Aliyun account deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_add_aliyun(mock_requests, mock_time):
    """Test mash account add aliyun."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'cn-beijing',
        'security_group_id': 'sg1',
        'vswitch_id': 'vs1'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'add',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--region', 'cn-beijing', '--access-key', '123456',
            '--access-secret', '654321', '--security-group-id',
            'sg1', '--vswitch-id', 'vs1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_aliyun_account_info(mock_requests, mock_time):
    """Test mash aliyun account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'cn-beijing',
        'security_group_id': 'sg1',
        'vswitch_id': 'vs1'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'info',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_aliyun_account_list(mock_requests, mock_time):
    """Test mash aliyun account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'cn-beijing',
        'security_group_id': 'sg1',
        'vswitch_id': 'vs1'
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'list'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_update_aliyun(mock_requests, mock_time):
    """Test mash account update aliyun."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'cn-beijing',
        'security_group_id': 'sg1',
        'vswitch_id': 'vs1'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'update',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--region', 'cn-beijing', '--access-key', '123456',
            '--access-secret', '654321', '--security-group-id',
            'sg1', '--vswitch-id', 'vs1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output

    # No updates
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'aliyun', 'update',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 1
    assert 'Nothing to update' in result.output
