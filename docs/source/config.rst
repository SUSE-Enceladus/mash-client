Configuration
=============

MASH Client uses a YAML config file. By default the client will look
for a config file at *~/.config/mash_client/config.yaml*.

This location can be configured with each command using the *-C/--config*
option. For example::

    mash --config ~/new/config.yaml job add ...

Options
-------

The following options are currently available in the config file:

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

.. _docs: https://docs.python.org/3/library/logging.html#levels
