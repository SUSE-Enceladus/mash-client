#
# spec file for package mash-client
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           mash-client
Version:        0.6.0
Release:        0
Summary:        Command line utility for MASH server
License:        GPL-3.0-or-later
Group:          Development/Languages/Python
URL:            https://github.com/SUSE-enceladus/mash-client
Source:         https://files.pythonhosted.org/packages/source/p/mash-client/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-click
BuildRequires:  python3-requests
BuildRequires:  python3-PyYAML
Requires:       python3-click
Requires:       python3-requests
Requires:       python3-PyYAML
BuildArch:      noarch

%description
mash-client provides a command line utility to interface
with a MASH server instance.

%prep
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -m 644 man/man1/*.1 %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{_mandir}/man1/*

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGES.md CONTRIBUTING.md README.md
%{_mandir}/man1/*
%{_bindir}/mash
%{python3_sitelib}/*

%changelog
