#
# spec file for package qmail (Version 1.03)
#
# Copyright  (c)  2001 - 2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# %define _unpackaged_files_terminate_build 0
%define pkgname		qmail
%define pkgversion	1.03
%define pkgrelease	56

%if 0%{?suse_version} > 1020
%define with_susefirewall_config 1
%endif

%define build_dietlibc	0
%define build_linksync	1
%define reiserfs	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}
%{?_with_nolinksync: %{expand: %%define build_linksync 0}}
%{?_with_reiserfs: %{expand: %%define reiserfs 1}}

Name:		%{pkgname}
Version:	%{pkgversion}
Release:        %{pkgrelease}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	qmail Mail Transfer Agent
License:	Public Domain
URL:		http://cr.yp.to/qmail.html
Packager:	Bernhard Graf <graf@movingtarget.de>
Group:		Productivity/Networking/Email/Servers
Source0:	http://cr.yp.to/qmail/%{pkgname}-%{pkgversion}.tar.gz
Source1:	qmail-init-%{pkgversion}.tar.bz2
Source2:	qmail-SuSEfirewall-0.01.tar.bz2
Patch0:		%{pkgname}-%{pkgversion}-master.patch
Patch1:		%{pkgname}-%{pkgversion}-link-sync.patch
Patch2:		%{pkgname}-%{pkgversion}-dietlibc-readwrite.patch
Provides:	MTA
Provides:	smtp_daemon
Obsoletes:	sendmail postfix exim
Provides:	sendmail
Conflicts:	qmail-cyclog
BuildRoot:	%{_tmppath}/%{name}-%{pkgversion}-%(id -nu)
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
BuildRequires:	c_compiler make patch binutils coreutils
%if %{build_dietlibc}
BuildRequires:  dietlibc >= 0.30
%endif
Requires:	aaa_base aaa_skel djbdns-tools net-tools sh-utils pwdutils
Requires:	daemontools supervise-scripts >= 3.2 ucspi-ipc ucspi-tcp >= 0.86-1
Requires:	util-linux

%description
Qmail is a small, fast, secure replacement for the sendmail package,
which is the program that actually receives, routes, and delivers
electronic mail.  *** Note: Be sure and read the documentation as there
are some small but very significant differences between sendmail and
qmail and the programs that interact with them.

Qmail is targeted at real mail servers with MX record and a permanent
TCP internet connection.

This qmail variant is optimized for high-volume servers.
%if %{reiserfs}
The qmail queue is optimized for the Reiser filesystem or any
filesystem that does hashing for fast file retrieval.
%endif
%if %{build_dietlibc}
Built with dietlibc.
%endif

%debug_package

%package smtpd
Group:		Productivity/Networking/Email/Servers
Summary:	SMTP server support for qmail
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	aaa_base daemontools sh-utils net-tools
Requires:	supervise-scripts >= 3.2 ucspi-tcp >= 0.86-1
Requires:	make util-linux
Provides:	qmail-smtpd
Provides:	smtp_daemon
%description smtpd
Support files for running the qmail SMTP server.
RBL blocking is supported by the rblsmtpd in the new ucspi-tcp package.
%if %{build_dietlibc}
Built with dietlibc.
%endif

%package qmtpd
Group:		Productivity/Networking/Email/Servers
Summary:	QMTP server support for qmail
Provides:	qmtpdaemon
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	aaa_base
Requires:	sh-utils
Requires:	net-tools
Requires:	supervise-scripts >= 3.2
Requires:	ucspi-tcp >= 0.86-1
Requires:	make
Provides:	qmtp_daemon
Provides:	qmail-qmtpd
%description qmtpd
Support files for running the qmail QMTP server.
%if %{build_dietlibc}
Built with dietlibc.
%endif

%package qmqpd
Group:		Productivity/Networking/Email/Servers
Summary:	QMQP server support for qmail
Provides:	qmqpdaemon
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	aaa_base
Requires:	sh-utils
Requires:	net-tools
Requires:	supervise-scripts >= 3.2
Requires:	ucspi-tcp >= 0.86-1
Requires:	make
Provides:	qmqp_daemon
Provides:	qmail-qmqpd
%description qmqpd
Support files for running the qmail QMQP server.
%if %{build_dietlibc}
Built with dietlibc.
%endif

