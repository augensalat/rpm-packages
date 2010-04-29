#
# spec file for package vmailmgr (Version 0.97)
#
# Copyright  (c)  2005 - 2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name		vmailmgr
%define initname	%{name}-init
%define version		0.97
%define initversion	%{version}
%define release		4
# %define _unpackaged_files_terminate_build 0
%define	cgidir		/srv/www/cgi-bin
%define phpdir		/srv/www/php

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Simple virtualizing POP3/IMAP password interface
License:	GPL
Group:		Productivity/Networking/Email/Utilities
Source:		%{name}-%{version}.tar.gz
Source1:	%{initname}-%{initversion}.tar.bz2
Patch:		%{name}-%{version}-strcasestr.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%(id -u -n)
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/touch
BuildRequires:	coreutils filesystem fileutils fillup make c_compiler libtool
BuildRequires:	pwdutils
Requires:	python
Requires:	qmail >= 1.03
Obsoletes:	checkvpw
URL:		http://www.vmailmgr.org/

%description
Vmailmgr provides a virtualizing password-checking interface to
qmail-pop3d and courier IMAP as well as both a delivery agent to
automatically deliver mail within a virtual domain and a set of tools
to manage such a domain from either the command line or from the web.

Author:
-------
    Bruce Guenter <bruceg@em.ca>

%debug_package

%package cgi
Summary:	CGI applications for vmailmgr
Group:		Productivity/Networking/Email/Utilities
Requires:	vmailmgr-daemon = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description cgi
This package contains CGI applications to allow web-based administration
of vmailmgr systems.

%package local
Summary:	Vmailmgr daemon for CGIs
Group:		Productivity/Networking/Email/Utilities
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	supervise-scripts >= 3.2
Requires:	ucspi-ipc
Provides:	%{name}-daemon = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description local
This package contains the vmailmgrd daemon that provides virtual domain
manipulation services to support unprivileged clients like CGIs.

%package tcp
Summary:	Vmailmgr TCP daemon for remote CGIs
Group:		Productivity/Networking/Email/Utilities
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	supervise-scripts >= 3.2
Requires:	ucspi-tcp
Provides:	%{name}-daemon = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description tcp
This package contains the vmailmgrd daemon that provides virtual domain
manipulation services to support unprivileged clients like CGIs across
remote links.

%package php
Summary:	PHP include files
Group:		Productivity/Networking/Email/Utilities
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

%description php
This package contains the include files necessary to call VMailMgr
functions from PHP.

%package python
Summary:	Python library for accessing VMailMgr
Group:		Productivity/Networking/Email/Utilities
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	python >= 1.5

%description python
This package contains the Python library code necessary to call VMailMgr

%package courier-imap
Summary:	Courier authentication module for VMailMgr
Group:		Productivity/Networking/Email/Utilities
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	courier-authlib

%description courier-imap
Courier authentication module for VMailMgr.

%prep
%setup -q -a1
%patch
%{configure}

%build
%{__make} all

%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%{__make} \
	DESTDIR=%{buildroot} \
	cgidir=%{cgidir} \
	pythonlibdir=%{py_libdir}/vmailmgr \
	phpdir=%{phpdir} \
	install
%{__install} -d %{buildroot}%{_mandir}

