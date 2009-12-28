#
# spec file for package ucspi-tcp (Version 0.88)
#
# Copyright  (c)  2001-2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name			ucspi-tcp
%define version                 0.88
%define release                 11

%define build_dietlibc	0
%define build_ssl	0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_dietlibc: %{expand: %%define build_dietlibc 1}}
%{?_with_ssl: %{expand: %%define build_ssl 1}}

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	TCP client-server command-line tools
License:	Public Domain
Group:		Productivity/Networking/System
Source:		http://cr.yp.to/ucspi-tcp/ucspi-tcp-%{version}.tar.gz
Source1:	maketcprules
Source2:	http://smarden.org/pape/djb/manpages/%{name}-%{version}-man.tar.gz
Patch0:		%{name}-%{version}.nodefaultrbl.patch
Patch1:		%{name}-ssl-20050405.patch
Patch2:		ftp://moni.csi.hu/pub/glibc-2.3.1/%{name}-%{version}.errno.patch
Patch3:		%{name}-%{version}-dietlibc-readwrite.patch
BuildRoot:	%{_tmppath}/ucspi-tcp-%{version}-%(id -u -n)
BuildRequires:	c_compiler make patch binutils coreutils
BuildRequires:	openssl openssl-devel openssl-certs
%if %{build_dietlibc}
BuildRequires:	dietlibc >= 0.30
%endif
Requires:	openssl openssl-certs
URL:		http://cr.yp.to/ucspi-tcp.html

%description
tcpclient and tcpserver are easy-to-use command-line tools for building
TCP client-server applications. tcpclient makes a TCP connection and
runs a program of your choice. tcpserver waits for incoming connections
and, for each connection, runs a program of your choice. Your program
receives environment variables showing the local and remote host names,
IP addresses, and port numbers.

tcpserver offers a concurrency limit to protect you from running out of
processes and memory. When you are handling 40 (by default) simultaneous
connections, tcpserver smoothly defers acceptance of new connections.

tcpserver also provides TCP access control features, similar to
tcp-wrappers/tcpd's hosts.allow but much faster. Its access control
rules are compiled into a hashed format with cdb, so it can easily deal
with thousands of different hosts.

tcpclient and tcpserver conform to UCSPI, the UNIX Client-Server Program
Interface, using the TCP protocol. UCSPI tools are available for several
different networks.

Author:
-------
    Dan J. Bernstein <djb@cr.yp.to>

%debug_package

%prep
%setup
%patch0 -p1
%if %{build_ssl}
%patch1
%else
%patch2 -p1
%endif

echo %{_exec_prefix} >conf-home
%setup -D -T -b 2
%if %{build_dietlibc}
%patch3
echo diet cc $RPM_OPT_FLAGS >conf-cc
echo diet cc >conf-ld
%else
echo cc $RPM_OPT_FLAGS >conf-cc
echo cc >conf-ld
%endif
%{__cp} %{S:1} .

%build
%{__make}

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_exec_prefix}

echo %{buildroot}%{_exec_prefix} >conf-home
%{__rm} -f install.o auto_home.o install
%{__make} install
./install

%{__install} -m 755 maketcprules %{buildroot}%{_exec_prefix}/bin
%{__install} -d %{buildroot}/etc/tcpcontrol
%if %{build_ssl}
  %{__rm} -fr %{buildroot}%{_exec_prefix}/man/cat?
  if test "%{_exec_prefix}/man" != "%{_mandir}" ; then
    %{__install} -d %{buildroot}%{_mandir}
    %{__mv} %{buildroot}%{_exec_prefix}/man/* %{buildroot}%{_mandir}
  fi
%else
  %{__install} -d %{buildroot}%{_mandir}/man1
  %{__install} -m 644 ../ucspi-tcp-%{version}-man/*.1 %{buildroot}%{_mandir}/man1
%endif

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%post
%{_exec_prefix}/bin/maketcprules

%files
%defattr(-,root,root)
%doc CHANGES README TODO
%attr(0755,-,-) %dir /etc/tcpcontrol
%attr(0755,-,-) %{_exec_prefix}/bin/*
%{_mandir}/*/*

%changelog
* Thu Oct 15 2009 Bernhard Graf <graf@movingtarget.de> 0.88-11
- Bug fix: didn't build when not using dietlibc

* Thu Feb 21 2008 Bernhard Graf <graf@movingtarget.de> 0.88-10
- optionally link with dietlibc (--with dietlibc)
- optionally build with SSL support (--with ssl)
- build debug package

* Wed Jan 30 2008 Bernhard Graf <graf@movingtarget.de> 0.88-9
- applying Andre´ Oppermann's ucspi-tcp-ssl-patch

* Tue Jan 29 2008 Bernhard Graf <graf@movingtarget.de>
- adjusted RPM group to SuSE specs
- new License: Public Domain

* Sat May 24 2003 Bernhard Graf <graf@adjoli.de>
- tiny cleanups in the spec file

* Sat Feb 15 2003 Bernhard Graf <graf@adjoli.de>
- Mate's nobase patch didn't offer the desired behaviour, because it required
  an RBL (-r rbl). The new nodefaultrbl patch is usefull, if only $RBLSMTPD
  has to be checked (set from tcpcontrol).

* Fri Feb 14 2003 Bernhard Graf <graf@adjoli.de>
- included Mate Wierdl's errno and nobase patches

* Sun Aug 7 2001 Bernhard Graf <graf@augensalat.de>
- included Gerrit Pape's ucspi-tcp manpages
- commands install under /usr/sbin

* Mon Mar 20 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.88 of ucspi-tcp.

* Wed Mar 15 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.87 of ucspi-tcp.
- Added "obsoletes" line for rblsmtpd.

* Mon Mar 13 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.86 of ucspi-tcp.
- Added documentation tarball.

* Sun Nov 7 1999 Bruce Guenter <bruceg@em.ca>
- Fixed install race condition exposed on faster computers.

* Sat Nov 14 1998 Bruce Guenter <bruce.guenter@qcc.sk.ca>
- Upgraded package to version 0.84.

* Fri Jul 10 1998 Bruce Guenter <bruce.guenter@qcc.sk.ca>
- Configured the binaries to go into /usr/bin instead of /usr/sbin
- Fixed installation problem with tcpcat (and other shell scripts)

* Tue Jan 20 1998 Bruce Guenter <bruce.guenter@qcc.sk.ca>
- Copied the tcpcconfig program from the old tcpcontrol package,
  renaming it to maketcprules, which works like ldconfig, building all
  the .rules files in /etc/tcpcontrol into .cdb files.

