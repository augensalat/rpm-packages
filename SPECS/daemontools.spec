#
# spec file for package daemontools (Version 0.76)
#
# Copyright  (c)  2003-2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define package_name    daemontools
%define version         0.76
%define release         7

%define build_dietlibc	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}

Name:           %{package_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	A collection of tools for managing UNIX services
License:	Public Domain
Group:		System/Base
Autoreqprov:	on
Source0:	http://cr.yp.to/daemontools/daemontools-%{version}.tar.gz
Source1:	http://smarden.org/pape/djb/manpages/daemontools-%{version}-man.tar.gz
Patch0:		daemontools-%{version}-src.patch
Patch1:		daemontools-%{version}-package.patch
Patch2:		http://www.thedjbway.org/patches/daemontools-%{version}.sigq12.patch
BuildRoot:	%{_tmppath}/daemontools-%{version}-%(id -nu)
BuildRequires:	c_compiler make patch binutils coreutils grep
%if %{build_dietlibc}
BuildRequires:	dietlibc >= 0.30
%endif
Requires:	bash
URL:		http://cr.yp.to/daemontools.html

%description
daemontools is a collection of tools for managing UNIX services. 

supervise monitors a service. It starts the service and restarts the
service if it dies. Setting up a new service is easy: all supervise
needs is a directory with a run script that runs the service.

multilog saves error messages to one or more logs. It optionally
timestamps each line and, for each log, includes or excludes lines
matching specified patterns. It automatically rotates logs to limit the
amount of disk space used. If the disk fills up, it pauses and tries
again, without losing any data.

This RPM package doesn't comply to Dan Bernstein's filesystem layout
definitions (http://cr.yp.to/unix.html), but instead tries to integrate
into a (SuSE) FHS compatible filesystem.

Author:
-------
    Dan J. Bernstein <djb@cr.yp.to>

%debug_package

%prep
%setup -T -b 1 -n daemontools-man
%setup -n admin/daemontools-0.76
%patch0
%patch1
%patch2 -p1
%if %{build_dietlibc}
echo diet cc $RPM_OPT_FLAGS >src/conf-cc
echo diet cc>src/conf-ld
%else
echo cc $RPM_OPT_FLAGS >conf-cc
echo cc >conf-ld
%endif

%build
package/compile

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}/service
%{__mkdir_p} %{buildroot}/sbin
%{__mkdir_p} %{buildroot}%{_mandir}/man8
%{__cp} -f command/* %{buildroot}/sbin
%{__cp} -f ../../daemontools-man/*.8 %{buildroot}%{_mandir}/man8
%{__cp} src/[CT]* .
%{__cp} ../../daemontools-man/README README.manpages
%{__mkdir_p} %{buildroot}%{_sysconfdir}/env

%{__install} -d -m 0755 %{buildroot}/etc/service
%{__install} -d -m 0755 %{buildroot}/etc/service/expireproctitle
%{__cat} <<EOT >%{buildroot}/etc/service/expireproctitle/run
#!/bin/sh
echo -n .
exec sleep 900
EOT
%{__chmod} 0755 %{buildroot}/etc/service/expireproctitle/run
%{__ln_s} ../etc/service/expireproctitle %{buildroot}/service/expireproctitle

# %{__rm} -rf CHANGES TODO README.manpages

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%preun
if test "$1" = 0 ; then
  svc -dx /service/* /service/*/log >/dev/null 2>&1
  sleep 5
  rm -rf /etc/service/expireproctitle/supervise
fi

%files
%defattr(-,root,root)
%doc CHANGES TODO README.manpages
%attr(0775,-,-) %dir %{_sysconfdir}/env
%attr(0775,-,-) /sbin/*
%{_mandir}/man*/*
%attr(0775,-,-) %dir /etc/service
%attr(0775,-,-) %dir /etc/service/expireproctitle
%attr(0775,-,-) /etc/service/expireproctitle/run
%attr(0775,-,-) %dir /service
/service/expireproctitle

%changelog
* Thu Feb 21 2008 Bernhard Graf <graf@movingtarget.de> 0.76-7
- optionally link with dietlibc (--with dietlibc)
- build debug package

* Tue Jan 29 2008 Bernhard Graf <graf@movingtartget.de>
- adjusted RPM group according to SuSE specs
- added expireproctitle service

* Tue Jan 22 2008 Bernhard Graf <graf@movingtarget.de>
- added directory /etc/env to give all packages bases on daemontools a
  home for their envdir files: /etc/env/application/*
- patch http://www.thedjbway.org/patches/daemontools-0.76.sigq12.patch

* Wed May 07 2003 Bernhard Graf <graf@movingtarget.de>
- for SuSE >8.0
- extended fhs-patch to make package compile with gcc 3.2 (errno issue)

* Mon Aug 6 2001 Bernhard Graf <graf@augensalat.de>
- Updated to version 0.76.

* Thu May 5 2001 Bruce Guenter <bruceg@em.ca>
- Added a hack to allow building on glibc 2.2 systems (such as RedHat 7.x)

* Fri Dec 1 2000 Bruce Guenter <bruceg@em.ca>
- Reverted to a completely plain, unmodified install.

* Mon Mar 6 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.70.

* Mon Dec 6 1999 Bruce Guenter <bruceg@em.ca>
- Modified svscan init script to start all services as "down" on
  startup, and to clean up properly on exit.
- Removed /var/lock/svc directory.
