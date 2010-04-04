#
# spec file for package cvm (Version 0.96)
#
# Copyright  (c)  2002-2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name		cvm
%define initname	%{name}-init
%define version		0.96
%define initversion	%{version}
%define release		0

%if 0%{?suse_version} > 1020
%define with_susefirewall_config 1
%endif

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Credential Validation Modules
License:	GPL
Group:		System/Base
Source:		http://untroubled.org/cvm/%{name}-%{version}.tar.gz
Source1:	%{initname}-%{initversion}.tar.bz2
Source2:	cvm-SuSEfirewall-0.01.tar.bz2
Patch:		%{name}-%{version}-legacy-include.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -nu)
PreReq:		%fillup_prereq /bin/cat /bin/mkdir /bin/touch /bin/chown /bin/chmod
BuildRequires:	coreutils filesystem fileutils fillup make c_compiler libtool
BuildRequires:	bglibs >= 1.103 mysql-devel postgresql-devel
Requires:	bglibs >= 1.103
Obsoletes:	cvm-vmailmgr cvm-qmail
URL:		http://untroubled.org/cvm/

%description
This package implements the CVM interface as a client (cvm-testclient),
and as a module (cvm-unix, cvm-pwfile).

%debug_package

%package devel
Summary:	Development libraries for CVM
Group:		Development/Libraries/Other
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description devel
This package includes all the development libraries and headers for
building CVM clients or modules.

%package mysql
Group:		System/Base
Summary:	MySQL Credential Validation Modules
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description mysql
Credential Validation Modules that authenticate against a MySQL server.

%package pgsql
Group:		System/Base
Summary:	PostgreSQL Credential Validation Modules
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description pgsql
Credential Validation Modules that authenticate against a PostgreSQL server.

%package qmail-local
Group:		Utilities/System
Summary:	qmail configuration lookup module
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3

%description qmail-local
This module uses the standard qmail configuration files to determine if an
address is valid, using the same lookups that qmail would.
CVM module on a UNIX domain socket.

%package qmail-udp
Group:		Utilities/System
Summary:	qmail configuration lookup module
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3

%description qmail-udp
This module uses the standard qmail configuration files to determine if an
address is valid, using the same lookups that qmail would.
CVM module on a UDP socket.

%package vmailmgr-local
Group:		Utilities/System
Summary:	CVM modules for vmailmgr
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3

%description vmailmgr-local
CVM authentication for and lookup of vmailmgr accounts.
One CVM authentication and one CVM lookup module on UNIX domain sockets.

%package vmailmgr-udp
Group:		Utilities/System
Summary:	CVM modules for vmailmgr
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3

%description vmailmgr-udp
CVM authentication for and lookup of vmailmgr accounts.
One CVM authentication and one CVM lookup module on UDP sockets.

%prep
%setup -q -a 1 -a 2
%patch
echo 'gcc %{optflags} -I"%{_includedir}/bglibs" -I"%{_includedir}/pgsql"' >conf-cc
echo 'gcc -lm -lz -L"%{_libdir}/bglibs" -L"%{_libdir}/mysql"' >conf-ld
echo %{_bindir} >conf-bin
echo %{_includedir} >conf-include
echo %{_libdir} >conf-lib

%build
%{__make} libraries programs mysql pgsql

%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%{__mkdir} -p %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{_includedir}
%{__mkdir} -p %{buildroot}%{_libdir}

%{__make} install_prefix=%{buildroot} install

# fix for SuSE x86_64 
#if test "%{_libdir}" != "%{_prefix}/lib"; then
#  mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
#fi

%{__install} -d -m 0755 %{buildroot}%{_sbindir}
(
  cd %{initname}-%{initversion} && \
  %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
	sysconfdir=%{_sysconfdir} \
	fillupdir=%{_var}/adm/fillup-templates \
	permissionsdir=%{_sysconfdir}/permissions.d \
	install
)
for n in qmail-local qmail-udp vmailmgr-local vmailmgr-udp ; do
  %{__ln_s} ../../etc/init.d/cvm-$n %{buildroot}%{_sbindir}/rccvm-$n
