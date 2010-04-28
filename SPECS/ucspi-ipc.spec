#
# spec file for package ucspi-ipc (Version 0.67)
#
# Copyright  (c)  2008 - 2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define package_name    ucspi-ipc
%define version         0.67
%define release         1

Name:           %{package_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	An UCSPI protocol for the local communication domain
License:	unknown, contact author
Group:		Productivity/Networking/System
Autoreqprov:	on
Source:		http://www.superscript.com/ucspi-ipc/%{name}-%{version}.tar.gz
Patch:		%{name}-%{version}-fhs.patch
BuildRoot:	%{_tmppath}/ucspi-ipc-%{version}-%(id -nu)
BuildRequires:	c_compiler make patch binutils coreutils
URL:		http://www.superscript.com/ucspi-ipc/intro.html

%description
ipcserver and ipcclient are command-line tools for building local-domain
client-server applications. They conform to the UNIX Client-Server Program
Interface, UCSPI.

ipcserver listens for connections on a local-domain stream socket, and runs
a program for each connection it accepts. The program environment includes
variables that hold the local and remote socket addresses, and the
effective user and group IDs of the process that called connect. ipcserver
offers a concurrency limit on acceptance of new connections, and selective
handling of connections based on client identity.

ipcclient requests a connection to a local-domain socket, and runs a
program. The program environment includes a variable that holds the local
socket address.

Author:
-------
    William E. Baxter

%prep
%setup -q -n host/superscript.com/net/%{name}-%{version}
%patch
echo gcc -D_GNU_SOURCE $RPM_OPT_FLAGS >src/conf-cc
echo gcc "$RPM_OPT_FLAGS -s" >src/conf-ld

%build
package/compile
package/rts

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}

for n in $(cat package/commands-base package/commands-ipcperl) ; do
  %{__install} -m 0755 command/$n %{buildroot}%{_bindir}
  echo "%attr(0775,root,root) %{_bindir}/$n" >>commandfiles
done

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%files -f commandfiles
%defattr(-,root,root)
%doc src/CHANGES src/TODO

%changelog
* Wed Apr 28 2010 Bernhard Graf <graf@movingtartget.de> 0.67-1
- make it build with glibc 2.10+
* Wed Jan 30 2008 Bernhard Graf <graf@movingtartget.de> 0.67-0
- initial wrap
