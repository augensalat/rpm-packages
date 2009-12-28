#
# spec file for package mailfront (Version 1.11)
#
# Copyright  (c)  2002-2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# %define _unpackaged_files_terminate_build 0
%define name mailfront
%define initname %{name}-init
%define version 1.11
%define initversion %{version}
%define release 10

%if 0%{?suse_version} > 1020
%define with_susefirewall_config 1
%endif

%define build_dietlibc	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}

Name:		%{name}
Version:	%{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Mail server network protocol front-ends
License:	GPL
Group:		Productivity/Networking/Email/Servers
Source0:	http://untroubled.org/mailfront/%{name}-%{version}.tar.gz
Source1:	%{initname}-%{initversion}.tar.bz2
Source2:	%{name}-SuSEfirewall-0.01.tar.bz2
Patch:		%{name}-%{version}.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -nu)
PreReq:		%fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
BuildRequires:	c_compiler make patch binutils coreutils
BuildRequires:	bglibs >= 1.101 cvm-devel >= 0.81
%if %{build_dietlibc}
BuildRequires:  dietlibc >= 0.30
%endif
Requires:	qmail >= 1.03 ucspi-tcp daemontools
URL:		http://untroubled.org/mailfront/

%description
This is mailfront, a package containing customizeable network front-ends
for mail servers.  Handles POP3, QMQP, QMTP, SMTP, and IMAP
(authentication only).

Author:
-------
    Bruce Guenter <bruceg@em.ca>

%debug_package

%package devel
Summary:	Mailfront development bits
Group:		Productivity/Networking/Email/Servers/Development

%description devel
Headers for building modules (front-ends, plugins, and back-ends) for
mailfront.

%package smtpd
Summary:	SMTP daemon replacement for qmail's smtpd
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools qmail >= 1.03 supervise-scripts >= 3.3 ucspi-tcp
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
Provides:	smtp_daemon

%description smtpd
The code for SMTP is divided internally into two sections: front-end and
back-end code. The front-end code handles the low-level details of the
protocol. The back-end code handles the validation and delivery details
in a protocol-independant fashion.

%package submissiond
Summary:	Email submission daemon ("smtp-auth-only")
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools qmail >= 1.03 supervise-scripts >= 3.3 ucspi-tcp
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description submissiond
A message submission daemon, see RFC 2476.

%package smtpsd
Summary:	Email submission daemon ("smtp-auth-only")
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools qmail >= 1.03 supervise-scripts >= 3.3 ucspi-ssl
Requires:	openssl
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description smtpsd
A message submission daemon, see RFC 2476, with SSL encryption.

%package qmtpd
Summary:	QMTP daemon replacement for qmail's qmtpd
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools qmail >= 1.03 supervise-scripts >= 3.3 ucspi-tcp
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description qmtpd
QMTP daemon replacement for qmail's qmtpd (qmtpfront-qmail)

%package qmqpd
Summary:	QMQP daemon replacement for qmail's qmqpd
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools qmail >= 1.03 supervise-scripts >= 3.3 ucspi-tcp
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description qmqpd
QMQP daemon replacement for qmail's qmqpd (qmqpfront-qmail)

%package pop3d
Summary:	POP3 daemon replacement for qmail's pop3d
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3 ucspi-tcp
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description pop3d
The POP3 front end is composed of two pieces: an authentication front end
(pop3front-auth) and a transfer back-end (pop3front-maildir).

%package pop3sd
Summary:	POP3 daemon with SSL encryption
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	daemontools supervise-scripts >= 3.3 ucspi-ssl openssl
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description pop3sd
POP3 daemon with SSL encryption.

%package imapd
Summary:	IMAP CVM authentication frontend for courier-imap
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	cvm daemontools supervise-scripts >= 3.3 ucspi-tcp
Requires:	courier-imap-solitary
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description imapd
courier-imap authentication frontend replacement to be used with CVM.

%package imapsd
Summary:	IMAP-SSL CVM authentication frontend for courier-imap
Group:		Productivity/Networking/Email/Servers
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	cvm daemontools supervise-scripts >= 3.3 ucspi-ssl
Requires:	openssl courier-imap-solitary
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod

