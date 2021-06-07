from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_delete_gce(mock_requests, mock_time):
    """Test mash account delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'GCE account deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'delete',
            '--name', 'acnt1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'GCE account deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_add_gce(mock_requests, mock_time):
    """Test mash account add gce."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-west1-a',
        'testing_account': 'testacnt',
        'is_publishing_account': True
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'add',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--zone', 'us-west1-a', '--credentials',
            'tests/data/gce_creds.json', '--testing-account', 'testacnt',
            '--is-publishing-account'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_ge_account_info(mock_requests, mock_time):
    """Test mash gce account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-west1-a',
        'testing_account': 'testacnt',
        'is_publishing_account': True
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'info',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_ge_account_list(mock_requests, mock_time):
    """Test mash gce account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-west1-a',
        'testing_account': 'testacnt',
        'is_publishing_account': True
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'list'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_update_gce(mock_requests, mock_time):
    """Test mash account update gce."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-west1-a',
        'testing_account': 'testacnt',
        'is_publishing_account': True
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'update',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--zone', 'us-west1-a', '--credentials',
            'tests/data/gce_creds.json', '--testing-account', 'testacnt'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output

    # No updates
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'gce', 'update',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 1
    assert 'Nothing to update' in result.output