%package pop3d
Group:		Productivity/Networking/Email/Servers
Summary:	POP3 server support for qmail
Provides:	pop3daemon
PreReq:		%insserv_prereq %fillup_prereq /bin/cat /bin/sed /bin/mkdir /bin/touch /bin/chown /bin/chmod
Requires:	%{name} = %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
Requires:	aaa_base
Requires:	sh-utils
Requires:	net-tools
Requires:	supervise-scripts >= 3.2
Requires:	ucspi-tcp >= 0.86-1
Requires:	checkpassword
Requires:	make
Provides:	pop3daemon
Provides:	pop3_daemon
Provides:	qmail-pop3d
%description pop3d
Support files for running the qmail POP3 server.
%if %{build_dietlibc}
Built with dietlibc.
%endif


%prep
%setup -n qmail-%{pkgversion}
%patch0
%if %{build_linksync}
%patch1
%endif
%if %{build_dietlibc}
%patch2
echo "diet cc -DEXTERNAL_TODO $RPM_OPT_FLAGS" >conf-cc
echo 'diet cc -static' >conf-ld
%else
echo "cc -DEXTERNAL_TODO $RPM_OPT_FLAGS" >conf-cc
echo cc >conf-ld
%endif


fds=`ulimit -n`
let spawnlimit='(fds-6)/2'
echo $spawnlimit >conf-spawn

%if %{reiserfs}
# conf-plit for ReiserFS
echo 1 >conf-split
%else
# conf-split for high volumes on ext2:
# assuming modern extX fs with dir_index turned on
echo 13 >conf-split
%endif

cat <<ETX >conf-groups
qmail
nogroup
ETX

%setup -n qmail-%{pkgversion} -D -T -a 1 -a 2

%build

make it man

%install

# These users and groups must be created before qmail can be installed!

groupadd -r nogroup &>/dev/null || :
groupadd -r qmail &>/dev/null || :
useradd -r -g nogroup -d /etc/qmail/alias -s /bin/true alias &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmaild &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmaill &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmailp &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmailq &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmailr &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmails &>/dev/null || :
useradd -r -g qmail -d /var/log -s /bin/true qmaillog &>/dev/null || :

test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%{__install} -d %{buildroot}
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_mandir}
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_docdir}/%{pkgname}
pushd %{buildroot}
  %{__install} -d sbin
  %{__install} -d etc/cron.hourly
  %{__install} -d etc/qmail
  %{__install} -d etc/qmail/alias
  %{__install} -d etc/qmail/control
  %{__install} -d etc/qmail/owners
  %{__install} -d etc/qmail/users
  %{__install} -d usr/lib
  %{__install} -d var/qmail
  %{__install} -d var/log/{qmail,qmail-qmtpd,qmail-smtpd,qmail-pop3d,qmail-qmqpd}

  %{__ln_s} ../../etc/qmail/alias var/qmail/alias
  %{__ln_s} ../../etc/qmail/control var/qmail/control
  %{__ln_s} ../../etc/qmail/owners var/qmail/owners
  %{__ln_s} ../../etc/qmail/users var/qmail/users
  %{__ln_s} ../..%{_bindir} var/qmail/bin
  %{__ln_s} ../..%{_mandir} var/qmail/man
popd

# Build the user and group files, required for qmail-hier
./make-owners .
# INSTALL IT
./install %{buildroot}/var/qmail
# CHECK IT
./instcheck %{buildroot}/var/qmail

# Remove preformatted man pages
%{__rm} -rf %{buildroot}/var/qmail/man/cat*
%{__rm} %{buildroot}/var/qmail/man
# rename mbox manpage to avoid conflict with mutt's mbox manpage
%{__mv} %{buildroot}%{_mandir}/man5/mbox.5 %{buildroot}%{_mandir}/man5/qmail-mbox.5

# qmail-* programs go to /sbin, all other rest in /usr/bin
# %{__mv} %{buildroot}%{_bindir}/qmail-* %{buildroot}/sbin

pushd %{buildroot}%{_exec_prefix}
  # fix for sendmail add-ons
  %{__mv} bin/sendmail sbin/sendmail
  %{__ln_s} ../sbin/sendmail lib/sendmail
  %{__mv} bin/splogger sbin/splogger
popd

# Install some extra configuration programs
%{__install} ipmeprint %{buildroot}%{_sbindir}