%description imapsd
SSL encrypting courier-imap authentication frontend replacement to be used with CVM.

%prep
%setup -n %{name}-%{version} -a 1 -a 2
%patch
echo "%{_includedir}/bglibs" >conf-bgincs
echo "%{_libdir}/bglibs" >conf-bglibs
echo gcc %{optflags} >conf-cc
echo 'gcc %{optflags} -fPIC -shared' >conf-ccso
echo 'gcc -rdynamic' >conf-ld
echo %{_bindir} >conf-bin
echo %{_libdir}/mailfront >conf-modules
echo %{_includedir} >conf-include

%build
%{__make}

%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%{__make} install_prefix=%{buildroot} install

%{__install} -d -m 0755 %{buildroot}%{_sbindir}
(
  cd %{initname}-%{initversion} && \
  %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	sysconfdir=%{_sysconfdir} \
	sharedir=%{_prefix}/share/mailfront \
	fillupdir=%{_var}/adm/fillup-templates \
	permissionsdir=%{_sysconfdir}/permissions.d \
	install
)
%{__ln_s} %{_sysconfdir}/init.d/mailfront-smtpd %{buildroot}%{_sbindir}/rcmailfront-smtpd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-submissiond %{buildroot}%{_sbindir}/rcmailfront-submissiond
%{__ln_s} %{_sysconfdir}/init.d/mailfront-smtpsd %{buildroot}%{_sbindir}/rcmailfront-smtpsd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-qmtpd %{buildroot}%{_sbindir}/rcmailfront-qmtpd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-qmqpd %{buildroot}%{_sbindir}/rcmailfront-qmqpd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-pop3d %{buildroot}%{_sbindir}/rcmailfront-pop3d
%{__ln_s} %{_sysconfdir}/init.d/mailfront-pop3sd %{buildroot}%{_sbindir}/rcmailfront-pop3sd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-imapd %{buildroot}%{_sbindir}/rcmailfront-imapd
%{__ln_s} %{_sysconfdir}/init.d/mailfront-imapsd %{buildroot}%{_sbindir}/rcmailfront-imapsd

%if 0%{?with_susefirewall_config}
  (
    cd mailfront-SuSEfirewall-0.01
    %{__make} DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} install
  )
%endif

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%post
%{fillup_only}

%post smtpd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-smtpd -a -x /service/mailfront-smtpd/run ; then
  pushd /service/mailfront-smtpd
  %{__rm} /service/mailfront-smtpd
  svc -dx . log
  popd >/dev/null
fi
if test $level = 1 ; then
  pushd /etc >/dev/null
  if test -f /var/run/inetd.pid && egrep '^smtp' inetd.conf &>/dev/null ; then
    test ! -e inetd.conf.rpmsave || %{__cp} -v inetd.conf inetd.conf.rpmsave
    %{__sed} -e 's/^smtp[    ]/#smtp /' inetd.conf >inetd.conf.new
    %{__mv} -f inetd.conf.new inetd.conf
    kill -HUP `cat /var/run/inetd.pid`
  fi
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront smtpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-smtpd/down
  touch %{_sysconfdir}/mailfront-smtpd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-smtpd /service/mailfront-smtpd

%preun smtpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-smtpd ; then
  pushd >/dev/null /service/mailfront-smtpd
  %{__rm} /service/mailfront-smtpd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-smtpd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-smtpd/log/supervise || :

%postun smtpd
%{insserv_cleanup}

%post submissiond
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-submissiond -a -x /service/mailfront-submissiond/run ; then
  pushd >/dev/null /service/mailfront-submissiond
  %{__rm} /service/mailfront-submissiond
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront submissiond}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-submissiond/down
  touch %{_sysconfdir}/mailfront-submissiond/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-submissiond /service/mailfront-submissiond

%preun submissiond
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-submissiond ; then
  pushd >/dev/null /service/mailfront-submissiond
  %{__rm} /service/mailfront-submissiond
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-submissiond/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-submissiond/log/supervise || :

%postun submissiond
%{insserv_cleanup}

