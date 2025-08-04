#
# spec file for package mash-client
#
# Copyright (c) 2025 SUSE LLC
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

%if 0%{?suse_version} >= 1600
%define pythons %{primary_python}
%else
%{?sle15_python_module_pythons}
%endif
%global _sitelibdir %{%{pythons}_sitelib}

Name:           mash-client
Version:        4.5.0
Release:        0
Summary:        Command line utility for MASH server
License:        GPL-3.0-or-later
Group:          Development/Languages/Python
URL:            https://github.com/SUSE-enceladus/mash-client
Source:         https://files.pythonhosted.org/packages/source/p/mash-client/%{name}-%{version}.tar.gz
BuildRequires:  python-rpm-macros
BuildRequires:  fdupes
BuildRequires:  %{pythons}-devel
BuildRequires:  %{pythons}-setuptools
BuildRequires:  %{pythons}-wheel
BuildRequires:  %{pythons}-pip
BuildRequires:  %{pythons}-click
BuildRequires:  %{pythons}-requests
BuildRequires:  %{pythons}-PyYAML
BuildRequires:  %{pythons}-PyJWT
Requires:       %{pythons}-click
Requires:       %{pythons}-requests
Requires:       %{pythons}-PyYAML
Requires:       %{pythons}-PyJWT
BuildArch:      noarch

%description
mash-client provides a command line utility to interface
with a MASH server instance.

%prep
%setup -q

%build
%pyproject_wheel

%install
%pyproject_install

install -d -m 755 %{buildroot}/%{_mandir}/man1
install -d -m 755 %{buildroot}/%{_mandir}/man5
install -m 644 man/man1/*.1 %{buildroot}/%{_mandir}/man1
install -m 644 man/man5/*.5 %{buildroot}/%{_mandir}/man5
gzip %{buildroot}/%{_mandir}/man1/mash*
gzip %{buildroot}/%{_mandir}/man5/mash*
%fdupes %{buildroot}%{_sitelibdir}

%files
%defattr(-,root,root)
%license LICENSE
%doc CHANGES.md CONTRIBUTING.md README.md
%{_mandir}/man1/mash*
%{_mandir}/man5/mash*
%{_bindir}/mash
%{_sitelibdir}/mash_client/
%{_sitelibdir}/mash_client-*.dist-info/

%changelog
