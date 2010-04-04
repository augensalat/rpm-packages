#
# spec file for package bglibs (Version 1.106)
#
# Copyright  (c)  2004-2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name		bglibs
%define version		1.106
%define release		0

Name:		%{name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	BG Libraries Collection
License:	GPL
Group:		Development/Libraries
Source:		http://untroubled.org/bglibs/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-buildroot
URL:		http://untroubled.org/bglibs/

%description
BG Libraries Collection

Author:
-------
    Bruce Guenter <bruceg@em.ca>

%prep
%setup
echo gcc "%{optflags}" -g >conf-cc
echo gcc '-g -L.' >conf-ld
echo %{_bindir} >conf-bin
echo %{_includedir}/%{name} >conf-include
echo %{_libdir}/%{name} >conf-lib
echo %{_mandir} >conf-man

%build
%{__make}

%install
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}
%{__make} install_prefix=%{buildroot} install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && %{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc ANNOUNCEMENT COPYING NEWS README doc/*
%doc %{_mandir}/*/*
%{_bindir}/*
%{_includedir}/%{name}
%{_libdir}/%{name}
%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%changelog
* Thu Apr 02 2009 Bernhard Graf <graf@movingtarget.de>
- updated to v1.106
* Mon Nov 03 2008 Bernhard Graf <graf@movingtarget.de>
- updated to v1.104
* Fri Jan 18 2008 Bernhard Graf <graf@movingtarget.de>
- updated to v1.102
* Tue Feb 21 2006 Bernhard Graf <graf@movingtarget.de>
- updated to v1.040
* Mon Dec 12 2005 Bernhard Graf <graf@movingtarget.de>
- updated to v1.031
* Mon Sep 19 2005 Bernhard Graf <graf@movingtarget.de>
- updated to v1.027
* Thu Jan 27 2005 Bernhard Graf <graf@movingtarget.de>
- updated to v1.019
* Fri Dec 12 2003 Bernhard Graf <graf@movingtarget.de>
- updated to v1.011
* Sun Aug 17 2003 Bernhard Graf <graf@movingtarget.de>
- gcc 3.3 patch for v1.009
- SPEC file cleanups
