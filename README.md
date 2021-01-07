![Build Status](https://github.com/SUSE-Enceladus/mash-client/workflows/Continuous%20testing%20&%20Linting/badge.svg?branch=master)
[![Documentation Status](https://readthedocs.org/projects/mash-client/badge/?version=latest)](https://mash-client.readthedocs.io/en/latest/?badge=latest)
[![Py Versions](https://img.shields.io/pypi/pyversions/mash-client.svg)](https://pypi.org/project/mash-client/)
[![License](https://img.shields.io/pypi/l/mash-client.svg)](https://pypi.org/project/mash-client/)

**mash-client**

overview
========

**mash-client** provides a command line utility to interface with the
MASH server REST API.

Installation
============

To install the package use the following commands as root:

```shell
$ zypper ar http://download.opensuse.org/repositories/Cloud:/Tools/<distribution>
$ zypper refresh
$ zypper in mash-client
```

Requirements
============

-   Click
-   requests
-   PyYaml
-   PyJWT

# [Docs](https://mash-client.readthedocs.io/en/latest/)

Usage
=====

Mash user commands
==================

The mash user account is the authentication mechanism of a user against the mash server. It will store information about cloud framework specific account information. The cloud framework account information stored for a given mash user provides the credentials necessary for mash to access a cloud framework account.

`mash user create`

Create a mash user account.

`mash user delete`

Delete a mash user account.

`mash user info`

List information about your user account.


Mash authentication commands
============================

Authentication command are used after a mash user has been created

`mash auth login`

Login to the mash user account

`mash auth logout`

Log out of the mash user account

`mash auth token`

Manage the authentication token


Mash cloud account commands
===========================

`mash account <framework> add`

Add cloud framework account information to the mash user account. Supported <framework>s are azure, ec2, and gce.

`mash account <framework> delete`

Remove cloud framework account information from the mash user account.

`mash account <framework> info`

Retrieve cloud framework account information from the mash user account.

`mash account <framework> list`

List all the framework accounts configured for the mash user.

`mash account <framework> update`

Update information for a cloud framework account for the mash user.


Mash job commands
=================

`mash job <framework> add [PATH_TO_JOB_DOC]`

Send a job request to the mash server submitting the specified job document.
The job document will be validated and a UUID is returned if the job is accepted.

`mash job delete`

Delete a job from the mash server. If the job is a one time job parts of the job may already be executed and created artifacts are not cleaned up.

`mash job info`

Retrieve information about a given job in the pipeline.

`mash job list`

List all the user's job in the mash pipeline.

All commands and subcommands support the `--help` option to provide command help. For example

`mash account azure add --help`

Issues/Enhancements
===================

Please submit issues and requests to
[Github](https://github.com/SUSE-Enceladus/mash-client/issues).

Contributing
============

Contributions to **mash-client** are welcome and encouraged. See
[CONTRIBUTING](https://github.com/SUSE-Enceladus/mash-client/blob/master/CONTRIBUTING.md)
for info on getting started.

License
=======

Copyright (c) 2019 SUSE LLC.

Distributed under the terms of GPL-3.0+ license, see
[LICENSE](https://github.com/SUSE-Enceladus/mash-client/blob/master/LICENSE)
for details.
