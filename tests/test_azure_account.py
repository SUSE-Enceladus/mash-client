from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_add_azure(mock_requests, mock_time):
    """Test mash account add azure."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'region': 'westus',
        'source_container': 'sc1',
        'source_resource_group': 'srg1',
        'source_storage_account': 'ssa'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'add',
            '--name', 'acnt1', '--region', 'westus',
            '--source-container', 'sc1', '--source-resource-group', 'srg1',
            '--source-storage-account', 'ssa', '--credentials',
            'tests/data/azure_creds.json'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_delete_azure(mock_requests, mock_time):
    """Test mash account delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Azure account deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'delete',
            '--name', 'acnt1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'Azure account deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_azure_account_info(mock_requests, mock_time):
    """Test mash azure account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'region': 'westus',
        'source_container': 'sc1',
        'source_resource_group': 'srg1',
        'source_storage_account': 'ssa'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'info',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_azure_account_list(mock_requests, mock_time):
    """Test mash azure account list."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'name': 'acnt1',
        'region': 'westus',
        'source_container': 'sc1',
        'source_resource_group': 'srg1',
        'source_storage_account': 'ssa'
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'list'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_update_azure(mock_requests, mock_time):
    """Test mash account update azure."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'region': 'westus',
        'source_container': 'sc1',
        'source_resource_group': 'srg1',
        'source_storage_account': 'ssa'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'update',
            '--name', 'acnt1', '--region', 'westus',
            '--source-container', 'sc1', '--source-resource-group', 'srg1',
            '--source-storage-account', 'ssa', '--credentials',
            'tests/data/azure_creds.json'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output

    # No updates
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'azure', 'update',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 1
    assert 'Nothing to update' in result.output
