# -*- coding: utf-8 -*-

"""Helper methods for mash client endpoints."""

# Copyright (c) 2020 SUSE LLC. All rights reserved.
#
# This file is part of mash_client. mash_client provides a command line
# utility for interfacing with a MASH server.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json

from mash_client.cli_utils import (
    handle_request,
    save_tokens_to_file,
    get_tokens_file,
    get_tokens_from_file,
    get_annotated_property,
    handle_request_with_token
)


def get_job_schema_by_cloud(
    config_data,
    output_style,
    cloud,
    raise_for_status=True
):
    result = handle_request(
        config_data,
        '/v1/jobs/{cloud}/'.format(cloud=cloud),
        action='get',
        raise_for_status=raise_for_status
    )

    if 'properties' not in result:
        return result

    if output_style == 'json':
        json_result = {}
        for key, value in result['properties'].items():
            json_result[key] = '' if value['type'] == 'string' else None

        result = json_result
    elif output_style == 'annotated':
        annotated_result = {}
        for key, value in result['properties'].items():
            annotated_result[key] = get_annotated_property(
                key,
                value,
                result.get('required', tuple())
            )

        result = annotated_result

    return result


def login_with_pass(
    config_data,
    email,
    password,
    raise_for_status=True,
    no_expiry=False
):
    job_data = {'email': email, 'password': password}

    if no_expiry:
        job_data['no_expiry'] = True

    result = handle_request(
        config_data,
        '/v1/auth/login',
        job_data=job_data,
        action='post',
        raise_for_status=raise_for_status
    )

    if 'refresh_token' not in result:
        return result

    tokens_file = get_tokens_file(
        config_data['config_dir'],
        config_data['profile']
    )
    save_tokens_to_file(tokens_file, result)

    return {'msg': 'Login successful.'}


def logout_session(config_data, raise_for_status=True):
    tokens_file = get_tokens_file(
        config_data['config_dir'],
        config_data['profile']
    )
    refresh_token = get_token(tokens_file)

    if not refresh_token:
        return {
            'msg': 'No refresh token, unable to logout.'
        }

    tokens = {}  # Clear local sessions
    save_tokens_to_file(tokens_file, tokens)

    return handle_request(
        config_data,
        '/v1/auth/logout',
        action='delete',
        token=refresh_token,
        raise_for_status=raise_for_status
    )


def get_token(tokens_file, token_type=None):
    if not token_type:
        token_type = 'refresh_token'

    tokens = get_tokens_from_file(tokens_file)
    return tokens.get(token_type)


def delete_job(config_data, job_id, raise_for_status=True):
    return handle_request_with_token(
        config_data,
        '/v1/jobs/{0}'.format(job_id),
        action='delete',
        raise_for_status=raise_for_status
    )


def get_job(config_data, job_id, raise_for_status=True):
    return handle_request_with_token(
        config_data,
        '/v1/jobs/{0}'.format(job_id),
        action='get',
        raise_for_status=raise_for_status
    )


def list_user_jobs(
    config_data,
    raise_for_status=True,
    page=None,
    per_page=None,
    api_version='v1'
):
    job_data = {}

    if page:
        job_data['page'] = page

    if per_page:
        job_data['per_page'] = per_page

    return handle_request_with_token(
        config_data,
        '/{api_version}/jobs/'.format(api_version=api_version),
        job_data=job_data,
        action='get',
        raise_for_status=raise_for_status
    )


def get_job_status(config_data, job_id, raise_for_status=True):
    result = handle_request_with_token(
        config_data,
        '/v1/jobs/{0}'.format(job_id),
        action='get',
        raise_for_status=raise_for_status
    )

    if 'state' not in result:
        return result

    status_info = {'state': result['state']}

    if result['state'] == 'running' and 'current_service' in result:
        status_info['current_service'] = result['current_service']

    return status_info


def get_job_test_results(config_data, job_id, raise_for_status=True):
    result = handle_request_with_token(
        config_data,
        '/v1/jobs/{0}'.format(job_id),
        action='get',
        raise_for_status=raise_for_status
    )

    if 'job_id' not in result:
        # An error occurred and raise_for_status is False.
        # job_id is required in all jobs.
        return result

    try:
        raw_test_results = result['data']['test_results']
    except KeyError:
        return {'msg': 'The job has no test results.'}

    try:
        result_data = json.loads(raw_test_results)
    except json.decoder.JSONDecodeError:
        return {'msg': 'The job\'s test results are malformed.'}

    return result_data


def add_job(
    config_data,
    job_data,
    cloud,
    api_version=None,
    raise_for_status=True
):
    versions = {
        'aliyun': 'v1',
        'azure': 'v1',
        'ec2': 'v1',
        'gce': 'v1',
        'oci': 'v1'
    }
    if not api_version:
        api_version = versions[cloud]

    return handle_request_with_token(
        config_data,
        '/{api_version}/jobs/{cloud}/'.format(
            api_version=api_version,
            cloud=cloud
        ),
        job_data,
        raise_for_status=raise_for_status
    )
