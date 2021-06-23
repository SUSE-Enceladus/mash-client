import json

from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


test_results = {
    "summary": {
        "duration": 1.618,
        "num_tests": 3,
        "passed": 1,
        "skipped": 1,
        "failed": 1
    },
    'tests': [
        {
            'nodeid': 'test_soft_reboot',
            'outcome': 'failed',
            'test_index': 0
        },
        {
            'nodeid': 'test_sles_motd.py::test_sles_motd',
            'outcome': 'passed',
            'test_index': 1
        },
        {
            'nodeid': 'test_sles_license.py::test_sles_license',
            'outcome': 'skipped',
            'test_index': 2
        }
    ]
}


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_delete(mock_requests, mock_time):
    """Test mash job delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'Job deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

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
    mock_time.time.return_value = 1568150470

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
def test_job_wait(mock_requests, mock_time):
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
        'cloud_architecture': 'x86_64',
        'state': 'finished'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'wait',
            '--job-id', '23fc826b-f6f5-4fbe-947d-52dcd097f0bc'
        ]
    )
    assert result.exit_code == 0
    assert 'finished' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_status(mock_requests, mock_time):
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
        'cloud_architecture': 'x86_64',
        'state': 'running',
        'current_service': 'test'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'status',
            '--job-id', '23fc826b-f6f5-4fbe-947d-52dcd097f0bc'
        ]
    )
    assert result.exit_code == 0
    assert 'running' in result.output
    assert 'test' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_test_results(mock_requests, mock_time):
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
        'cloud_architecture': 'x86_64',
        'state': 'finished',
        'data': {
            'test_results': json.dumps(test_results)
        }
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'test-results',
            '--job-id', '23fc826b-f6f5-4fbe-947d-52dcd097f0bc',
            '--verbose'
        ]
    )
    assert result.exit_code == 0
    assert 'FAILED tests=3|pass=1|skip=1|fail=1|error=0' in result.output
    assert 'test_sles_license' in result.output


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
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'list'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0bc' in result.output