done

%if 0%{?with_susefirewall_config}
  (
    cd cvm-SuSEfirewall-0.01
    %{__make} DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} install
  )
%endif

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%post
%{fillup_only}
/sbin/ldconfig

%postun
/sbin/ldconfig

%post qmail-local
test -e /var/qmail/control/virtualdomains || touch /var/qmail/control/virtualdomains
if test -L /service/cvm-qmail-local -a -x /service/cvm-qmail-local/run ; then
  pushd >/dev/null /service/cvm-qmail-local
  %{__rm} /service/cvm-qmail-local
  svc -dx . log
  popd >/dev/null
fi
%{fillup_only -ans cvm qmail-local}
%{fillup_and_insserv -fy}

%{__ln_s} %{_sysconfdir}/cvm-qmail-local /service/cvm-qmail-local

%preun qmail-local
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove services
if test -L /service/cvm-qmail-local ; then
  pushd >/dev/null /service/cvm-qmail-local
  %{__rm} /service/cvm-qmail-local
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/cvm-qmail-local/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-qmail-local/log/supervise || :

%postun qmail-local
%{insserv_cleanup}

%post qmail-udp
test -e /var/qmail/control/virtualdomains || touch /var/qmail/control/virtualdomains
if test -L /service/cvm-qmail-udp -a -x /service/cvm-qmail-udp/run ; then
  pushd >/dev/null /service/cvm-qmail-udp
  %{__rm} /service/cvm-qmail-udp
  svc -dx . log
  popd >/dev/null
fi
%{fillup_only -ans cvm qmail-udp}
%{fillup_and_insserv -fy}

%{__ln_s} %{_sysconfdir}/cvm-qmail-udp /service/cvm-qmail-udp

%preun qmail-udp
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove services
if test -L /service/cvm-qmail-udp ; then
  pushd >/dev/null /service/cvm-qmail-udp
  %{__rm} /service/cvm-qmail-udp
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/cvm-qmail-udp/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-qmail-udp/log/supervise || :

%postun qmail-udp
%{insserv_cleanup}

%post vmailmgr-local
test -e /var/qmail/control/virtualdomains || touch /var/qmail/control/virtualdomains
if test -L /service/cvm-vmailmgr-local -a -x /service/cvm-vmailmgr-local/run ; then
  pushd >/dev/null /service/cvm-vmailmgr-local
  %{__rm} /service/cvm-vmailmgr-local
  svc -dx . log
  popd >/dev/null
fi
if test -L /service/cvm-vmlookup-local -a -x /service/cvm-vmlookup-local/run ; then
  pushd >/dev/null /service/cvm-vmlookup-local
  %{__rm} /service/cvm-vmlookup-local
  svc -dx . log
  popd >/dev/null
fi
%{fillup_only -ans cvm vmailmgr-local}
%{fillup_and_insserv -fy}

%{__ln_s} %{_sysconfdir}/cvm-vmailmgr-local /service/cvm-vmailmgr-local
%{__ln_s} %{_sysconfdir}/cvm-vmlookup-local /service/cvm-vmlookup-local

%preun vmailmgr-local
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove services
if test -L /service/cvm-vmailmgr-local ; then
  pushd >/dev/null /service/cvm-vmailmgr-local
  %{__rm} /service/cvm-vmailmgr-local
  svc -dx . log
  popd >/dev/null
fi
if test -L /service/cvm-vmlookup-local ; then
  pushd >/dev/null /service/cvm-vmlookup-local
  %{__rm} /service/cvm-vmlookup-local
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/cvm-vmailmgr-local/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmailmgr-local/log/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmlookup-local/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmlookup-local/log/supervise || :

%postun vmailmgr-local
%{insserv_cleanup}

