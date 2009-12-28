#
# spec file for package greylite (Version 2.3)
#
# Copyright  (c)  2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name	greylite
%define version	2.3
%define release	1

%define build_dietlibc	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}
%{?_with_ssl: %{expand: %%define build_ssl 1}}

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Greylisting for qmail
License:	BSD
Group:		Productivity/Networking/Email/Utilities
Source:		http://mij.oltrelinux.com/net/greylite/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}-suspicion
Patch:		%{name}-%{version}.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -u -n)
BuildRequires:	c_compiler make binutils coreutils
BuildRequires:	libGeoIP-devel libcares-devel >= 1.5 sqlite-devel >= 3
%if %{build_dietlibc}
BuildRequires:	dietlibc >= 0.30
%endif
Requires:	qmail
PreReq:		sqlite >= 3
URL:		http://cr.yp.to/ucspi-tcp.html

%description
Greylite is a SPAM filter with exceptional effectiveness and without false
positives. It combines natively with qmail and works as a proxy for any
SMTP server.

Greylite implements a modified greylisting algorithm that improves the
filtering effectiveness and minimizes the delay drawbacks associated with
the standard greylisting algorithm.

Author:
-------
    Michele Mazzucchi <mij@bitchx.it>

%debug_package

%prep
%setup
%patch

%build
%{__make} WITH_GEOIP=yes WITH_DNSBLENV=yes all

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sbindir}
%{__mkdir_p} %{buildroot}%{_mandir}/man8
%{__mkdir_p} %{buildroot}%{_var}/lib/%{name}
%{__install} -m 0755 greylite %{buildroot}%{_sbindir}
%{__install} -m 0755 dnsblenv %{buildroot}%{_sbindir}
%{__install} -m 0644 greylite.8 %{buildroot}%{_mandir}/man8
echo .quit | sqlite3 -batch -init greydb.sql %{buildroot}%{_var}/lib/%{name}/greylite.db
%{__install} -m 0644 %{S:1} %{buildroot}%{_var}/lib/%{name}/suspicion

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes README greydb.sql
%{_mandir}/man8/*
%attr(0755,qmaild,nogroup) %dir %{_var}/lib/%{name}
%attr(0644,qmaild,nogroup) %config(noreplace,missingok) %verify(not md5 size mtime) %{_var}/lib/%{name}/greylite.db
%attr(0644,root,root) %config(noreplace,missingok) %verify(not md5 size mtime) %{_var}/lib/%{name}/suspicion
%attr(0755,-,-) %{_sbindir}/*

%changelog
* Fri Mar 07 2008 Bernhard Graf <graf@movingtarget.de> 2.3-1
- default suspicion file added
* Thu Mar 06 2008 Bernhard Graf <graf@movingtarget.de> 2.3-0
- initial install
