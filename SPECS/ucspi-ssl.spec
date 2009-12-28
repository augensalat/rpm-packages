#
# spec file for package ucspi-ssl (Version 0.70)
#
# Copyright  (c)  2004-2008  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define package_name	ucspi-ssl
%define version		0.70
%define release		1

Name:		%{package_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	TCP client-server command-line tools with SSL support
License:	unknown, contact author
Group:		Productivity/Networking/System
Source:		http://www.superscript.com/ucspi-ssl/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -u -n)
BuildRequires:	c_compiler make patch binutils coreutils
BuildRequires:	openssl openssl-devel openssl-certs
Requires:	openssl openssl-certs
URL:		http://www.superscript.com/ucspi-ssl/intro.html

%define ssldir	/etc/ssl

%description
sslserver and sslclient are command-line tools for building SSL
client-server applications. They conform to the UNIX Client-Server Program
Interface, UCSPI.

sslserver listens for connections, and runs a program for each connection
it accepts. The program environment includes variables that hold the local
and remote host names, IP addresses, and port numbers. sslserver offers a
concurrency limit on acceptance of new connections, and selective handling
of connections based on client identity.

sslclient requests a connection to a TCP socket, and runs a program. The
program environment includes the same variables as for sslserver.

Author:
-------
    William E. Baxter

%debug_package

%prep
%setup -q -n host/superscript.com/net/%{name}-%{version}

echo gcc $RPM_OPT_FLAGS >src/conf-cc
# echo gcc "$RPM_OPT_FLAGS -lcrypto -lssl -s" >src/conf-ld
echo gcc >src/conf-ld
echo "%{ssldir}/certs" >src/conf-cadir
echo "%{ssldir}/%{package_name}/dh1024.pem" >src/conf-dhfile
echo "%{_bindir}" >src/conf-tcpbin

%build
package/compile
package/rts

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}

for n in $(cat package/commands-base package/commands-sslperl); do
  %{__install} -m 0755 command/$n %{buildroot}%{_bindir}
  echo "%attr(0775,root,root) %{_bindir}/$n" >>commandfiles
done
%{__mkdir_p} %{buildroot}%{ssldir}/%{package_name}
touch %{buildroot}%{ssldir}/%{package_name}/dh1024.pem
%{__mkdir_p} %{buildroot}/etc/cron.daily
cat >%{buildroot}/etc/cron.daily/%{package_name} <<ETX
#!/bin/sh
# generate a new SSL DH key
umask 077
RANDFILE=\$(mktemp rand.XXXXXX)
ps axwww >/tmp/\$RANDFILE
openssl dhparam -rand /tmp/\$RANDFILE -out %{ssldir}/%{package_name}/dh1024.pem.new 1024 2>/dev/null && \
mv -f %{ssldir}/%{package_name}/dh1024.pem.new %{ssldir}/%{package_name}/dh1024.pem || \
rm -f %{ssldir}/%{package_name}/dh1024.pem.new
%{__rm} -f /tmp/\$RANDFILE
ETX
chmod 0755 %{buildroot}/etc/cron.daily/%{package_name}

umask 077
RANDFILE=$(mktemp rand.XXXXXX)
ps axwww >/tmp/$RANDFILE
openssl dhparam -rand /tmp/$RANDFILE -out %{buildroot}%{ssldir}/%{package_name}/dh1024.pem 1024
%{__rm} -f /tmp/$RANDFILE

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%files -f commandfiles
%defattr(-,root,root)
%doc src/CHANGES package/README src/TODO src/UCSPI-SSL
%attr (0755,root,root) /etc/cron.daily/%{package_name}
%attr (0700,root,root) %config(noreplace,missingok) %verify(not md5 size mtime) %{ssldir}/%{package_name}/dh1024.pem

%changelog
* Tue Mar 18 2008 Bernhard Graf <graf@movingtartget.de>
- cron job to create new dh1024 file once a day
* Wed Jan 30 2008 Bernhard Graf <graf@movingtartget.de>
- updated to version 0.70
- RPM group conforming to OpenSuSE spec
* Sun Feb 06 2005 Bernhard Graf <graf@movingtarget.de>
- updated to version 0.68
* Sun Mar 07 2004 Bernhard Graf <graf@movingtarget.de>
- create dh1024.pem in %post stage
* Wed Jan 21 2004 Bernhard Graf <graf@movingtarget.de>
- initial wrap
