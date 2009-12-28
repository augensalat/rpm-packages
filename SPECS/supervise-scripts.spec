#
# spec file for package supervise-scripts (Version 3.5)
#
# Copyright  (c)  2003-2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define package_name    supervise-scripts
%define version         3.5
%define release         5
%global build_mandrake  %([ -e /etc/mandrake-release ]; echo $[1-$?])
%global build_suse      %([ -e /etc/SuSE-release ]; echo $[1-$?])

Name:           %{package_name}
Version:        %{version}
%if %build_mandrake
Release:        %{release}mdk
Distribution:   %(head -n1 /etc/mandrake-release)
%elseif %build_suse
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
%else
Release:        %{release}
%endif
Summary:	Utility scripts for use with supervise and svscan.
License:	GPL
Group:		System/Base
Source:		http://untroubled.org/supervise-scripts/%{name}-%{version}.tar.gz
Patch:		%{name}-%{version}.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -u -n)
URL:		http://untroubled.org/supervise-scripts/
Packager:	Bernhard Graf <graf@movingtarget.de>
Requires:	daemontools >= 0.75 binutils coreutils grep
BuildRequires:	bglibs >= 1.011

%description
A set of scripts for handling programs managed with supervise and svscan.

%prep
%setup
%patch

%build
echo /sbin >conf-bin
echo %{_mandir} >conf-man
echo %{_libdir}/bglibs >conf-bglibs
echo %{_includedir}/bglibs >conf-bgincs
%{__make} programs

%install
test "%{buildroot}" != "/" && test -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}/sbin
%{__install} -d %{buildroot}%{_mandir}
%{__install} -d -m 0755 %{buildroot}/var/service

echo %{buildroot}/sbin >conf-bin
echo %{buildroot}%{_mandir} >conf-man
%{__make} installer instcheck
./installer
./instcheck

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

