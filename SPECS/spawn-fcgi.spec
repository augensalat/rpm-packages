#
# spec file for package spawn-fcgi (Version 1.6.3)
#
# Copyright  (c)  2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name	spawn-fcgi
%define version	1.6.3
%define release	0

Name:           %{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:        Spawn FastCGI applications independent of the webserver
License:        BSD 3-Clause
Group:          Productivity/Networking/Web/Servers
URL:            http://redmine.lighttpd.net/projects/spawn-fcgi/
Source:         http://www.lighttpd.net/download/spawn-fcgi-%{version}.tar.bz2
BuildRequires:	c_compiler make
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
spawn-fcgi is used to spawn FastCGI applications independent of the webserver.

Authors:
---------
    Jan Kneschke
    Stefan Buehler

%prep
%setup

%build
%configure
%{__make}

%install
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%{__make} install DESTDIR=%{buildroot}

%clean
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_bindir}/spawn-fcgi
%{_mandir}/man1/spawn-fcgi.1*

%changelog
* Tue Nov 03 2009 graf@movingtarget.de 1.6.3-0
- initial package
