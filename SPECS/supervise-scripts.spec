#
# spec file for package supervise-scripts (Version 3.5)
#
# Copyright  (c)  2003-2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define package_name    supervise-scripts
%define version         4.0
%define release         0

Name:           %{package_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Utility scripts for use with supervise and svscan.
License:	GPL
Group:		System/Base
Source:		http://untroubled.org/supervise-scripts/%{name}-%{version}.tar.gz
Patch:		%{name}-%{version}.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -nu)
URL:		http://untroubled.org/supervise-scripts/
Requires:	daemontools >= 0.76 coreutils grep
BuildArch:	noarch

%description
A set of scripts for handling programs managed with supervise and svscan.

%prep
%setup
%patch

%build
echo /sbin >conf-bin
echo %{_mandir} >conf-man
%{__make} programs

%install
test "%{buildroot}" != "/" && test -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}/sbin
%{__install} -d %{buildroot}%{_mandir}
%{__install} -d -m 0755 %{buildroot}/var/service

%{__make} PREFIX=%{buildroot} install

%post
/sbin/svscan-add-to-inittab

%clean
test "%{buildroot}" != "/" && test -d %{buildroot} && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING NEWS README
%attr(0775,-,-) /sbin/*
%{_mandir}/man*/*
%attr(0775,-,-) %dir /var/service

%changelog
* Sun Apr 04 2010 Bernhard Graf <graf@movingtartget.de>
- upgraded to version 4.0
* Tue Jan 29 2008 Bernhard Graf <graf@movingtartget.de>
- adjusted RPM group according to SuSE specs
* Thu Jan 27 2005 Bernhard Graf <graf@movingtartget.de>
- removed %dir /service from %files
- added BuildRequires: bglibs >= 1.011
* Sat Dec 27 2003 Bernhard Graf <graf@movingtartget.de>
- returned to use svscanboot instead of svscan-start in /etc/inittab
* Tue Nov 18 2003 Bernhard Graf <graf@movingtartget.de>
- updated to v3.5
* Wed May 07 2003 Bernhard Graf <graf@movingtartget.de>
- Really use /service instead of /etc/service
* Thu Jun 27 2002 Bernhard Graf <graf@adjoli.de>
- bumped to version 3.4
* Wed Feb 13 2002 Bernhard Graf <graf@adjoli.de>
- re-inserted svscan-stopall into inittab
* Tue Aug 07 2001 Bernhard Graf <graf@augensalat.de>
- updated to daemontools 0.75
- change paths to comply with FHS and my own daemontools RPM

