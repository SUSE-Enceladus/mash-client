from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_add_oci(mock_requests, mock_time):
    """Test mash oci job add valid job."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'job_id': '23fc826b-f6f5-4fbe-947d-52dcd097f0bc',
        'last_service': 'deprecation',
        'utctime': 'now',
        'image': 'test_image_oem',
        'download_url':
            'http://download.opensuse.org/repositories/Cloud:Tools/images',
        'cloud_architecture': 'x86_64'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150480

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'oci',
            'add', 'tests/data/oci_job.json'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0bc' in result.output
