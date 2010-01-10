#
# spec file for package djbdns (Version 1.05)
#
# Copyright  (c)  2001-2010  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name			djbdns
%define version                 1.05
%define release                 13

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	Domain Name System server and tools
License:	Copyright 2000 D. J. Bernstein <djb@cr.yp.to>
URL:		http://cr.yp.to/djbdns.html
Packager:	Bernhard Graf <graf@movingtarget.de>
Group:		Productivity/Networking/DNS/Servers
Source0:	http://cr.yp.to/djbdns/djbdns-%{version}.tar.gz
Source1:	http://smarden.org/pape/djb/manpages/djbdns-%{version}-man.tar.gz
Source2:	djbdns-%{version}-init.tar.bz2
Patch0:		djbdns-%{version}-fhs.patch
Patch1:		djbdns-%{version}-man-fhs.patch
Patch2:		djbdns-%{version}-rootservers.patch
Patch3:		http://www.iecc.com/rbldns-patch.txt
Patch4:		djbdns-%{version}-thirdpartypoisoning.patch
PreReq:		%insserv_prereq
BuildRequires:	c_compiler make patch binutils coreutils
BuildRoot:	%{_tmppath}/djbdns-%{version}-%(id -nu)

%description
djbdns is a collection of Domain Name System tools.

%package dnscache
Summary:	Caching nameserver
Group:		Productivity/Networking/DNS/Servers
Requires:	supervise-scripts >= 3.4-2
URL:		http://cr.yp.to/djbdns/dnscache.html
%description dnscache
dnscache is a local DNS cache. It accepts recursive DNS queries from
local clients such as web browsers and mail transfer agents. It collects
responses from remote DNS servers. It caches the responses to save time
later.

%package tinydns
Summary:	tinydns DNS server
Group:		Productivity/Networking/DNS/Servers
Requires:	supervise-scripts >= 3.4-2
URL:		http://cr.yp.to/djbdns/tinydns.html
%description tinydns
tinydns is a DNS server. It accepts iterative DNS queries from hosts
around the Internet, and responds with locally configured information.

%package pickdns
Summary:	load-balancing DNS server
Group:		System Environment/Daemons
Requires:	supervise-scripts >= 3.4-2
URL:		http://cr.yp.to/djbdns/pickdns.html
%description pickdns
pickdns is a load-balancing DNS server. It accepts iterative DNS queries
from hosts around the Internet, and responds with a dynamic selection of
locally configured IP addresses with 5-second TTLs.

In versions 1.04 and above, the features of pickdns have been integrated
into tinydns.

%package walldns
Summary:	reverse DNS wall
Group:		Productivity/Networking/DNS/Servers
Requires:	supervise-scripts >= 3.4-2
URL:		http://cr.yp.to/djbdns/walldns.html
%description walldns
walldns is a reverse DNS wall. It accepts iterative DNS queries for
in-addr.arpa domains from hosts around the Internet, and supplies
generic responses that avoid revealing local host information.

For example, walldns provides a PTR record for 4.3.2.1.in-addr.arpa
showing 4.3.2.1.in-addr.arpa as the name of IP address 1.2.3.4, and a
matching A record showing 1.2.3.4 as the IP address of
4.3.2.1.in-addr.arpa.

%package rbldns
Summary:	IP-address-listing DNS server
Group:		Productivity/Networking/DNS/Servers
Requires:	supervise-scripts >= 3.4-2
URL:		http://cr.yp.to/djbdns/rbldns.html
%description rbldns
rbldns is an IP-address-listing DNS server. It accepts iterative DNS
queries from hosts around the Internet asking about various IP
addresses. It provides responses showing whether the addresses are on a
locally configured list, such as RBL or DUL.

%package axfrdns
Summary:	DNS zone-transfer server
Group:		Productivity/Networking/DNS/Servers
Requires:	supervise-scripts >= 3.4-2
Requires:	ucspi-tcp >= 0.88
URL: http://cr.yp.to/djbdns/axfrdns.html
%description axfrdns
axfrdns is a DNS zone-transfer server. It reads a zone-transfer request
in DNS-over-TCP format from its standard input, and responds with
locally configured information.

%package tools
Summary:	Domain Name System tools
Group:		Productivity/Networking/DNS/Utilities
URL:		http://cr.yp.to/djbdns/tools.html
%description tools
* dnsip prints the IP addresses of a fully qualified domain name.
* dnsipq prints the fully qualified domain name and IP addresses of a
  short host name.
* dnsname does a reverse lookup for the IP address a.b.c.d. and prints
  the first domain name for that address.
* dnsfilter reads a series of lines from stdin, converts an IP address
  to a host name at the beginning of each line, and prints the results
  to stdout.
