#
# spec file for package qmail-autoresponder (Version 0.96.2)
# 
# Copyright  (c)  2006 - 2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# 

%define name	qmail-autoresponder
%define version	0.96.2
%define release	1

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	UNIX-domain socket client-server command-line tools
License:	GPL
Group:		Productivity/Networking/Email/Utilities
Source:		http://untroubled.org/qmail-autoresponder/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%(id -nu)
URL:		http://untroubled.org/qmail-autoresponder/
BuildRequires:	bglibs >= 1.006

%description
This package contains a program to provide automatic rate limited email
responses from qmail.

Author:
-------
    Bruce Guenter <bruceg@em.ca>

%debug_package

%package mysql
Summary:	MySQL-based Autoresponder for qmail
Group:		Productivity/Networking/Email/Utilities
BuildRequires:	mysql-devel

%description mysql
This package contains a program to provide automatic rate limited email
responses from qmail, based entirely on a MySQL database.

%prep
%setup

%build
echo "gcc -g %{optflags}" >conf-cc
echo "gcc -lz %{optflags}" >conf-ld
echo %{_libdir}/bglibs >conf-bglibs
echo %{_includedir}/bglibs >conf-bgincs
%{__make}

%install
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_mandir}
echo %{buildroot}%{_bindir} >conf-bin
echo %{buildroot}%{_mandir} >conf-man
%{__rm} -f conf_bin.c conf_man.c insthier.o installer instcheck
%{__make} installer instcheck
./installer
./instcheck

%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING README procedure.txt
%{_bindir}/qmail-autoresponder
%{_mandir}/man*/*

%files mysql
%doc schema.mysql
%{_bindir}/qmail-autoresponder-mysql

%changelog
* Thu Mar 06 2008 Bernhard Graf <graf@movingtarget.de>
- RPM group complies to openSUSE conventions
- add schema.mysql to docs
* Wed Jan 08 2006 Bernhard Graf <graf@movingtarget.de>
- Updated to release of 0.96.2
* Tue Apr 26 2005 Marko Piatkowski <piatkowski@adjoli.de>
- Initial release of 0.96.1