%post vmailmgr-udp
test -e /var/qmail/control/virtualdomains || touch /var/qmail/control/virtualdomains
if test -L /service/cvm-vmailmgr-udp -a -x /service/cvm-vmailmgr-udp/run ; then
  pushd >/dev/null /service/cvm-vmailmgr-udp
  %{__rm} /service/cvm-vmailmgr-udp
  svc -dx . log
  popd >/dev/null
fi
if test -L /service/cvm-vmlookup-udp -a -x /service/cvm-vmlookup-udp/run ; then
  pushd >/dev/null /service/cvm-vmlookup-udp
  %{__rm} /service/cvm-vmlookup-udp
  svc -dx . log
  popd >/dev/null
fi
%{fillup_only -ans cvm vmailmgr-udp}
%{fillup_and_insserv -fy}

%{__ln_s} %{_sysconfdir}/cvm-vmailmgr-udp /service/cvm-vmailmgr-udp
%{__ln_s} %{_sysconfdir}/cvm-vmlookup-udp /service/cvm-vmlookup-udp

%preun vmailmgr-udp
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove services
if test -L /service/cvm-vmailmgr-udp ; then
  pushd >/dev/null /service/cvm-vmailmgr-udp
  %{__rm} /service/cvm-vmailmgr-udp
  svc -dx . log
  popd >/dev/null
fi
if test -L /service/cvm-vmlookup-udp ; then
  pushd >/dev/null /service/cvm-vmlookup-udp
  %{__rm} /service/cvm-vmlookup-udp
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/cvm-vmailmgr-udp/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmailmgr-udp/log/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmlookup-udp/supervise || :
%{__rm} -fr %{_sysconfdir}/cvm-vmlookup-udp/log/supervise || :

%postun vmailmgr-udp
%{insserv_cleanup}

