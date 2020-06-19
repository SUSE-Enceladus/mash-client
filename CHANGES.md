v3.1.0 (2020-06-19)
===================

- Fix typo in spec for config man page.
  [\65](https://github.com/suse-enceladus/mash-client/pull/65)
- Improvements to config file setup.
  [\66](https://github.com/suse-enceladus/mash-client/pull/66)
- Handle errors from OIDC provider.
  [\67](https://github.com/suse-enceladus/mash-client/pull/67)
- Add border on div and change color on status.
  [\68](https://github.com/suse-enceladus/mash-client/pull/68)
- Add option for job dry run.
  [\70](https://github.com/suse-enceladus/mash-client/pull/70)

v3.0.0 (2020-04-20)
===================

- Add OpenID Connect authentication support.
  [\52](https://github.com/suse-enceladus/mash-client/pull/52)
- Remove username, email is now primary key for user.
  [\55](https://github.com/suse-enceladus/mash-client/pull/55)
- Add commands for password change and reset.
  [\58](https://github.com/suse-enceladus/mash-client/pull/58)
- Add new commands for setup and echo client config.
  [\60](https://github.com/suse-enceladus/mash-client/pull/60)
- Provide useful msg if config file not found.
  [\61](https://github.com/suse-enceladus/mash-client/pull/61)
- Add man page text for configuration file creation.
  [\62](https://github.com/suse-enceladus/mash-client/pull/62)
- Add API to retrieve job doc examples.
  [\63](https://github.com/suse-enceladus/mash-client/pull/63)
- Cleanup (remove) group options in azure and gce accounts.
  [\64](https://github.com/suse-enceladus/mash-client/pull/64)

v2.1.0 (2020-02-24)
===================

- Integrate OCI cloud framework into mash pipeline.
  [\51](https://github.com/suse-enceladus/mash-client/pull/51)

v2.0.0 (2019-12-20)
===================

- Update the configuration docs with profile.
  [\46](https://github.com/suse-enceladus/mash-client/pull/46)
- Update README to reflect the latest command line interface.
  [\47](https://github.com/suse-enceladus/mash-client/pull/47)
- Remove group option from gce and azure accounts.
  [\49](https://github.com/suse-enceladus/mash-client/pull/49)
- Remove man pages from source.
  [\50](https://github.com/suse-enceladus/mash-client/pull/50)

v1.1.0 (2019-10-25)
===================

- Add coverage to travis testing.
  [\42](https://github.com/suse-enceladus/mash-client/pull/42)
- Add profiles option to handle multiple configs.
  [\43](https://github.com/suse-enceladus/mash-client/pull/43)
- Add comment to delete confirmation about updates.
  [\44](https://github.com/suse-enceladus/mash-client/pull/44)
- Fix account list routes.
  [\45](https://github.com/suse-enceladus/mash-client/pull/45)

v1.0.0 (2019-10-02)
===================

- Integrate all endpoints from MASH v4.0.0
- Add authentication to requests
- Split up cli into multiple modules
- Simplify the echo dictionary function

v0.6.0 (2019-08-07)
===================

- Update client for mash server api changes.
  [\21](https://github.com/suse-enceladus/mash-client/pull/21)

v0.5.0 (2019-07-29)
===================

- Add subnet option to ec2 add account.
  [\20](https://github.com/suse-enceladus/mash-client/pull/20)

v0.4.0 (2019-06-08)
===================

- Improve the help message for additional region handling.
  [\16](https://github.com/suse-enceladus/mash-client/pull/16)
- Add is publishing account option for gce accounts.
  [\17](https://github.com/suse-enceladus/mash-client/pull/17)

v0.3.0 (2019-03-08)
===================

- add testing account option for gce account add.
  [\15](https://github.com/suse-enceladus/mash-client/pull/15)

v0.2.0 (2019-02-22)
===================

- Add readthedocs documentation.
  [\11](https://github.com/SUSE-Enceladus/mash-client/pull/11)
- Move default mash client config file.
  [\12](https://github.com/SUSE-Enceladus/mash-client/pull/12)
- Add ec2 account has a single target region.
  [\13](https://github.com/SUSE-Enceladus/mash-client/pull/13)
- Re-word cli option help messages.
  [\14](https://github.com/SUSE-Enceladus/mash-client/pull/14)

v0.1.0 (2019-02-04)
===================

- Update mash job delete.
  [\#5](https://github.com/SUSE-Enceladus/mash-client/pull/5)
- Update account delete.
  [\#6](https://github.com/SUSE-Enceladus/mash-client/pull/6)
- Add integration test suite.
  [\#9](https://github.com/SUSE-Enceladus/mash-client/pull/9)
- Remove references to provider.
  [\#10](https://github.com/SUSE-Enceladus/mash-client/pull/10)

v0.0.2 (2018-11-15)
===================

- Cleanup spec requirements.
  [\#2](https://github.com/SUSE-Enceladus/mash-client/pull/2)
- Handle Azure source and destination storage options.
  [\#3](https://github.com/SUSE-Enceladus/mash-client/pull/3)
- Add GCE add account endpoint.
  [\#4](https://github.com/SUSE-Enceladus/mash-client/pull/4)
- Use required options instead of positional args.
  [\#7](https://github.com/SUSE-Enceladus/mash-client/pull/7)
  [\#8](https://github.com/SUSE-Enceladus/mash-client/pull/8)

v0.0.1 (2018-08-24)
===================

- Initial release.