%{__mkdir_p} %{buildroot}/usr/lib/courier-authlib
%{__mv} %{buildroot}/usr/lib/courier-imap/libexec/authlib/* %{buildroot}/usr/lib/courier-authlib

(
  cd %{initname}-%{initversion} && \
  %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
	sysconfdir=%{_sysconfdir} \
	fillupdir=%{_var}/adm/fillup-templates \
	install
)
%{__ln_s} ../../etc/init.d/vmailmgr-local %{buildroot}%{_sbindir}/rcvmailmgr-local
%{__ln_s} ../../etc/init.d/vmailmgr-tcp %{buildroot}%{_sbindir}/rcvmailmgr-tcp

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%pre
/usr/sbin/groupadd -r vmailmgr &>/dev/null || :
/usr/sbin/useradd -r -g vmailmgr -d /var/lib/vmailmgr -s /bin/false vmailmgr &>/dev/null || :

%post
%{fillup_only}

%post local
if test -L /service/vmailmgr-local -a -x /service/vmailmgr-local/run ; then
  pushd >/dev/null /service/vmailmgr-local
  %{__rm} /service/vmailmgr-local
  svc -dx . log
  popd >/dev/null
fi
%{fillup_and_insserv -fy}
%{fillup_only -ns vmailmgr local}
%{__ln_s} %{_sysconfdir}/vmailmgr-local /service/vmailmgr-local

%preun local
level=${1:-0}
test $level -eq 0 || exit 0
if test -L /service/vmailmgr-local ; then
  pushd >/dev/null /service/vmailmgr-local
  %{__rm} /service/vmailmgr-local
  svc -dx . log
  popd >/dev/null
  sleep 3
fi
%{__rm} -fr %{_sysconfdir}/vmailmgr-local/supervise || :
%{__rm} -fr %{_sysconfdir}/vmailmgr-local/log/supervise || :

%post tcp
if test -L /service/vmailmgr-tcp -a -x /service/vmailmgr-tcp/run ; then
  pushd >/dev/null /service/vmailmgr-tcp
  %{__rm} /service/vmailmgr-tcp
  svc -dx . log
  popd >/dev/null
fi
%{fillup_and_insserv -fy}
%{fillup_only -ns vmailmgr tcp}
%{__ln_s} %{_sysconfdir}/vmailmgr-tcp /service/vmailmgr-tcp

%preun tcp
level=${1:-0}
test $level -eq 0 || exit 0
if test -L /service/vmailmgr-tcp ; then
  pushd >/dev/null /service/vmailmgr-tcp
  %{__rm} /service/vmailmgr-tcp
  svc -dx . log
  popd >/dev/null
  sleep 3
fi
%{__rm} -fr %{_sysconfdir}/vmailmgr-tcp/supervise || :
%{__rm} -fr %{_sysconfdir}/vmailmgr-tcp/log/supervise || :

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS TODO
%doc authenticate/*.html commands/*.html daemon/*.html
%doc doc/ChangeLog-pre* doc/YEAR2000 doc/*.txt doc/*.html doc/*.pdf doc/*.info
%doc doc/*.texi
%attr(0755,root,root) %doc scripts/autoresponder.sh
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/autoresponse-dir
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/autoresponse-file
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/default-maildir
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/maildir-arg-str
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/password-file
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/socket-file
%attr(0644,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/user-dir
%attr(0755,root,root) %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr/vdeliver-postdeliver
%attr(0755,root,root) %{_sbindir}/vmailmgrd
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
%attr(0644,root,root) %{_mandir}/man7/*
%attr(0644,root,root) %{_mandir}/man8/*
%attr(0750,root,root) %{_prefix}/share/vmailmgr/create-config-vmailmgr
%attr(0755,vmailmgr,vmailmgr) %dir %{_var}/lib/vmailmgr
%attr(0755,root,root) %dir %{_var}/lib/vmailmgr/error-maildir
%attr(0755,root,root) %dir %{_var}/spool/bulletins
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.vmailmgr

%files cgi
%defattr(-,root,root)
%doc cgi/*.html
%attr(0755,root,root) %{cgidir}/listvdomain
%attr(0755,root,root) %{cgidir}/vaddalias
%attr(0755,root,root) %{cgidir}/vadduser
%attr(0755,root,root) %{cgidir}/vchattr
%attr(0755,root,root) %{cgidir}/vchforwards
%attr(0755,root,root) %{cgidir}/vdeluser
%attr(0755,root,root) %{cgidir}/vpasswd

%files php
%defattr(-,root,root)
%doc php/vmail.features
%attr(0755,root,root) %dir %{phpdir}
%attr(0644,root,root) %{phpdir}/*

%files python
%defattr(-,root,root)
%attr(0755,root,root) %dir %{py_libdir}/vmailmgr
%attr(0644,root,root) %{py_libdir}/vmailmgr/*

%files local
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/vmailmgr-local
%attr(-,root,root) %{_sbindir}/rcvmailmgr-local
%attr(0644,root,root) %{_sysconfdir}/permissions.d/vmailmgr-local
%attr(1755,root,root) %dir %{_sysconfdir}/vmailmgr-local
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr-local/env
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr-local/log
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/vmailmgr-local/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/vmailmgr-local/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr-local/env/*
%attr(0750,root,root) %{_prefix}/share/vmailmgr/create-config-vmailmgr-local
%attr(0750,root,root) %{_prefix}/share/vmailmgr/create-log-config-vmailmgr-local
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.vmailmgr-local
%attr(0755,nobody,nobody) %dir %{_var}/log/vmailmgr-local

%files tcp
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/vmailmgr-tcp
%attr(-,root,root) %{_sbindir}/rcvmailmgr-tcp
%attr(0644,root,root) %{_sysconfdir}/permissions.d/vmailmgr-tcp
%attr(1755,root,root) %dir %{_sysconfdir}/vmailmgr-tcp
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr-tcp/env
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr-tcp/log
%attr(0755,root,root) %dir %{_sysconfdir}/vmailmgr-tcp/rules
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/vmailmgr-tcp/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/vmailmgr-tcp/log/run
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr-tcp/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr-tcp/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr-tcp/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/vmailmgr-tcp/rules/data.cdb
%attr(0750,root,root) %{_prefix}/share/vmailmgr/create-config-vmailmgr-tcp
%attr(0750,root,root) %{_prefix}/share/vmailmgr/create-log-config-vmailmgr-tcp
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.vmailmgr-tcp
%attr(0755,nobody,nobody) %dir %{_var}/log/vmailmgr-tcp

%files courier-imap
%defattr(-,root,root)
/usr/lib/courier-authlib/*

%changelog
* Thu Apr 29 2010 Bernhard Graf <graf@movingtarget.de> 0.97-4
- make it build with glibc 2.10+
* Thu Mar 06 2008 Bernhard Graf <graf@movingtarget.de>
- fixed autoresponder facility (/etc/vmailmgr must be world-readable)
* Tue Mar 04 2008 Bernhard Graf <graf@movingtarget.de>
- refactored configuration file layout
- removed SuSEconfig configuration setup - configuration is now created
  when the services are started
* Sat Feb 05 2005 Bernhard Graf <graf@movingtarget.de>
- updated to v0.97
* Wed Dec 10 2003 Bernhard Graf <graf@movingtarget.de>
- first package release