%files
%defattr(-,root,root)
%doc COPYING NEWS README *.html
%attr(0755,root,root) %{_bindir}/cvm-[^mp]*
%attr(0755,root,root) %{_bindir}/cvm-pwfile
%attr(0644,root,root) %{_sysconfdir}/permissions.d/cvm
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.cvm
%attr(0644,root,root) %{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_includedir}/cvm
%attr(0644,root,root) %{_includedir}/cvm/*
%attr(0644,root,root) %{_includedir}/cvm-sasl.h
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_libdir}/*.la
%{_libdir}/*.so

%files mysql
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/cvm-mysql*

%files pgsql
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/cvm-pgsql*

%files qmail-local
%defattr(-,root,root)
%attr(0754,root,root) /etc/init.d/cvm-qmail-local
%{_sbindir}/rccvm-qmail-local
%attr(0644,root,root) %{_sysconfdir}/permissions.d/cvm-qmail-local
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-qmail-local
%attr(0750,root,root) %dir %{_sysconfdir}/cvm-qmail-local/env
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-qmail-local/log
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-qmail-local/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-qmail-local/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-qmail-local/env/*
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-qmail-local
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-qmail-local
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.cvm-qmail-local
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-qmail-local

%files qmail-udp
%defattr(-,root,root)
%attr(0754,root,root) /etc/init.d/cvm-qmail-udp
%{_sbindir}/rccvm-qmail-udp
%attr(0644,root,root) %{_sysconfdir}/permissions.d/cvm-qmail-udp
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-qmail-udp
%attr(0750,root,root) %dir %{_sysconfdir}/cvm-qmail-udp/env
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-qmail-udp/log
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-qmail-udp/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-qmail-udp/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-qmail-udp/env/*
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/cvm-qmail-udp
%endif
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-qmail-udp
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-qmail-udp
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.cvm-qmail-udp
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-qmail-udp

%files vmailmgr-local
%defattr(-,root,root)
%attr(0754,root,root) /etc/init.d/cvm-vmailmgr-local
%{_sbindir}/rccvm-vmailmgr-local
%attr(0644,root,root) %{_sysconfdir}/permissions.d/cvm-vmailmgr-local
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-local
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-vmlookup-local
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-local/env
%attr(0750,root,root) %dir %{_sysconfdir}/cvm-vmlookup-local/env
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-local/log
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmlookup-local/log
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmailmgr-local/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmlookup-local/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmailmgr-local/log/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmlookup-local/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-vmailmgr-local/env/*
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-vmlookup-local/env/*
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-vmailmgr-local
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-vmailmgr-local
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-vmlookup-local
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-vmlookup-local
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.cvm-vmailmgr-local
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-vmailmgr-local
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-vmlookup-local

%files vmailmgr-udp
%defattr(-,root,root)
%attr(0754,root,root) /etc/init.d/cvm-vmailmgr-udp
%{_sbindir}/rccvm-vmailmgr-udp
%attr(0644,root,root) %{_sysconfdir}/permissions.d/cvm-vmailmgr-udp
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-udp
%attr(1755,root,root) %dir %{_sysconfdir}/cvm-vmlookup-udp
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-udp/env
%attr(0750,root,root) %dir %{_sysconfdir}/cvm-vmlookup-udp/env
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmailmgr-udp/log
%attr(0755,root,root) %dir %{_sysconfdir}/cvm-vmlookup-udp/log
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmailmgr-udp/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmlookup-udp/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmailmgr-udp/log/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/cvm-vmlookup-udp/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-vmailmgr-udp/env/*
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/cvm-vmlookup-udp/env/*
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/cvm-vmailmgr-udp
%endif
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-vmailmgr-udp
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-vmailmgr-udp
%attr(0750,root,root) %{_prefix}/share/cvm/create-config-cvm-vmlookup-udp
%attr(0750,root,root) %{_prefix}/share/cvm/create-log-config-cvm-vmlookup-udp
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.cvm-vmailmgr-udp
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-vmailmgr-udp
%attr(0755,nobody,nobody) %dir %{_var}/log/cvm-vmlookup-udp


%changelog
* Sun Apr 04 2010 Bernhard Graf <graf@movingtarget.de>
- updated to version 0.96
* Tue Nov 03 2009 Bernhard Graf <graf@movingtarget.de>
- updated to version 0.95
* Mon Nov 03 2008 Bernhard Graf <graf@movingtarget.de>
- updated to version 0.90
* Wed Mar 05 2008 Bernhard Graf <graf@movingtarget.de>
- small fixes in cvm-lookup run files
- spec file bug fix where fillup was not found after a `cd'
* Fri Feb 29 2008 Bernhard Graf <graf@movingtarget.de>
- refactored configuration file layout
- split local socket and udp socket daemons into their own packages
- removed SuSEconfig configuration setup - configuration is now created
  when the service is started
- automatically open SuSEfirewall for the respective daemons on SuSE >=10.3
* Sun Jan 20 2008 Bernhard Graf <graf@movingtarget.de>
- added patch, see
  http://lists.untroubled.org/?list=bgware&cmd=showthread&threadid=jcpdhdfoaijolgdonpio
* Fri Jan 18 2008 Bernhard Graf <graf@movingtarget.de>
- upgraded to version 0.82
* Mon Sep 19 2005 Bernhard Graf <graf@movingtarget.de>
- upgraded to version 0.76
* Wed Mar 30 2005 Bernhard Graf <graf@movingtarget.de>
- patch for cvm-qmail module ("." to ":" conversion)
- build fix for x86_64 systems
* Sun Jan 30 2005 Bernhard Graf <graf@movingtarget.de>
- updated to v0.32
- separate packages for qmail, MySQL, PostgreSQL and vmailmgr modules
* Tue Dec 16 2003 Bernhard Graf <graf@movingtarget.de>
- updated to v0.18
* Mon Aug 18 2003 Bernhard Graf <graf@adjoli.de>
- updated to v0.17
- separated devel package
* Sat Jan 12 2002 Bernhard Graf <graf@adjoli.de>
- first package release for adjoli/SuSE