%post smtpsd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-smtpsd -a -x /service/mailfront-smtpsd/run ; then
  pushd >/dev/null /service/mailfront-smtpsd
  %{__rm} /service/mailfront-smtpsd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront smtpsd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-smtpsd/down
  touch %{_sysconfdir}/mailfront-smtpsd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-smtpsd /service/mailfront-smtpsd

%preun smtpsd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-smtpsd ; then
  pushd >/dev/null /service/mailfront-smtpsd
  %{__rm} /service/mailfront-smtpsd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-smtpsd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-smtpsd/log/supervise || :

%postun smtpsd
%{insserv_cleanup}

%post qmtpd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-qmtpd -a -x /service/mailfront-qmtpd/run ; then
  pushd >/dev/null /service/mailfront-qmtpd
  %{__rm} /service/mailfront-qmtpd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront qmtpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-qmtpd/down
  touch %{_sysconfdir}/mailfront-qmtpd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-qmtpd /service/mailfront-qmtpd

%preun qmtpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-qmtpd ; then
  pushd >/dev/null /service/mailfront-qmtpd
  %{__rm} /service/mailfront-qmtpd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-qmtpd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-qmtpd/log/supervise || :

%postun qmtpd
%{insserv_cleanup}

%post qmqpd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-qmqpd -a -x /service/mailfront-qmqpd/run ; then
  pushd >/dev/null /service/mailfront-qmqpd
  %{__rm} /service/mailfront-qmqpd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront qmqpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-qmqpd/down
  touch %{_sysconfdir}/mailfront-qmqpd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-qmqpd /service/mailfront-qmqpd

%preun qmqpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-qmqpd ; then
  pushd >/dev/null /service/mailfront-qmqpd
  %{__rm} /service/mailfront-qmqpd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-qmqpd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-qmqpd/log/supervise || :

%postun qmqpd
%{insserv_cleanup}

%post pop3d
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-pop3d -a -x /service/mailfront-pop3d/run ; then
  pushd >/dev/null /service/mailfront-pop3d
  %{__rm} /service/mailfront-pop3d
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront pop3d}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-pop3d/down
  touch %{_sysconfdir}/mailfront-pop3d/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-pop3d /service/mailfront-pop3d

%preun pop3d
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-pop3d ; then
  pushd >/dev/null /service/mailfront-pop3d
  %{__rm} /service/mailfront-pop3d
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-pop3d/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-pop3d/log/supervise || :

%postun pop3d
%{insserv_cleanup}

%post pop3sd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-pop3sd -a -x /service/mailfront-pop3sd/run ; then
  pushd >/dev/null /service/mailfront-pop3sd
  %{__rm} /service/mailfront-pop3sd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront pop3sd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-pop3sd/down
  touch %{_sysconfdir}/mailfront-pop3sd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-pop3sd /service/mailfront-pop3sd

%preun pop3sd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-pop3sd ; then
  pushd >/dev/null /service/mailfront-pop3sd
  %{__rm} /service/mailfront-pop3sd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-pop3sd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-pop3sd/log/supervise || :

%postun pop3sd
%{insserv_cleanup}

%post imapd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-imapd -a -x /service/mailfront-imapd/run ; then
  pushd >/dev/null /service/mailfront-imapd
  %{__rm} /service/mailfront-imapd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront imapd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-imapd/down
  touch %{_sysconfdir}/mailfront-imapd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-imapd /service/mailfront-imapd

%preun imapd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-imapd ; then
  pushd >/dev/null /service/mailfront-imapd
  %{__rm} /service/mailfront-imapd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-imapd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-imapd/log/supervise || :

%postun imapd
%{insserv_cleanup}

%post imapsd
level=${1:-0}
# in any case remove service first
if test -L /service/mailfront-imapsd -a -x /service/mailfront-imapsd/run ; then
  pushd >/dev/null /service/mailfront-imapsd
  %{__rm} /service/mailfront-imapsd
  svc -dx . log
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans mailfront imapsd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/mailfront-imapsd/down
  touch %{_sysconfdir}/mailfront-imapsd/log/down
fi
%{__ln_s} %{_sysconfdir}/mailfront-imapsd /service/mailfront-imapsd

