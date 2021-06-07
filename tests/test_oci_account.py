from unittest.mock import Mock, patch

from mash_client.cli import main

from click.testing import CliRunner


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_delete_oci(mock_requests, mock_time):
    """Test mash account delete."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'msg': 'oci account deleted'}
    mock_requests.delete.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'delete',
            '--name', 'acnt1', '--force'
        ]
    )
    assert result.exit_code == 0
    assert 'oci account deleted' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_add_oci(mock_requests, mock_time):
    """Test mash account add oci."""
    response = Mock()
    response.status_code = 201
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-phoenix-1',
        'availability_domain': 'Omic:PHX-AD-1',
        'compartment_id': 'ocid1.compartment.oc1..',
        'oci_user_id': 'ocid1.user.oc1..',
        'tenancy': 'ocid1.tenancy.oc1..'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'add',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--region', 'us-phoenix-1', '--availability-domain',
            'Omic:PHX-AD-1', '--compartment-id', 'ocid1.compartment.oc1..',
            '--oci-user-id', 'ocid1.user.oc1..', '--tenancy',
            'ocid1.tenancy.oc1..', '--signing-key-file', 'tests/data/test.pem'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_oci_account_info(mock_requests, mock_time):
    """Test mash oci account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-phoenix-1',
        'availability_domain': 'Omic:PHX-AD-1',
        'compartment_id': 'ocid1.compartment.oc1..',
        'oci_user_id': 'ocid1.user.oc1..',
        'tenancy': 'ocid1.tenancy.oc1..'
    }
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'info',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_oci_account_list(mock_requests, mock_time):
    """Test mash oci account info."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = [{
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-phoenix-1',
        'availability_domain': 'Omic:PHX-AD-1',
        'compartment_id': 'ocid1.compartment.oc1..',
        'oci_user_id': 'ocid1.user.oc1..',
        'tenancy': 'ocid1.tenancy.oc1..'
    }]
    mock_requests.get.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'list'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output


@patch('mash_client.cli_utils.time')
@patch('mash_client.cli_utils.requests')
def test_account_update_oci(mock_requests, mock_time):
    """Test mash account update oci."""
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'id': '1',
        'name': 'acnt1',
        'bucket': 'storage_bucket',
        'region': 'us-phoenix-1',
        'availability_domain': 'Omic:PHX-AD-1',
        'compartment_id': 'ocid1.compartment.oc1..',
        'oci_user_id': 'ocid1.user.oc1..',
        'tenancy': 'ocid1.tenancy.oc1..'
    }
    mock_requests.post.return_value = response
    mock_time.time.return_value = 1568150470

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'update',
            '--name', 'acnt1', '--bucket', 'storage_bucket',
            '--region', 'us-phoenix-1', '--availability-domain',
            'Omic:PHX-AD-1', '--compartment-id', 'ocid1.compartment.oc1..',
            '--oci-user-id', 'ocid1.user.oc1..', '--tenancy',
            'ocid1.tenancy.oc1..', '--signing-key-file', 'tests/data/test.pem'
        ]
    )
    assert result.exit_code == 0
    assert 'acnt1' in result.output

    # No updates
    result = runner.invoke(
        main,
        [
            '-C', 'tests/data/', 'account', 'oci', 'update',
            '--name', 'acnt1'
        ]
    )
    assert result.exit_code == 1
    assert 'Nothing to update' in result.output