(
  cd qmail-init-%{pkgversion} && \
  %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
	bindir=%{_bindir} \
	sbindir=/sbin \
	sysconfdir=%{_sysconfdir} \
	sharedir=%{_prefix}/share/qmail \
	fillupdir=%{_var}/adm/fillup-templates \
	permissionsdir=%{_sysconfdir}/permissions.d \
	install
)
%{__ln_s} -f ..%{_sysconfdir}/init.d/qmail %{buildroot}/sbin/rcqmail
%{__ln_s} -f ..%{_sysconfdir}/init.d/qmail-smtpd %{buildroot}/sbin/rcqmail-smtpd
%{__ln_s} -f ..%{_sysconfdir}/init.d/qmail-qmtpd %{buildroot}/sbin/rcqmail-qmtpd
%{__ln_s} -f ..%{_sysconfdir}/init.d/qmail-qmqpd %{buildroot}/sbin/rcqmail-qmqpd
%{__ln_s} -f ..%{_sysconfdir}/init.d/qmail-pop3d %{buildroot}/sbin/rcqmail-pop3d

%if 0%{?with_susefirewall_config}
  (
    cd qmail-SuSEfirewall-0.01
    %{__make} DESTDIR=%{buildroot} \
	sysconfdir=%{_sysconfdir} \
	install
  )
%endif

pushd %{buildroot}/etc/qmail/alias
  echo '&root' >.qmail-postmaster
  echo '&root' >.qmail-mailer-daemon
  touch .qmail-root
  chmod 644 .qmail*
popd

pushd %{buildroot}/etc/qmail/control
  touch defaultdomain locals me plusdomain rcpthosts
  chmod 644 defaultdomain locals me plusdomain rcpthosts
popd

pushd %{buildroot}/etc/qmail/users
  touch append assign cdb include exclude mailnames subusers
  chmod 644 *
popd

%{buildroot}%{_bindir}/make-owners %{buildroot}/etc/qmail

# echo ./Maildir/ >%{buildroot}/etc/qmail/control/aliasempty

# rebuild the sym-links under /var/qmail
(cd %{buildroot}/var/qmail && %{__rm} -f alias control users owners bin man)
%{__ln_s} ../../etc/qmail/alias %{buildroot}/var/qmail/alias
%{__ln_s} ../../etc/qmail/control %{buildroot}/var/qmail/control
%{__ln_s} ../../etc/qmail/owners %{buildroot}/var/qmail/owners
%{__ln_s} ../../etc/qmail/users %{buildroot}/var/qmail/users
%{__ln_s} ../../%{_bindir} %{buildroot}/var/qmail/bin
%{__ln_s} ../..%{_mandir} %{buildroot}/var/qmail/man
%{__rm} -rf %{buildroot}/var/qmail/boot
%{__rm} -rf %{buildroot}/var/qmail/doc
%{__ln_s} ../..%{_docdir}/%{name} %{buildroot}/var/qmail/doc

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

# Pre/Post-install Scripts #####################################################
%pre
groupadd -r nogroup &>/dev/null || :
groupadd -r qmail &>/dev/null || :
useradd -r -g nogroup -d /etc/qmail/alias -s /bin/true alias &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmaild &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmaill &>/dev/null || :
useradd -r -g nogroup -d /var/qmail -s /bin/true qmailp &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmailq &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmailr &>/dev/null || :
useradd -r -g qmail -d /var/qmail -s /bin/true qmails &>/dev/null || :
useradd -r -g qmail -d /var/log -s /bin/true qmaillog &>/dev/null || :

%post
level=${1:-0}
umask 022

# in any case remove services first
if test -L /service/qmail -a -x /service/qmail/run ; then
  cd /service/qmail
  %{__rm} /service/qmail
  svc -dx . log
fi
if test -L /service/qmail-qstat -a -x /service/qmail-qstat/run ; then
  cd /service/qmail-qstat
  %{__rm} /service/qmail-qstat
  svc -dx .
fi
if test -L /service/qmail-qread -a -x /service/qmail-qread/run ; then
  cd /service/qmail-qread
  %{__rm} /service/qmail-qread
  svc -dx .
fi

%{_bindir}/make-owners /etc/qmail
(
  cd >/dev/null /etc/qmail/users
  test -f cdb || ( qmail-pw2u </etc/passwd >assign && qmail-newu )
)

