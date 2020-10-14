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

from mash_client.cli_utils import handle_request, get_annotated_property


def get_job_schema_by_cloud(
    config_data,
    output_style,
    cloud,
    raise_for_status=True
):
    result = handle_request(
        config_data,
        '/jobs/{cloud}/'.format(cloud=cloud),
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
