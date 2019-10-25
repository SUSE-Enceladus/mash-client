Configuration
=============

MASH Client uses a YAML configuration file. The default path for the
configuration file is *~/.config/mash_client/default.yaml*.

This location can be configured with each command using the *-C/--config-dir*
option. For example::

    mash --config-dir ~/new/dir/ job ...

You can create multiple config files by using the *--profile* option.
For exmample::

    mash --profile prod job ...

Will use the following configuration file: *~/.config/mash_client/prod.yaml*.

Options
-------

The following options are currently available in the configuration file:

*host*
  Hostname of the MASH Server API. Example *http://127.0.0.1*

*port*
  Port where the API is being served. Example *5000*

*log_level*
  Python log level. See Python docs_ for level values.

*no_color*
  If set to *True* removes ANSI color and styling from output.

*verify*
  Verify SSL Certificate. This is *True* by default. Can be *True*,
  *False* or a */path/to/certfile/* used in verification.

*profile*
  The configuration profile to use. Expected to match a
  config file in config directory. Example: production,
  for *~/.config/mash_client/production.yaml*.

.. _docs: https://docs.python.org/3/library/logging.html#levels
