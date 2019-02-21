[![Build Status](https://travis-ci.com/SUSE-Enceladus/mash-client.svg?branch=master)](https://travis-ci.com/SUSE-Enceladus/mash-client)
[![Documentation Status](https://readthedocs.org/projects/mash-client/badge/?version=latest)](https://mash-client.readthedocs.io/en/latest/?badge=latest)
[![Py Versions](https://img.shields.io/pypi/pyversions/mash-client.svg)](https://pypi.org/project/mash-client/)
[![License](https://img.shields.io/pypi/l/mash-client.svg)](https://pypi.org/project/mash-client/)

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

# [Docs](https://mash-client.readthedocs.io/en/latest/)

Usage
=====

The client has the following endpoints:

`mash job add`

Send add job request to mash server based on provided json document.

`mash job delete`

Delete a job given the UUID.

`mash account add azure`
`mash account add ec2`
`mash account add gce`

Add account based on cloud framework.

`mash account delete`

Delete mash account.

To get more info on an endpoint use the `--help` option:

`mash account add azure --help`

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