* dnsmx prints the MX records of a fully qualified domain name.
* dnstxt prints the TXT record of a fully qualified domain name.
* dnsqr asks for records of a certain type under a fully qualified
  domain name. type can be any, a, ns, mx, ptr, txt, cname, soa, hinfo,
  rp, sig, key, aaaa, axfr.
* dnsq sends a non-recursive DNS query to a DNS server for a certain
  records under a fully qualified domain name.
* dnstrace searches for all DNS servers that can affect the resolution
  of a certain record under a fully qualified domain name, starting from
  a root server.
* dnstracesort provides human-friendly output of dnstrace's output.

%prep
%setup
%setup -D -T -a 1
%setup -D -T -a 2
%patch0 -p1
%patch1
%patch2
%patch3 -p1
%patch4
echo %{_exec_prefix} >conf-home

%build
%{__make}

%install
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%{__mkdir_p} %{buildroot}%{_exec_prefix}
%{__mkdir_p} %{buildroot}/etc
echo %{buildroot}%{_exec_prefix} >conf-home
%{__rm} -f auto_home.o auto_home.c hier.o install instcheck
%{__perl} -pi -le 's!/!'%{buildroot}'!' hier.c
%{__make} install instcheck
./install
./instcheck

for section in 1 5 8; do
  mandir=%{buildroot}%{_mandir}/man$section
  %{__mkdir_p} $mandir
  %{__install} -m 444 djbdns-man/*.$section $mandir
done

%{__mkdir_p} %{buildroot}%{_sbindir}
initdir=%{buildroot}/etc/init.d
%{__mkdir_p} $initdir
for file in axfrdns dnscache pickdns rbldns tinydns walldns
do
  %{__install} -m 755 djbdns-%{version}-init/init/$file $initdir
  %{__ln_s} ../../etc/init.d/$file %{buildroot}%{_sbindir}/rc$file
done

%pre dnscache
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/dnscache -s /bin/true dnscache 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post dnscache
install_count=$1
%{fillup_and_insserv -fy dnscache}
if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Local DNS cache:
Create the service directory by running the dnscache-conf program:
    dnscache-conf dnscache dnslog /etc/dnscache
Tell svscan about the new service:
    svc-add /etc/dnscache
svscan will start the service within five seconds.
Finally, replace the nameserver line in /etc/resolv.conf with
    nameserver 127.0.0.1

External DNS cache:
Create the service directory by running the dnscache-conf program, with
your IP address (in this example: 1.2.3.4) at the end of the line:
    dnscache-conf dnscache dnslog /etc/dnscachex 1.2.3.4
Tell svscan about the new service:
    svc-add /etc/dnscachex
svscan will start the service within five seconds.

By default, dnscache does not accept queries from remote hosts. Use
    touch /etc/dnscachex/root/ip/1.2.3
to tell dnscache to accept queries from 1.2.3.*.
You can add or remove networks on the fly.
Tell other clients to use the external cache by adding
    nameserver 1.2.3.4
to their /etc/resolv.conf.
ETX
else
  %{__cat} <<ETX
You can restart dnscache with
    rcdnscache restart
ETX
fi

%preun dnscache
test "$1" = 0 -a -L /service/dnscache && svc-remove dnscache || true

%postun dnscache
%{restart_on_update dnscache}
%{insserv_cleanup}
test "$1" = 0 && userdel dnscache >/dev/null 2>&1 || true

%files dnscache
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/dnscache
%{_sbindir}/rcdnscache
%config /etc/dnsroots.global
%{_exec_prefix}/bin/dnscache*
%{_mandir}/man8/dnscache*
%doc CHANGES README TODO VERSION

%pre tinydns
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/tinydns/root -s /bin/bash tinydns 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post tinydns
install_count=$1
%{fillup_and_insserv -fy tinydns}

if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Create the service directory by running the tinydns-conf program
with your IP address at the end of the line:
    tinydns-conf tinydns dnslog /etc/tinydns 1.2.3.5
Tell svscan about the new service:
    svc-add /etc/tinydns
svscan will start the service within five seconds.

Information how to configure tinydns can by found at
http://cr.yp.to/djbdns.html
ETX
else
  %{__cat} <<ETX
You can restart tinydns with
    rctinydns restart
ETX
fi

%preun tinydns
test "$1" = 0 -a -L /service/tinydns && svc-remove tinydns || true

%postun tinydns
%{restart_on_update tinydns}
%{insserv_cleanup}
test "$1" = 0 && userdel tinydns >/dev/null 2>&1 || true

%files tinydns
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/tinydns
%{_sbindir}/rctinydns
%{_exec_prefix}/bin/tinydns*
%{_mandir}/man8/tinydns*
%doc CHANGES README TINYDNS TODO VERSION

%pre walldns
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/walldns -s /bin/true walldns 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post walldns
install_count=$1
%{fillup_and_insserv -fy walldns}

if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Create the service directory by running the walldns-conf program,
with your IP address at the end of the line:
    walldns-conf walldns dnslog /etc/walldns 1.2.4.5
Tell svscan about the new service:
    svc-add /etc/walldns
svscan will start the service within five seconds.

Information how to configure walldns can by found at
http://cr.yp.to/djbdns.html
ETX
else
  %{__cat} <<ETX
You can restart walldns with
    rcwalldns restart
ETX
fi

%preun walldns
test "$1" = 0 -a -L /service/walldns && svc-remove walldns || true

%postun walldns
%{restart_on_update walldns}
%{insserv_cleanup}
test "$1" = 0 && userdel walldns >/dev/null 2>&1 || true

%files walldns
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/walldns
%{_sbindir}/rcwalldns
%{_exec_prefix}/bin/walldns*
%{_mandir}/man8/walldns*
%doc CHANGES README TODO VERSION

%pre rbldns
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/rbldns -s /bin/true rbldns 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post rbldns
install_count=$1
%{fillup_and_insserv -fy rbldns}

if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Create the service directory by running the rbldns-conf program with
your IP address (in the example 1.2.3.6) at the end of the line:
    rbldns-conf rbldns dnslog /etc/rbldns 1.2.3.6 base
Tell svscan about the new service:
    svc-add /etc/rbldns
svscan will start the service within five seconds.

rbldns-conf creates /etc/rbldns/root/Makefile to run rbldns-data upon
request.

rbldns-conf arranges for rbldns to answer queries under the base domain.
The name base must not contain any special characters.

Information how to configure rbldns can by found at
http://cr.yp.to/djbdns.html
ETX
else
  %{__cat} <<ETX
You can restart rbldns with
    rcrbldns restart
ETX
fi

%preun rbldns
test "$1" = 0 -a -L /service/rbldns && svc-remove rbldns || true

%postun rbldns
%{restart_on_update rbldns}
%{insserv_cleanup}
test "$1" = 0 && userdel rbldns >/dev/null 2>&1 || true

%files rbldns
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/rbldns
%{_sbindir}/rcrbldns
%{_exec_prefix}/bin/rbldns*
%{_mandir}/man8/rbldns*
%doc CHANGES README TODO VERSION

%pre axfrdns
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/axfrdns -s /bin/true axfrdns 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post axfrdns
install_count=$1
%{fillup_and_insserv -fy axfrdns}

if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Create the service directory by running the axfrdns-conf program with
your IP address (in this example 1.2.3.5) at the end of the line:
    axfrdns-conf axfrdns dnslog /etc/axfrdns /etc/tinydns 1.2.3.5
Change directory to /etc/axfrdns, and add a line to tcp allowing zone
transfers to 9.8.7.6for the zones heaven.af.mil and 3.2.1.in-addr.arpa
(all examples here!):
    9.8.7.6:allow,AXFR="heaven.af.mil/3.2.1.in-addr.arpa"
Compile tcp into a binary format for tcpserver:
    make
Tell svscan about the new service:
    svc-add /etc/axfrdns
svscan will start the service within five seconds.

Information how to configure axfrdns can by found at
http://cr.yp.to/djbdns.html
ETX
else
  %{__cat} <<ETX
You can restart axfrdns with
    rcaxfrdns restart
ETX
fi

%preun axfrdns
test "$1" = 0 -a -L /service/axfrdns && svc-remove axfrdns || true

%postun axfrdns
%{restart_on_update axfrdns}
%{insserv_cleanup}
test "$1" = 0 && userdel axfrdns >/dev/null 2>&1 || true

%files axfrdns
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/axfrdns
%{_sbindir}/rcaxfrdns
%{_exec_prefix}/bin/axfr*
%{_mandir}/man8/axfr*
%doc CHANGES README TODO VERSION

%pre pickdns
groupadd -r nogroup 2>/dev/null || true
useradd -r -g nogroup -d %{_sysconfdir}/pickdns -s /bin/true pickdns 2>/dev/null || true
useradd -r -g nogroup -d %{_var}/log -s /bin/true dnslog 2>/dev/null || true

%post pickdns
install_count=$1
%{fillup_and_insserv -fy pickdns}

if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
Create the service directory by running the pickdns-conf program
with your IP address at the end of the line:
    pickdns-conf pickdns dnslog /etc/pickdns 1.2.3.7
Tell svscan about the new service:
    svc-add /etc/pickdns
svscan will start the service within five seconds.

pickdns is a load-balancing DNS server. It accepts iterative DNS queries
from hosts around the Internet, and responds with a dynamic selection of
locally configured IP addresses with 5-second TTLs.

In versions 1.04 and above, the features of pickdns have been integrated
into tinydns.

Information how to configure pickdns can by found at
http://cr.yp.to/djbdns/pickdns.html
ETX
else
  %{__cat} <<ETX
You can restart pickdns with
    rcpickdns restart
ETX
fi

%preun pickdns
test "$1" = 0 -a -L /service/pickdns && svc-remove pickdns || true

%postun pickdns
%{restart_on_update pickdns}
%{insserv_cleanup}
test "$1" = 0 && userdel pickdns >/dev/null 2>&1 || true

%files pickdns
%defattr(-,root,root)
%attr(0744,root,root) %config %{_sysconfdir}/init.d/pickdns
%{_sbindir}/rcpickdns
%{_exec_prefix}/bin/pickdns*
%{_mandir}/man8/pickdns*
%doc CHANGES README TODO VERSION

%files tools
%defattr(-,root,root)
%{_exec_prefix}/bin/dnsfilter
%{_exec_prefix}/bin/dnsip
%{_exec_prefix}/bin/dnsipq
%{_exec_prefix}/bin/dnsmx
%{_exec_prefix}/bin/dnsname
%{_exec_prefix}/bin/dnsq
%{_exec_prefix}/bin/dnsqr
%{_exec_prefix}/bin/dnstrace
%{_exec_prefix}/bin/dnstracesort
%{_exec_prefix}/bin/dnstxt
%{_exec_prefix}/bin/random-ip
%{_mandir}/man1/*
%{_mandir}/man5/*
%doc CHANGES README TODO VERSION

%clean
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"


%changelog
* Sun Jan 10 2010 Bernhard Graf <graf@movingtarget.de>
- applying security patch, see
  http://www.securityfocus.com/archive/1/501294/30/0/threaded
  http://article.gmane.org/gmane.network.djbdns/13864
* Tue Jan 29 2008 Bernhard Graf <graf@movingtarget.de>
- changed RPM groups to match SuSE (LSB?) standards
- using RPM macros fillup_and_insserv, insserv_cleanup and restart_on_update
- fixed several bugs in pre- and post-install scripts
* Mon Mar 29 2004 Bernhard Graf <graf@movingtarget.de>
- added patch to A and TXT records in the root of the rbldns server zone
* Thu Jan 29 2004 Bernhard Graf <graf@movingtarget.de>
- bugfix: move insserv call from %postun to %preun sections
* Sun Jan 18 2004 Bernhard Graf <graf@movingtarget.de>
- fixed init scripts: only tinydns provides named now
* Thu Nov 20 2003 Bernhard Graf <graf@movingtarget.de>
- patch dnsroots.global for new ip of j.root-servers.net
* Wed May 07 2003 Bernhard Graf <graf@movingtarget.de>
- for SuSE >8.0
- extended fhs-patch to make package compile with gcc 3.2 (errno issue)
* Sat Sep 22 2001 Bernhard Graf <graf@augensalat.de>
- using SuSE's insserv and fillup installation tools
* Thu Aug 10 2001 Bernhard Graf <graf@augensalat.de>
- split into sub packages:
  dnscache, tinydns, walldns, rbldns, axfrdns, pickdns, tools.
- patch for the *-conf programs to install logfiles in /var/log
- SuSE conformant start/stop scripts, automatic creation of suid users
- integrated Gerrit Pape's djbdns manpages.
* Mon Feb 12 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.05
* Mon Jan 22 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.04
* Sun Jan 7 2001 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.03
* Wed Oct 18 2000 Bruce Guenter <bruceg@em.ca>
- Renamed to djbdns.
- Updated to version 1.02
* Thu Mar 30 2000 Bruce Guenter <bruceg@em.ca>
- Moved all the RedHat specific stuff into a seperate "run" package.
* Wed Mar 29 2000 Bruce Guenter <bruceg@em.ca>
- Make the original conf programs retain their original names, and give
  the new programs the name *-rhconf.
* Sun Mar 26 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 1.00.
* Wed Mar 15 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.93.
* Mon Mar 6 2000 Bruce Guenter <bruceg@em.ca>
- Fixed a typo in the common init script.
* Thu Mar 2 2000 Bruce Guenter <bruceg@em.ca>
- Updated to version 0.91.
- Modified RPM specific files to use new directory structure.
- Added descriptions to the init.d scripts to fix problems with
  chkconfig.
* Sun Feb 20 2000 Bruce Guenter <bruceg@em.ca>
- Fixed some bugs in the init scripts and the redhat-conf script.
- Repackaged the RPM specific stuff into a seperate tarball.
* Tue Feb 15 2000 Bruce Guenter <bruceg@em.ca>
- Added init scripts to start any axfrdns, dnscache, pickdns, rbldns,
  tinydns, or walldns service.
* Mon Feb 14 2000 Bruce Guenter <bruceg@em.ca>
- Added RedHat specific *-conf script to put the log files in /var/log
- Added dnsip to list of programs in /usr/bin

