from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_delete(mock_requests, mock_time):
    """Test mash job delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Job deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'delete', '--job-id',
            '12345678-1234-1234-1234-123456789012', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'Job deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_info(mock_requests, mock_time):
    """Test mash job get info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'job_id': '23fc826b-f6f5-4fbe-947d-52dcd097f0bc',
        'last_service': 'deprecation',
        'utctime': 'now',
        'image': 'test_image_oem',
        'download_url':
            'http://download.opensuse.org/repositories/Cloud:Tools/images',
        'cloud_architecture': 'x86_64'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'info',
            '--job-id', '23fc826b-f6f5-4fbe-947d-52dcd097f0bc'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0bc' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_list(mock_requests, mock_time):
    """Test mash job get info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'job_id': '23fc826b-f6f5-4fbe-947d-52dcd097f0bc',
        'last_service': 'deprecation',
        'utctime': 'now',
        'image': 'test_image_oem',
        'download_url':
            'http://download.opensuse.org/repositories/Cloud:Tools/images',
        'cloud_architecture': 'x86_64'
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'list'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0bc' in result.output
