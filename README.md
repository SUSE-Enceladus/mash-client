[![Build Status](https://travis-ci.com/SUSE-Enceladus/mash-client.svg?branch=master)](https://travis-ci.com/SUSE-Enceladus/mash-client)

**mash-client**

overview
========

**mash-client** provides a command line utilty to interface with the
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

Usage
=====

The client has the following endpoints:

`mash job add [OPTIONS] DOCUMENT`

Send add job request to mash server based on provided json document.

`mash job delete [OPTIONS] JOB_ID`

Delete a job given the UUID.

`mash account add ec2 [OPTIONS] ACCOUNT_NAME PARTITION REQUESTING_USER
ACCESS_KEY_ID SECRET_ACCESS_KEY`

Add EC2 account given the provided args.

`mash account add azure [OPTIONS] ACCOUNT_NAME CONTAINER_NAME REGION
REQUESTING_USER RESOURCE_GROUP STORAGE_ACCOUNT CREDENTIALS_PATH`

Add Azure account given the provided args.

`mash account delete [OPTIONS] ACCOUNT_NAME PROVIDER REQUESTING_USER`

Delete account given the provided args.

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

Copyright (c) 2018 SUSE LLC.

Distributed under the terms of GPL-3.0+ license, see
[LICENSE](https://github.com/SUSE-Enceladus/mash-client/blob/master/LICENSE)
for details.
