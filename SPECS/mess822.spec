%define _unpackaged_files_terminate_build 0
%define pkgname mess822

Name:		%{pkgname}
Summary:	mess822 is a library for parsing Internet mail messages. 
Version:	0.58
Release:	1
License:	Public Domain
Group:		Utilities/System
Source:		ftp://cr.yp.to/software/%{name}-%{version}.tar.gz
Buildroot:	%{_tmppath}/%{name}-%{version}-%(id -u -n)
URL:		http://cr.yp.to/%{name}.html
Packager:	Bernhard Graf <graf@movingtarget.de>
Patch:		%{name}-%{version}.errno.patch
Distribution:	%(head -1 /etc/SuSE-release)

%description
mess822 is a library for parsing Internet mail messages. The mess822
package contains several applications that work with qmail:

   * ofmipd rewrites messages from dumb clients. It supports a database
     of recognized senders and From lines, using cdb for fast lookups.

   * new-inject is an experimental new version of qmail-inject. It
     includes a flexible user-controlled hostname rewriting mechanism.

   * iftocc can be used in .qmail files. It checks whether a known
     address is listed in To or Cc.

   * 822header, 822field, 822date, and 822received extract various
     pieces of information from a mail message.

   * 822print converts a message into an easier-to-read format.

mess822 supports the full complexity of RFC 822 address lists, including
address groups, source routes, spaces around dots, etc. It also supports
common RFC 822 extensions: backslashes in atoms, dots in phrases,
addresses without host names, etc. It extracts each address as an
easy-to-use string, with a separate string for the accompanying comment.

mess822 converts RFC 822 dates into libtai's struct caltime format. It
supports numeric time zones, the standard old-fashioned time zones, and
many nonstandard time zones.

mess822 is fast. For example, extracting 10000 addresses from a 160KB To
field takes less than a second on a Pentium-100.

%prep
%setup
%patch -p1

%build

echo %{_prefix} > conf-home
make prog

# Fix hier.c so that nothing gets installed
# in man/cat?.
awk '!/cat/ { sub("/etc","%{buildroot}/etc"); print}' hier.c > hier.c.tmp
%{__mv} hier.c.tmp hier.c

%install
test "%{buildroot}" != "/" && test -d %{buildroot} && %{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_prefix} %{buildroot}/etc %{buildroot}/%{_mandir}
# The next steps make sure that instcheck and install
# will do their job in %{buildroot}%{_prefix} and not
# in %{_prefix}

echo %{buildroot}%{_prefix} >conf-home

%{__make} install instcheck
./install
./instcheck
%{__mv} %{buildroot}%{_prefix}/man/* %{buildroot}/%{_mandir}
test "%{_lib}" == lib || %{__mv} %{buildroot}%{_prefix}/lib %{buildroot}%{_prefix}/%{_lib}

%clean
test "%{buildroot}" != "/" && test -d %{buildroot} && %{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BLURB CHANGES INSTALL README 
%doc THANKS TODO VERSION 
%{_prefix}/bin/*
%{_mandir}/*/*
%{_prefix}/include/*
%{_prefix}/%{_lib}/*
/etc/*

%changelog
* Sun Apr 04 2004 Bernhard Graf <graf@movingtarget.de>
- Initial wrap version 0.58

