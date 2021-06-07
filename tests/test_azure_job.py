import json

from unittest.mock import Mock, patch
from mash_client.cli import main
from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_job_add_azure(mock_requests, mock_time):
    """Test mash job add valid job."""
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
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'azure',
            'add', 'tests/data/azure_job.json'
        ]
    )
    assert result.exit_code == 0
    assert '23fc826b-f6f5-4fbe-947d-52dcd097f0bc' in result.output


@patch('mash_client.cli_utils.requests')
def test_get_job_schema(mock_requests):
    """Test mash job get annotated schema."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'additionalProperties': False,
        'properties': {
            'cleanup_images': {
                'example': True,
                'type': 'boolean'
            },
            'cloud_account': {
                'description': '',
                'example': 'account1',
                'minLength': 1,
                'type': 'string'
            }
        },
        'required': [
            'cloud_account'
        ],
        'type': 'object'
    }
    mock_requests.get.return_value = response

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'job', 'oci', 'schema', '--annotated'
        ]
    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['cloud_account']['example'] == 'account1'