%{fillup_and_insserv -y qmail}

QMAILCTL=/etc/qmail/control

# Try to get a valid hostname...
FQHOSTNAME=$(/bin/hostname -f | tr A-Z a-z)
# check whether hostname contains at least one dot...
echo $FQHOSTNAME | grep "\." >/dev/null || FQHOSTNAME=""

test -z "$FQHOSTNAME" && {
    # still no valid hostname? Then read /etc/HOSTNAME
    test -s /etc/HOSTNAME && FQHOSTNAME=$(head -1 /etc/HOSTNAME)
    # check whether hostname contains at least one dot...
    echo $FQHOSTNAME | grep "\." >/dev/null || FQHOSTNAME=""
    # still no valid hostname? :-( set hostname to linux.local
    test -z "$FQHOSTNAME" && FQHOSTNAME=linux.local
}
test -f $QMAILCTL/me -a -s $QMAILCTL/me || \
	echo >$QMAILCTL/me $FQHOSTNAME
test -f $QMAILCTL/defaultdomain -a -s $QMAILCTL/defaultdomain || \
	echo >$QMAILCTL/defaultdomain $FQHOSTNAME
test -f $QMAILCTL/plusdomain -a -s $QMAILCTL/plusdomain || \
	echo >$QMAILCTL/plusdomain $FQHOSTNAME

if [ ! -f "$QMAILCTL/locals" ] ; then
  (
    echo localhost
    echo $FQHOSTNAME
    ipmeprint | (
      while read ip; do
        str=`dnsname $ip 2>/dev/null`
        test -n "$str" && echo $str
      done
    )
  ) | sort -u | tr A-Z a-z >> $QMAILCTL/locals
  cp $QMAILCTL/locals $QMAILCTL/rcpthosts
fi

# add services now
%{__ln_s} %{_sysconfdir}/qmail       /service/qmail
%{__ln_s} %{_sysconfdir}/qmail-qstat /service/qmail-qstat
%{__ln_s} %{_sysconfdir}/qmail-qread /service/qmail-qread


%preun
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove services
if test -L /service/qmail ; then
  cd /service/qmail
  %{__rm} /service/qmail
  svc -dx . log
fi
if test -L /service/qmail-qstat ; then
  cd /service/qmail-qstat
  %{__rm} /service/qmail-qstat
  svc -dx .
fi
if test -L /service/qmail-qread ; then
  cd /service/qmail-qread
  %{__rm} /service/qmail-qread
  svc -dx .
fi
sleep 5		# XXX
%{__rm} -fr %{_sysconfdir}/qmail/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail/log/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-qstat/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-qread/supervise || :

%postun
level=${1:-0}
%{insserv_cleanup}

test $level -gt 0 && exit 0
echo "Removing Qmail user ids..."
#userdel alias
userdel qmaild
userdel qmaill
userdel qmailp
userdel qmailq
userdel qmailr
userdel qmails
userdel qmaillog

echo "Removing qmail group ids..."
groupdel qmail
#groupdel nofiles || /bin/true


%post smtpd
level=${1:-0}
# in any case remove service first
if test -L /service/qmail-smtpd -a -x /service/qmail-smtpd/run ; then
  cd /service/qmail-smtpd
  %{__rm} /service/qmail-smtpd
  svc -dx . log
fi

if test $level = 1 ; then
  pushd /etc >/dev/null
  if [ -f /var/run/inetd.pid ] && egrep '^smtp' inetd.conf >/dev/null 2>&1; then
    if ! [ -e inetd.conf.rpmsave ]; then
      cp -v inetd.conf inetd.conf.rpmsave
    fi
    sed	-e 's/^smtp[ 	]/#smtp	/' inetd.conf >inetd.conf.new
    mv -f inetd.conf.new inetd.conf
    kill -HUP `cat /var/run/inetd.pid`
  fi
  popd >/dev/null
fi