%preun imapsd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/mailfront-imapsd ; then
  pushd >/dev/null /service/mailfront-imapsd
  %{__rm} /service/mailfront-imapsd
  svc -dx . log
  popd >/dev/null
fi
sleep 3
%{__rm} -fr %{_sysconfdir}/mailfront-imapsd/supervise || :
%{__rm} -fr %{_sysconfdir}/mailfront-imapsd/log/supervise || :

%postun imapsd
%{insserv_cleanup}

%files
%defattr(-,root,root)
%doc ANNOUNCEMENT COPYING NEWS README TODO *.html
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_libdir}/mailfront
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront

%files devel
%{_includedir}/mailfront

%files smtpd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-smtpd
%{_sbindir}/rcmailfront-smtpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-smtpd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-smtpd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpd/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-smtpd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-smtpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-smtpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-smtpd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpd/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-smtpd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-smtpd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-smtpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-smtpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-smtpd

%files submissiond
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-submissiond
%{_sbindir}/rcmailfront-submissiond
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-submissiond
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-submissiond
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-submissiond/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-submissiond/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-submissiond/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-submissiond/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-submissiond/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-submissiond/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-submissiond/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-submissiond/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-submissiond/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-submissiond/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-submissiond/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-submissiond/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-submissiond
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-submissiond
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-submissiond
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-submissiond
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-submissiond

%files smtpsd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-smtpsd
%{_sbindir}/rcmailfront-smtpsd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-smtpsd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-smtpsd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpsd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpsd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-smtpsd/rules
%attr(0750,root,nogroup) %dir %{_sysconfdir}/mailfront-smtpsd/ssl
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-smtpsd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-smtpsd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-smtpsd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-smtpsd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/rules/include
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-smtpsd/ssl/openssl.cnf
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-smtpsd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-smtpsd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-smtpsd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-smtpsd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-smtpsd

%files qmtpd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-qmtpd
%{_sbindir}/rcmailfront-qmtpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-qmtpd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-qmtpd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmtpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmtpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmtpd/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-qmtpd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-qmtpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-qmtpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-qmtpd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmtpd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmtpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmtpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmtpd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmtpd/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-qmtpd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-qmtpd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-qmtpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-qmtpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-qmtpd

%files qmqpd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-qmqpd
%{_sbindir}/rcmailfront-qmqpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-qmqpd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-qmqpd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmqpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmqpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-qmqpd/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-qmqpd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-qmqpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-qmqpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-qmqpd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmqpd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmqpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmqpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmqpd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-qmqpd/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-qmqpd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-qmqpd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-qmqpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-qmqpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-qmqpd

%files pop3d
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-pop3d
%{_sbindir}/rcmailfront-pop3d
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-pop3d
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-pop3d
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3d/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3d/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3d/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-pop3d/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-pop3d/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-pop3d/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-pop3d/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3d/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3d/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3d/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3d/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3d/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-pop3d
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-pop3d
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-pop3d
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-pop3d
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-pop3d

%files pop3sd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-pop3sd
%{_sbindir}/rcmailfront-pop3sd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-pop3sd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-pop3sd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3sd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3sd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-pop3sd/rules
%attr(0750,root,nogroup) %dir %{_sysconfdir}/mailfront-pop3sd/ssl
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-pop3sd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-pop3sd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-pop3sd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-pop3sd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/rules/include
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-pop3sd/ssl/openssl.cnf
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-pop3sd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-pop3sd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-pop3sd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-pop3sd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-pop3sd

%files imapd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-imapd
%{_sbindir}/rcmailfront-imapd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-imapd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-imapd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapd/rules
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-imapd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-imapd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-imapd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-imapd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapd/rules/include
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-imapd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-imapd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-imapd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-imapd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-imapd

