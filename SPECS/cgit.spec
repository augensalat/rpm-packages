#
# spec file for package cgit (Version 0.8.2.1)
#
# Copyright  (c)  2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define name        cgit
%define version     0.8.2.1
%define release     0.git6445
%define cachedir    %{_localstatedir}/cache/cgit
%define wwwdir      /srv/www/cgit
%define scriptdir   %{wwwdir}/cgi-bin
%define datadir     %{wwwdir}/htdocs
%define sharedir    %{_datadir}/cgit

%define make_cgit \
export CFLAGS="%{optflags}" \
make V=1 \\\
     DESTDIR=%{buildroot} \\\
     INSTALL="install -p"  \\\
     CACHE_ROOT=%{cachedir} \\\
     CGIT_VERSION=%{version} \\\
     CGIT_SCRIPT_PATH=%{scriptdir} \\\
     CGIT_SCRIPT_NAME=cgit \\\
     CGIT_DATA_PATH=%{datadir}

Name:		%{name}
Version:	%{version}
Release:        %{release}
Summary:        A fast webinterface for git
Group:          Development/Tools/Version Control
License:        GPLv2
URL:            http://hjemli.net/git/cgit/
Source0:        %{name}-%{version}.tar.bz2
Source1:        cgitrc
Source2:        cgit.apache2
Source3:        cgit.lighttpd
Source4:	cgit.head-include
Source5:	cgit.highlight-css
Source6:	cgit.about-html
Source7:	cgit.syntax-highlighting
Source8:	cgit.favicon
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  zlib-devel openssl openssl-devel
Requires:	openssl

%description
This is an attempt to create a fast web interface for the git scm,
using a builtin cache to decrease server io-pressure.

%package apache2
Summary:	Apache2 cgit configuration
Group:		Development/Tools/Version Control
Requires:	cgit = %{version}-%{release}
Requires:	apache2

%description apache2
Apache2 cgit configuration.

Actually this is more a demonstration how to do the configuring, thus
it is not required to install this package, if you want to run cgit with
Apache.

%package lighttpd
Summary:	Lighttpd cgit configuration
Group:		Development/Tools/Version Control
Requires:	cgit = %{version}-%{release}
Requires:	lighttpd

%description lighttpd
Lighttpd cgit configuration example.

By default the whole configuration is commented out, so this is more a
demonstration how to do the configuring, thus it is not required to
install this package, if you want to run cgit with Lighttpd.

%package highlight
Summary:	Syntax highlighting for cgit
Group:		Development/Tools/Version Control
Requires:	cgit = %{version}-%{release}
Requires:	highlight

%description highlight
cgit can be configured to do syntax highlighting with the help of an
external program. 

This setup uses (and requires) 'highlight' (http://www.andre-simon.de/)
to do the actual syntax highlighting.

%prep
%setup -q

%build
%{make_cgit}


%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%{make_cgit} install
install -d -m0755 %{buildroot}%{_sysconfdir}/apache2/conf.d
install -d -m0755 %{buildroot}%{_sysconfdir}/lighttpd/conf.d
install -d -m0755 %{buildroot}%{sharedir}/filters
install -d -m0755 %{buildroot}%{sharedir}/include
install -p -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cgitrc
install -p -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/apache2/conf.d/cgit.conf
install -p -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/lighttpd/conf.d/cgit.conf
install -p -m0644 %{SOURCE4} %{buildroot}%{sharedir}/include/head.html
install -p -m0644 %{SOURCE5} %{buildroot}%{datadir}/cgit-highlight.css
install -p -m0644 %{SOURCE6} %{buildroot}%{datadir}/about.html
install -p -m0755 %{SOURCE7} %{buildroot}%{sharedir}/filters/syntax-highlighting.sh
install -p -m0644 %{SOURCE8} %{buildroot}%{datadir}/favicon.ico
install -d -m0755 %{buildroot}%{cachedir}

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%post highlight
install_count=$1
if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
To enable syntax highlighting, please open /etc/cgitrc in an editor
and uncomment the following lines by removing the '#':

#head-include=/usr/share/cgit/include/head.html
#source-filter=/usr/share/cgit/filters/syntax-highlighting.sh

ETX
fi

%files
%defattr(-,root,root)
%doc COPYING README* cgitrc.5.txt
%config(noreplace) %{_sysconfdir}/cgitrc
%dir %attr(-,wwwrun,www) %{cachedir}
%dir %{datadir}
%config(noreplace) %{datadir}/favicon.ico
%config(noreplace) %{datadir}/cgit.png
%config(noreplace) %{datadir}/cgit.css
%config(noreplace) %{datadir}/about.html
%dir %{sharedir}
%dir %{sharedir}/include
%dir %{sharedir}/filters
%{scriptdir}/*

%files apache2
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/apache2/conf.d/cgit.conf

%files lighttpd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/cgit.conf

%files highlight
%defattr(-,root,root)
%attr(0755,-,-) %{sharedir}/filters/syntax-highlighting.sh
%config(noreplace) %{sharedir}/include/head.html
%config(noreplace) %{datadir}/cgit-highlight.css

%changelog
* Sat Aug 22 2009 Bernhard Graf <graf@movingtarget.de>
- ported to openSUSE
- separate packages for Apache2 and Lighttpd
- support for syntax highlighting in tree view (requires hightlight package)
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Sun Mar 15 2009 Todd Zullinger <tmz@pobox.com> - 0.8.2.1-1
- Update to 0.8.2.1
* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Sun Feb 01 2009 Todd Zullinger <tmz@pobox.com> - 0.8.2-1
- Update to 0.8.2
- Drop upstreamed Makefile patch
* Sun Jan 18 2009 Todd Zullinger <tmz@pobox.com> - 0.8.1-2
- Rebuild with new openssl
* Mon Jan 12 2009 Todd Zullinger <tmz@pobox.com> - 0.8.1-1
- Initial package