%{fillup_and_insserv -f}
%{fillup_only -ans qmail smtpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/qmail-smtpd/down
  touch %{_sysconfdir}/qmail-smtpd/log/down
fi
%{__ln_s} %{_sysconfdir}/qmail-smtpd /service/qmail-smtpd

%preun smtpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/qmail-smtpd ; then
  cd /service/qmail-smtpd
  %{__rm} /service/qmail-smtpd
  svc -dx . log
  sleep 5	# XXX
fi
%{__rm} -fr %{_sysconfdir}/qmail-smtpd/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-smtpd/log/supervise || :

%postun smtpd
%{insserv_cleanup}


%post qmtpd
level=${1:-0}
# in any case remove service first
if test -L /service/qmail-qmtpd -a -x /service/qmail-qmtpd/run ; then
  cd /service/qmail-qmtpd
  %{__rm} /service/qmail-qmtpd
  svc -dx . log
fi

%{fillup_and_insserv -f}
%{fillup_only -ans qmail qmtpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/qmail-qmtpd/down
  touch %{_sysconfdir}/qmail-qmtpd/log/down
fi
%{__ln_s} %{_sysconfdir}/qmail-qmtpd /service/qmail-qmtpd

%preun qmtpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service 
if test -L /service/qmail-qmtpd ; then
  cd /service/qmail-qmtpd
  %{__rm} /service/qmail-qmtpd
  svc -dx . log
  sleep 5	# XXX
fi
%{__rm} -fr %{_sysconfdir}/qmail-qmtpd/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-qmtpd/log/supervise || :
 
%postun qmtpd
%{insserv_cleanup}


%post qmqpd
level=${1:-0}
# in any case remove service first
if test -L /service/qmail-qmqpd -a -x /service/qmail-qmqpd/run ; then
  cd /service/qmail-qmqpd
  %{__rm} /service/qmail-qmqpd
  svc -dx . log
fi

%{fillup_and_insserv -f}
%{fillup_only -ans qmail qmqpd}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/qmail-qmqpd/down
  touch %{_sysconfdir}/qmail-qmqpd/log/down
fi
%{__ln_s} %{_sysconfdir}/qmail-qmqpd /service/qmail-qmqpd

%preun qmqpd
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service 
if test -L /service/qmail-qmqpd ; then
  cd /service/qmail-qmqpd
  %{__rm} /service/qmail-qmqpd
  svc -dx . log
  sleep 5	# XXX
fi
%{__rm} -fr %{_sysconfdir}/qmail-qmqpd/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-qmqpd/log/supervise || :

%postun qmqpd
%{insserv_cleanup}


%post pop3d
level=${1:-0}
# in any case remove service first
if test -L /service/qmail-pop3d -a -x /service/qmail-pop3d/run ; then
  cd /service/qmail-pop3d
  %{__rm} /service/qmail-pop3d
  svc -dx . log
fi

%{fillup_and_insserv -f}
%{fillup_only -ans qmail pop3d}

# on first install service is installed but not started
if test $level -eq 1 ; then
  touch %{_sysconfdir}/qmail-pop3d/down
  touch %{_sysconfdir}/qmail-pop3d/log/down
fi
%{__ln_s} %{_sysconfdir}/qmail-pop3d /service/qmail-pop3d

%preun pop3d
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service 
if test -L /service/qmail-pop3d ; then
  cd /service/qmail-pop3d
  %{__rm} /service/qmail-pop3d
  svc -dx . log
  sleep 5	# XXX
fi
%{__rm} -fr %{_sysconfdir}/qmail-pop3d/supervise || :
%{__rm} -fr %{_sysconfdir}/qmail-pop3d/log/supervise || :

%postun pop3d
%{insserv_cleanup}

 
# Files List ###################################################################
%files
%defattr(-,root,qmail)

%doc BLURB BLURB2 BLURB3 BLURB4 CHANGES FAQ EXTTODO FILES
%doc INSTALL INSTALL.* INTERNALS PIC.* README* REMOVE.*
%doc SECURITY SENDMAIL TEST.* THANKS THOUGHTS TODO.* UPGRADE
%doc qmail-init-%{pkgversion}/README.*

%attr(0744,root,root) %config %{_sysconfdir}/init.d/qmail
/sbin/rcqmail

%config %{_sysconfdir}/profile.d/*

%defattr(-,-,qmail)

%config %{_sysconfdir}/cron.hourly/qmail-newusers

%attr(0644,root,root) %{_sysconfdir}/permissions.d/qmail

%attr(1755,root,root) %dir %{_sysconfdir}/qmail
%attr(0755,root,root) %dir %{_sysconfdir}/qmail/env
# %ghost %attr(-,root,qmail) %config(missingok,noreplace) %{_sysconfdir}/qmail/env/*
%attr(0755,root,root) %dir %{_sysconfdir}/qmail/log
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qstat
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qread
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail/log/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qstat/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qread/run

%attr(2755,alias,qmail) %dir %{_sysconfdir}/qmail/alias
%attr(0644,alias,qmail) %config(noreplace,missingok) %verify(not md5 size mtime) %{_sysconfdir}/qmail/alias/.qmail-*

%attr(0755,root,qmail) %{_sysconfdir}/qmail/owners

%attr(0755,root,qmail) %dir %{_sysconfdir}/qmail/users
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/assign
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/cdb
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/include
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/append
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/exclude
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/mailnames
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/users/subusers

%attr(0755,root,qmail) %dir %{_sysconfdir}/qmail/control
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %{_sysconfdir}/qmail/control/defaultdomain
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %{_sysconfdir}/qmail/control/locals
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %{_sysconfdir}/qmail/control/plusdomain
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %{_sysconfdir}/qmail/control/rcpthosts
# %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/qmail/control/aliasempty
%attr(0644,root,qmail) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail/control/me

%attr(0755,root,qmail) %{_bindir}/bouncesaying
%attr(0755,root,qmail) %{_bindir}/condredirect
%attr(0755,root,qmail) %{_bindir}/datemail
%attr(0755,root,qmail) %{_bindir}/elq
%attr(0755,root,qmail) %{_bindir}/except
%attr(0755,root,qmail) %{_bindir}/forward
%attr(0755,root,qmail) %{_bindir}/maildir2mbox
%attr(0755,root,qmail) %{_bindir}/maildirmake
%attr(0755,root,qmail) %{_bindir}/maildirwatch
%attr(0755,root,qmail) %{_bindir}/mailq
%attr(0755,root,qmail) %{_bindir}/mailsubj
%attr(0755,root,qmail) %{_bindir}/make-owners
%attr(0755,root,qmail) %{_bindir}/pinq
%attr(0755,root,qmail) %{_bindir}/predate
%attr(0755,root,qmail) %{_bindir}/preline
%attr(0755,root,qmail) %{_bindir}/qail
%attr(0755,root,qmail) %{_bindir}/qbiff
%attr(0755,root,qmail) %{_bindir}/qreceipt
%attr(0755,root,qmail) %{_bindir}/qsmhook
%attr(0755,root,qmail) %{_bindir}/tcp-env
%attr(0711,root,qmail) %{_bindir}/qmail-clean
%attr(0711,root,qmail) %{_bindir}/qmail-getpw
%attr(0755,root,qmail) %{_bindir}/qmail-inject
%attr(0711,root,qmail) %{_bindir}/qmail-local
%attr(0700,root,qmail) %{_bindir}/qmail-lspawn
%attr(0700,root,qmail) %{_bindir}/qmail-newmrh
%attr(0700,root,qmail) %{_bindir}/qmail-newu
%attr(0711,root,qmail) %{_bindir}/qmail-pw2u
%attr(0755,root,qmail) %{_bindir}/qmail-qread
%attr(0755,root,qmail) %{_bindir}/qmail-qstat
%attr(4711,qmailq,qmail) %{_bindir}/qmail-queue
%attr(0755,root,qmail) %{_bindir}/qmail-qmqpc
%attr(0700,root,qmail) %{_bindir}/qmail-reload
%attr(0711,root,qmail) %{_bindir}/qmail-remote
%attr(0711,root,qmail) %{_bindir}/qmail-rspawn
%attr(0711,root,qmail) %{_bindir}/qmail-send
%attr(0711,root,qmail) %{_bindir}/qmail-todo
%attr(0755,root,qmail) %{_bindir}/qmail-showctl
%attr(0700,root,qmail) %{_bindir}/qmail-start
%attr(0755,root,qmail) %{_bindir}/qmail-tcpok
%attr(0755,root,qmail) %{_bindir}/qmail-tcpto

/usr/lib/sendmail
%{_sbindir}/ipmeprint
%{_sbindir}/sendmail
%{_sbindir}/splogger

%{_mandir}/man1/*
#%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/qmail-[a-n]*
%{_mandir}/man8/qmail-pw*
%{_mandir}/man8/qmail-qread*
%{_mandir}/man8/qmail-qstat*
%{_mandir}/man8/qmail-qmqpc*
%{_mandir}/man8/qmail-queue*
%{_mandir}/man8/qmail-r*
%{_mandir}/man8/qmail-send*
%{_mandir}/man8/qmail-showctl*
%{_mandir}/man8/qmail-start*
%{_mandir}/man8/qmail-t*
%{_mandir}/man8/[a-pr-z]*
%{_var}/qmail/alias
%{_var}/qmail/bin
%{_var}/qmail/control
%{_var}/qmail/doc
%{_var}/qmail/man
%{_var}/qmail/owners
%{_var}/qmail/queue
%{_var}/qmail/users

%attr(0750,root,root) %{_prefix}/share/qmail/create-config-qmail
%attr(0750,root,root) %{_prefix}/share/qmail/create-log-config-qmail
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.qmail
%attr(0700,qmaillog,qmail) %dir %{_var}/log/qmail

%files smtpd
%defattr(-,root,qmail)
%attr(0755,root,root) %config %{_sysconfdir}/init.d/qmail-smtpd
/sbin/rcqmail-smtpd
%attr(0755,root,qmail) %{_bindir}/qmail-smtpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/qmail-smtpd
%attr(1755,root,root) %dir %{_sysconfdir}/qmail-smtpd
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-smtpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-smtpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-smtpd/rules
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-smtpd/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-smtpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-smtpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-smtpd/log/down
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-smtpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-smtpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-smtpd/rules/data.cdb
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/qmail-smtpd
%endif
%attr(0750,root,root) %{_prefix}/share/qmail/create-config-qmail-smtpd
%attr(0750,root,root) %{_prefix}/share/qmail/create-log-config-qmail-smtpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.qmail-smtpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/qmail-smtpd
%{_mandir}/man8/qmail-smtpd*


%files qmtpd
%attr(0755,root,root) %config %{_sysconfdir}/init.d/qmail-qmtpd
/sbin/rcqmail-qmtpd
%attr(0755,root,qmail) %{_bindir}/qmail-qmtpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/qmail-qmtpd
%attr(1755,root,root) %dir %{_sysconfdir}/qmail-qmtpd
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmtpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmtpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmtpd/rules
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qmtpd/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qmtpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-qmtpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-qmtpd/log/down
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmtpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmtpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmtpd/rules/data.cdb
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/qmail-qmtpd
%endif
%attr(0750,root,root) %{_prefix}/share/qmail/create-config-qmail-qmtpd
%attr(0750,root,root) %{_prefix}/share/qmail/create-log-config-qmail-qmtpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.qmail-qmtpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/qmail-qmtpd
%{_mandir}/man8/qmail-qmtpd*


%files qmqpd
%defattr(-,root,qmail)
%attr(0755,root,root) %config %{_sysconfdir}/init.d/qmail-qmqpd
/sbin/rcqmail-qmqpd
%attr(0755,root,qmail) %{_bindir}/qmail-qmqpd
%attr(0644,root,root) %{_sysconfdir}/permissions.d/qmail-qmqpd
%attr(1755,root,root) %dir %{_sysconfdir}/qmail-qmqpd
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmqpd/env
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmqpd/log
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-qmqpd/rules
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qmqpd/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-qmqpd/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-qmqpd/down
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-qmqpd/log/down
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmqpd/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmqpd/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-qmqpd/rules/data.cdb
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/qmail-qmqpd
%endif
%attr(0750,root,root) %{_prefix}/share/qmail/create-config-qmail-qmqpd
%attr(0750,root,root) %{_prefix}/share/qmail/create-log-config-qmail-qmqpd
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.qmail-qmqpd
%attr(0700,qmaillog,qmail) %dir %{_var}/log/qmail-qmqpd
%{_mandir}/man8/qmail-qmqpd*


%files pop3d
%defattr(-,root,qmail)
%attr(0755,root,root) %config %{_sysconfdir}/init.d/qmail-pop3d
/sbin/rcqmail-pop3d
%attr(0755,root,qmail) %{_bindir}/qmail-pop3d
%attr(0711,root,qmail) %{_bindir}/qmail-popup
%attr(0644,root,root) %{_sysconfdir}/permissions.d/qmail-pop3d
%attr(1755,root,root) %dir %{_sysconfdir}/qmail-pop3d
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-pop3d/env
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-pop3d/log
%attr(0755,root,root) %dir %{_sysconfdir}/qmail-pop3d/rules
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-pop3d/run
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/qmail-pop3d/log/run
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-pop3d/down
%attr(0644,root,root) %ghost %{_sysconfdir}/qmail-pop3d/log/down
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-pop3d/rules/Makefile
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-pop3d/rules/data
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/qmail-pop3d/rules/data.cdb
%if 0%{?with_susefirewall_config}
%attr(0644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/qmail-pop3d
%endif
%attr(0750,root,root) %{_prefix}/share/qmail/create-config-qmail-pop3d
%attr(0750,root,root) %{_prefix}/share/qmail/create-log-config-qmail-pop3d
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.qmail-pop3d
%attr(0700,qmaillog,qmail) %dir %{_var}/log/qmail-pop3d
%{_mandir}/man8/qmail-pop*


%changelog
* Wed Apr 28 2010 Bernhard Graf <graf@movingtarget.de> 1.03-56
- fixed Requires for current openSUSE
- added Provides: smtp_daemon to qmail base package
* Mon Apr 28 2008 Bernhard Graf <graf@movingtarget.de> 1.03-55
- moved back executables from /sbin to /usr/bin
* Fri Feb 29 2008 Bernhard Graf <graf@movingtarget.de>
- refactored configuration file layout
- added link-sync patch
- optionally link with dietlibc (--with dietlibc)
- optionally build queue for reiserfs (--with reiserfs)
- optionally disable link-sync patvh (--with nolinksync)
- RPM group according to openSUSE specs
- removed SuSEconfig configuration setup - configuration is now created
  when the service is started
- automatically open SuSEfirewall for the respective daemons on SuSE >=10.3
* Tue May 17 2005 Bernhard Graf <graf@movingtarget.de>
- removed logging from realrcptto code (already done by smtp-logging patch)
- updated config/setup to handle CHKRCPT
* Tue May 17 2005 Bernhard Graf <graf@movingtarget.de>
- added Paus Jarc's realrcptto patch to movingtarget base patch
* Mon Mar 28 2005 Bernhard Graf <graf@movingtarget.de>
- applied mtbulkmailer.patch which contains
  + big-todo.patch (handle big volumes of queue inserts)
  + random_ip_bind.patch (randomly bind to one of local ips)
* Fri Mar 25 2005 Bernhard Graf <graf@movingtarget.de>
- qmail + movingtarget base patch
* Wed Feb 11 2004 Bernhard Graf <graf@movingtarget.de>
- moved service directories from /etc/qmail/service to /var/service
* Tue Nov 25 2003 Bernhard Graf <graf@movingtarget.de>
- update to SuSE 9.0 / rpm 4.1.1
* Tue Sep 02 2003 Bernhard Graf <graf@movingtarget.de>
- update to SuSE 8.2
- SuSEconfig scripts
* Sun Feb 09 2003 Bernhard Graf <graf@adjoli.de>
- Bug fix in /usr/share/qmail/log-functions: Make "/" work in $service
* Mon Jan 28 2002 Bernhard Graf <graf@adjoli.de>
- this spec file can build optimized versions for extfs and reiserfs now
- added creation of /etc/qmail/users/cdb in %post
* Fri Jan 25 2002 Bernhard Graf <graf@adjoli.de>
- renamed resulting packages to qmailreiser* to reflect appropriate filesystem
- Improved the multilog setup (be able to set different n and s options)
- fixed uninstall error messages
* Thu Jan 10 2002 Bernhard Graf <graf@adjoli.de>
- moved qmqpc from package qmqpd to package qmail
* Fri Sep 21 2001 Bernhard Graf <graf@augensalat.de>
- removed checkpassword from package
- using SuSE's insserv and fillup installation tools
- fixed a bug where altering inetd.conf
* Sun Aug 12 2001 Bernhard Graf <graf@augensalat.de>
- changed svscan service directory location to /etc/service
- cosmetic changes in SPEC file
- improved add_user and add_groups functions
* Sun Jun 03 2001 Alistair Cloete <acloete@yahoo.com> 1.03+patches-18jojo1
- added 'Provides: smtp_daemon' for SuSE
- added explicit uids and gids
- changed 'Requires: initscripts' to aaa_base
- changed 'Requires: shadow_utils' to shadow
