#
# spec file for package webalizer-run (Version 0.01)
# 
# Copyright  (c)  2005 - 2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# 

%define package_name	webalizer-run
%define version		0.01
%define release		2

Name:		%{package_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	run a daemon that feeds Apache logs to webalizer
License:	Artistic License
Group:		Development/Libraries/Perl
Source:		%{package_name}-%{version}.tar.gz
BuildRequires:	perl
Requires:	perl = %{perl_version}
Requires:	daemontools >= 0.76, webalizer >= 2.0, supervise-scripts
BuildRoot:	%{_tmppath}/%{name}-%{version}-%(id -nu)

%description
"webalizer-run" must be executed by supervise(8) (or a similar program).
It waits for Apache type log files to appear in "$ENV{INPUTDIR}/new". It
periodically checks for new content in "$ENV{INPUTDIR}/new", the time
period can be set with $ENV{TIMER}. Moreover it can be triggerd by writing
arbitrary data to a FIFO named by $ENV{TRIGGER}, the FIFO is created by
"webalizer-run" if it does not exist.

Authors:
--------
    Bernhard Graf <graf-webalizer-run@movingtarget.de>

%prep
%setup -n %{package_name}-%{version}

%build
%{__perl} Makefile.PL
%{__make}
%{__make} test

%install
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}
%perl_make_install
%perl_process_packlist

%{__mkdir_p} %{buildroot}/etc/webalizer/{env,log}
%{__mkdir_p} %{buildroot}/var/lib/webalizer/logs/{cur,new,tmp}
%{__install} -d -m2755 %{buildroot}/srv/www/webalizer
%{__install} -d -m0755 %{buildroot}/var/log/www/webalizer

cat <<ETX >%{buildroot}/etc/webalizer/run
#!/bin/sh
exec 2>&1
exec envdir /etc/webalizer/env envuidgid nobody %{_bindir}/webalizer-run
ETX

cat <<ETX >%{buildroot}/etc/webalizer/log/run
#!/bin/sh
exec setuidgid nobody multilog t /var/log/www/webalizer
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/INPUTDIR
/var/lib/webalizer/logs

Directory to be monitored for logfiles.
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/OUTPUTDIR
/srv/www/webalizer

Directory for webalizer(1) output.
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/NICENESS
20

nice(1) level for webalizer
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/TIMER
1800

Time period in seconds that passes before webalizer-run re-checks the
input directory
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/TRIGGER
/var/run/webalizer-run

Path to trigger FIFO
ETX

cat <<ETX >%{buildroot}/etc/webalizer/env/WEBALIZERCONF
/srv/www/webalizer.conf

Configuration file to use with the webalizer(1)
ETX

%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}

%post
test -L /service/webalizer || svc-add /etc/webalizer >/dev/null

%preun
# stop and remove service
if test -L /service/webalizer ; then
  svc-remove webalizer
  %{__rm} -fr /etc/webalizer/supervise
  %{__rm} -fr /etc/webalizer/log/supervise
fi

%files
%defattr(-,root,root)
%doc Changes README
%doc %{_mandir}/man1/*
%{_bindir}/*
%{perl_vendorarch}/auto/%{package_name}
/var/adm/perl-modules/%{package_name}
%attr(1755,nobody,nobody) /etc/webalizer
%attr(0755,nobody,nobody) /var/lib/webalizer/logs
%attr(2755,nobody,nobody) %dir /srv/www/webalizer
%attr(0755,nobody,nobody) %dir /var/log/www/webalizer


%changelog -n %{name}
* Thu Nov 26 2009 - Bernhard Graf <graf@movingtarget.de> - 0.01-2
- fixed SPEC file for RPM 4
- moved stuff from /var/service/webalizer to /etc/webalizer
* Fri Apr 15 2005 - Bernhard Graf <graf@movingtarget.de> - 0.01-1
- initial rpm 0.01
