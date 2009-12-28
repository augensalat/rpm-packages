#
# spec file for package twoftpd (Version 1.41)
#
# Copyright  (c)  2002-2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define _unpackaged_files_terminate_build 0
%define name twoftpd
%define initname %{name}-init
%define version 1.41
%define initversion %{version}
%define release 0

%if 0%{?suse_version} > 1020
%define with_susefirewall_config 1
%endif

Name:		%{name}
Version:	%{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Secure, simple, and efficient FTP server
License:	GPL
Group:		Productivity/Networking/Ftp/Servers
Source0:	http://untroubled.org/twoftpd/%{name}-%{version}.tar.gz
Source1:	%{initname}-%{version}.tar.bz2
Source2:	%{name}-SuSEfirewall-0.01.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -nu)
PreReq:         %insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
BuildRequires:	c_compiler make patch binutils coreutils
BuildRequires:	bglibs >= 1.103, cvm >= 0.90, cvm-devel >= 0.90
Requires:	daemontools supervise-scripts >= 3.5 ucspi-tcp
Requires:	cvm >= 0.90
URL:		http://untroubled.org/twoftpd/

%description
This is twoftpd, a new FTP server that strives to be secure, simple, and
efficient.

Author:
-------
    Bruce Guenter <bruceg@em.ca>

%prep
%setup -q -a 1 -a 2
echo "%{_includedir}/bglibs" >conf-bgincs
echo "%{_libdir}/bglibs" >conf-bglibs
echo "gcc ${optflags}" >conf-cc
echo "gcc -s" >conf-ld
echo %{_bindir} >conf-bin
echo %{_mandir} >conf-man

%build
%{__make} programs

%install
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_mandir}
make install install_prefix=%{buildroot}

%{__install} -d -m 0755 %{buildroot}%{_sbindir}
(
  cd %{initname}-%{version} && \
   %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	sharedir=%{_prefix}/share/twoftpd \
	fillupdir=%{_var}/adm/fillup-templates \
	permissionsdir=%{_sysconfdir}/permissions.d \
	install
)

%{__ln_s} ../../etc/init.d/$n %{buildroot}%{_sbindir}/rctwoftpd

%if 0%{?with_susefirewall_config}
  (
    cd twoftpd-SuSEfirewall-0.01
    %{__make} DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} install
  )
%endif

%clean
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

# Pre/Post-install Scripts #####################################################
%pre
groupadd -r twoftpd 2>/dev/null || :
useradd -r -g twoftpd -G '' -d %{_sysconfdir}/twoftpd -s /bin/true twoftpd || :

%post
level=${1:-0}
# in any case remove service first
if test -L /service/twoftpd -a -x /service/twoftpd/run ; then
  pushd /service/twoftpd
  %{__rm} /service/twoftpd
  svc -dx . log
  popd >/dev/null
fi
%{fillup_and_insserv twoftpd}
if test $level -eq 1 ; then
  touch %{_sysconfdir}/twoftpd/down
  touch %{_sysconfdir}/twoftpd/log/down
fi
%{__ln_s} %{_sysconfdir}/twoftpd /service/twoftpd

%preun
# stop and remove service
if test -L "/service/twoftpd" ; then
  svc-remove twoftpd
  %{__rm} -fr %{_var}/service/twoftpd/supervise
  %{__rm} -fr %{_var}/service/twoftpd/log/supervise
fi

level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/twoftpd ; then
  pushd >/dev/null /service/twoftpd
  %{__rm} /service/twoftpd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/twoftpd/supervise || :
%{__rm} -fr %{_sysconfdir}/twoftpd/log/supervise || :

%postun
%{insserv_cleanup}

%files
%defattr(-,root,root)
%doc COPYING NEWS README TODO
%doc %{_mandir}/*
%attr(0755,root,root) %{_bindir}/*
%attr(0744,root,root) /etc/init.d/twoftpd
%attr(-,root,root) %{_sbindir}/rctwoftpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/twoftpd
%attr(1755,root,root) %dir %{_sysconfdir}/twoftpd
%attr(0700,root,root) %dir %{_sysconfdir}/twoftpd/env
%attr(0700,root,root) %dir %{_sysconfdir}/twoftpd/log
%attr(0700,root,root) %dir %{_sysconfdir}/twoftpd/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/twoftpd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/twoftpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/twoftpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/twoftpd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/twoftpd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/twoftpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/twoftpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/twoftpd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/twoftpd/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/twoftpd
%endif
%attr(0750,root,root) %{_prefix}/share/twoftpd/create-config
%attr(0750,root,root) %{_prefix}/share/twoftpd/create-log-config
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.twoftpd
%attr(0700,twoftpd,twoftpd) %dir %{_var}/log/twoftpd

%changelog
* Mon Nov 03 2008 Bernhard Graf <graf@movingtarget.de>
- updated to version 1.41
* Tue Feb 08 2005 Bernhard Graf <graf@movingtarget.de>
- updated to version 1.20 which includes Scott's patches already
* Sat Dec 27 2003 Bernhard Graf <graf@movingtarget.de>
- included Scott Gifford's patches from
  http://www.suspectclass.com/~sgifford/bgware-patches/
  to have twoftpd-xfer and twoftpd-anon with the same IP
- moved service directory from /etc/twoftpd/service to /var/service
* Sun Dec 21 2003 Bernhard Graf <graf@movingtarget.de>
- updated to v1.17
- SuSE 8.2 sysconfig/SuSEconfig stuff
* Sun Jan 13 2002 Bernhard Graf <graf@adjoli.de>
- added manpages in %files section
* Sat Jan 12 2002 Bernhard Graf <graf@adjoli.de>
- first package release for adjoli/SuSE