%files imapsd
%defattr(-,root,root)
%attr(0754,root,root) %{_sysconfdir}/init.d/mailfront-imapsd
%{_sbindir}/rcmailfront-imapsd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/mailfront-imapsd
%attr(1755,root,root) %dir %{_sysconfdir}/mailfront-imapsd
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapsd/env
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapsd/log
%attr(0755,root,root) %dir %{_sysconfdir}/mailfront-imapsd/rules
%attr(0750,root,nogroup) %dir %{_sysconfdir}/mailfront-imapsd/ssl
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-imapsd/run
%attr(0754,root,root) %config(noreplace) %{_sysconfdir}/mailfront-imapsd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-imapsd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/mailfront-imapsd/log/down
%attr(0644,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/env/*
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/rules/data.cdb
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/rules/include
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/mailfront-imapsd/ssl/openssl.cnf
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/mailfront-imapsd
%endif
%attr(0750,root,root) %{_prefix}/share/mailfront/create-config-mailfront-imapsd
%attr(0750,root,root) %{_prefix}/share/mailfront/create-log-config-mailfront-imapsd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.mailfront-imapsd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/mailfront-imapsd

%changelog
* Fri Sep 19 2008 Bernhard Graf <graf@movingtarget.de> 1-11-10
- added "Provides: smtp_daemon" for OpenSUSE compatibility
* Tue Apr 08 2008 Bernhard Graf <graf@movingtarget.de> 1-11-9
- support for plugin-policyd in smtpd setup
* Sun Mar 23 2008 Bernhard Graf <graf@movingtarget.de> 1-11-8
- patch imapfront-auth to improve courier-imap compability, esp for ACLs
- patch pop3front to add CAPA command and AUTH query command
* Wed Mar 19 2008 Bernhard Graf <graf@movingtarget.de> 1-11-7
- removed Obsoletes and Provides lines
- added SSL secured SMTP, POP3 and IMAP services
* Sun Mar 16 2008 Bernhard Graf <graf@movingtarget.de> 1-11-6
- added recipient patch to fix plugin oddities with recipient handling
* Wed Mar 12 2008 Bernhard Graf <graf@movingtarget.de> 1-11-5
- Working setup for courier-imap-solitary
* Fri Mar 07 2008 Bernhard Graf <graf@movingtarget.de> 1-11-4
- fixed softlimit call to use `-d' instead of `-m'
- mailfront-smtpd now optionally uses greylite instead of rblsmtpd
* Thu Mar 06 2008 Bernhard Graf <graf@movingtarget.de> 1.11-3
- bug fix patch for plugin-cvm-validate
- spec file bug fix where fillup was not found after a `cd'
- run file fixes: replaced $PLUGINS by $plugins to prevent clashes with mailfront
  that reads $PLUGINS implicitely
* Fri Feb 29 2008 Bernhard Graf <graf@movingtarget.de> 1.11-2
- refactored configuration file layout
- removed SuSEconfig configuration setup - configuration is now created
  when the service is started
- automatically open SuSEfirewall for the respective daemons on SuSE >=10.3
* Tue Jan 22 2008 Bernhard Graf <graf@movingtarget.de> 1.11-1
- updated to version 1.11
- refactored file system layout to avoid conflicts with installed daemons
  so they can be installed in parallel
* Fri Jan 18 2008 Bernhard Graf <graf@movingtarget.de>
- patch for cvm-validate.c
- fixed run scripts
* Mon Feb 07 2005 Bernhard Graf <graf@movingtarget.de>
- bug fixes in init scripts
* Fri Jan 28 2005 Bernhard Graf <graf@movingtarget.de>
- Version 0.92
* Thu Feb 12 2004 Bernhard Graf <graf@movingtarget.de>
- Version 0.90
- Fix in /var/service/smtpd/run to always use rblsmtpd
* Wed Jan 21 2004 Bernhard Graf <graf@movingtarget.de>
- bug fix: Some environment variables have been written to /etc/qmail/control
* Sun Dec 07 2003 Bernhard Graf <graf@movingtarget.de>
- Version 0.88
* Thu Nov 27 2003 Bernhard Graf <graf@movingtarget.de>
- Version 0.87
- easier installation (configuration with /etc/sysconfig and SuSEconfig)
* Thu Feb 06 2003 Bernhard Graf <graf@adjoli.de>
- Version 0.81
- Startup scripts cleanups
* Mon Aug 12 2002 Bernhard Graf <graf@adjoli.de>
- Initial wrap
