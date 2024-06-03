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

%define python python
%{?sle15_python_module_pythons}

Name:           mash-client
Version:        4.2.1
Release:        0
Summary:        Command line utility for MASH server
License:        GPL-3.0-or-later
Group:          Development/Languages/Python
URL:            https://github.com/SUSE-enceladus/mash-client
Source:         https://files.pythonhosted.org/packages/source/p/mash-client/%{name}-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  fdupes
BuildRequires:  python311-devel
BuildRequires:  python311-setuptools
BuildRequires:  python311-wheel
BuildRequires:  python311-pip
BuildRequires:  python311-click
BuildRequires:  python311-click-man
BuildRequires:  python311-requests
BuildRequires:  python311-PyYAML
BuildRequires:  python311-PyJWT
Requires:       python311-click
Requires:       python311-requests
Requires:       python311-PyYAML
Requires:       python311-PyJWT
BuildArch:      noarch

%description
mash-client provides a command line utility to interface
with a MASH server instance.

%prep
%setup -q

%build
%pyproject_wheel
mkdir -p man/man1
%python_exec setup.py --command-packages=click_man.commands man_pages --target man/man1

%install
%pyproject_install

install -d -m 755 %{buildroot}/%{_mandir}/man1
install -d -m 755 %{buildroot}/%{_mandir}/man5
install -m 644 man/man1/*.1 %{buildroot}/%{_mandir}/man1
install -m 644 man/man5/*.5 %{buildroot}/%{_mandir}/man5
gzip %{buildroot}/%{_mandir}/man1/*
gzip %{buildroot}/%{_mandir}/man5/*
%{python_expand %fdupes %{buildroot}%{$python_sitelib}}

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGES.md CONTRIBUTING.md README.md
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_bindir}/mash
%{python_sitelib}/*

%changelog
