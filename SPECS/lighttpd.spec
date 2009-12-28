#
# spec file for package lighttpd (Version 1.4.24)
#
# Copyright  (c)  2006 - 2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define pkg_name	lighttpd
%define pkg_user	wwwrun
%define pkg_group	www
%define pkg_home	/var/lib/%{pkg_name}
%define version		1.4.24
%define release         0
%define initdir		%{_sysconfdir}/init.d

%define with_tests 1
%define with_ipv6 0
%define with_ldap 0
%define with_ssl 0
%define with_enh_webdav 0
%define with_mod_magnet 1

# commandline overrides: rpm -ba|--rebuild --with 'xxx'
%{?_with_ipv6: %{expand: %%define with_ipv6 1}}
%{?_with_ldap: %{expand: %%define with_ldap 1}}
%{?_with_ssl: %{expand: %%define with_ssl 1}}
%{?_with_enh_webdav: %{expand: %%define with_enh_webdav 1}}

%if 0%{?sles_version} == 9
%define with_tests 0
%define with_enh_webdav 0
%endif
%if 0%{?suse_version} > 1020
%define with_susefirewall_config 1
%endif

Name:           %{pkg_name}
Version:        %{version}
Release:        %{release}
Distribution:   %(head -n1 /etc/SuSE-release)
Summary:	A fast webserver with minimal memory-footprint
License:	BSD
Group:		Productivity/Networking/Web/Servers
URL:		http://www.lighttpd.net/
Source:		http://www.lighttpd.net/download/%{pkg_name}-%{version}.tar.bz2
Source1:	%{pkg_name}-init-%{version}.tar.bz2
Source2:        lightytest.sh
Source3:        lighttpd.SuSEfirewall
Source4:        lighttpd-ssl.SuSEfirewall
Patch0:		lighttpd-1.4.20-proxy.patch
Patch2:         lighttpd-1.4.22_geoip.patch
# Patch3:		lighttpd-include-shell-waitpid.patch
BuildRequires:	c_compiler make libtool zlib-devel
BuildRequires:	pcre >= 3.1 pcre-devel >= 3.1
BuildRequires:  FastCGI-devel e2fsprogs-devel fam-devel gdbm-devel
BuildRequires:	libattr-devel libmemcache-devel libxml2-devel mysql-devel
BuildRequires:	openldap2-devel pkgconfig pwdutils
#
%if 0%{?with_enh_webdav}
BuildRequires:  sqlite-devel >= 3
%endif
#
%if 0%{?opensuse_bs}
BuildRequires:  lua51-devel
%define with_geoip 1
%else
BuildRequires:  lua-devel
%if 0%{sles_version}
%define with_mod_magnet 0
%endif
%endif
#
%if 0%{?with_geoip}
BuildRequires:  GeoIP-devel
%endif
#
%if 0%{?with_tests}
BuildRequires:  php5-fastcgi
%endif
#
%if 0%{?suse_version} < 1000
BuildRequires:  libstdc++-devel
%endif
%if 0%{?suse_version} > 1020
BuildRequires:  libbz2-devel
%endif
PreReq:         %insserv_prereq %fillup_prereq
Requires:	pcre >= 3.1 zlib
Requires:	daemontools supervise-scripts >= 3.2
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%(id -nu)

%description
lighttpd is intented to be a frontend for ad-servers which have to deliver
small files concurrently to many connections.

Author:
-------
    Jan Kneschke <jan@kneschke.de>

%debug_package

%package mod_cml
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        CML (Cache Meta Language) module for Lighttpd

%description mod_cml
CML is a Meta language to describe the dependencies of a page at one
side and building a page from its fragments on the oth er side using
LUA.

CML (Cache Meta Language) wants to solves several problems:

* dynamic content needs caching to perform

* checking if the content is dirty inside of the application is
   usually more expensive than sending out the cached data

* a dynamic page is usually fragmented and the fragments have
   different livetimes

* the different fragements can be cached independently

Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%package mod_magnet
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        A module to control the request handling in lighttpd

%description mod_magnet
A module to control the request handling in lighttpd.

It is the successor of mod_cml.



Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%package mod_mysql_vhost
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        MySQL based virtual hosts (vhosts) module for Lighttpd

%description mod_mysql_vhost
With MySQL based vhosting you can put the information where to look for
a. document-root of a given host into a MySQL database.

Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%package mod_trigger_b4_dl
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        Another anti hot-linking module for Lighttpd

%description mod_trigger_b4_dl
Anti Hotlinking:

* if user requests download-url directly the request is denied and
   he is redirected to ''deny-url'

* if user visits trigger-url before requesting download-url access
   is granted

* if user visits download-url again after trigger-timeout has run
   down to the request is denied and he is redirected  to deny-url

The storage for the trigger information is either stored locally in a
gdbm file or remotly in memcached.

Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%package mod_rrdtool
Requires:       %{name} = %{version}
Requires:       rrdtool
Group:          Productivity/Networking/Web/Servers
Summary:        Lighttpd module to feed rrdtool databases

%description mod_rrdtool
RRD_tool is a system to store and display time-series data (i.e.
network bandwidth, machine-room temperature, server load average).

This module feeds an rrdtool database with the traffic stats from
lighttpd.

Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%if 0%{?with_geoip}
%package mod_geoip
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        A Secure, Fast, Compliant, and Very Flexible Web Server

%description mod_geoip
Lighttpd a secure, fast, compliant, and very flexible Web server that
has been optimized for high-performance environments. It has a very low
memory footprint compared to other Web servers and takes care of CPU
load.  Its advanced feature set (FastCGI, CGI, Auth,
Output-Compression, URL-Rewriting, and more) makes lighttpd the perfect
Web server software for every server that is suffering load problems.

This is just a dummy package which is not build in autobuild. see the
buildservice project server:http if you want it.

Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%endif
%package mod_webdav
Requires:       %{name} = %{version}
Group:          Productivity/Networking/Web/Servers
Summary:        WebDAV module for Lighttpd

%description mod_webdav
The WebDAV module is a very minimalistic implementation of RFC 2518.
Minimalistic means that not all operations are implementated yet..

So far we have

* PROPFIND

* OPTIONS

* MKCOL

* DELETE

* PUT

and the usual GET, POST, HEAD from HTTP/1.1..

So far mounting a webdav resource into Windows XP works and the basic
litmus tests are passed.



Authors:
--------
    Jan Kneschke <jan@kneschke.de>

%prep

%setup -q -a 1
%patch0
%if 0%{?with_geoip}
%patch2
%endif
#%patch3

%build
%if 0%{?with_geoip}
autoreconf -fi
%endif
export CFLAGS="%{optflags} -DLDAP_DEPRECATED -W -Wmissing-prototypes -Wmissing-declarations -Wpointer-arith -Wchar-subscripts -Wformat=2 -Wbad-function-cast -std=gnu99"
%if %suse_version > 1000
export CFLAGS="$CFLAGS -fstack-protector"
%endif
%configure \
    --bindir=%{_sbindir}        \
    --libdir=%{_libdir}/%{pkg_name} \
    --enable-lfs                \
%if 0%{?with_ipv6}
    --enable-ipv6               \
%else
    --disable-ipv6               \
%endif
%if 0%{?with_ldap}
    --with-ldap                 \
%endif
    --with-mysql                \
%if 0%{?with_ssl}
    --with-openssl              \
%endif
    --with-gdbm                 \
    --with-lua                  \
    --with-memcache             \
    --with-bzip2                \
    --with-webdav               \
%if 0%{?with_enh_webdav}
    --with-webdav-props         \
    --with-webdav-locks         \
%endif
    --with-fam                  \
    --with-attr
%{__make}
%if 0%{?with_tests}
sh -x %{S:2}
%endif

%install
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
%makeinstall

%{__install} -d -m 0755 %{buildroot}%{pkg_home}/sockets
%{__install} -d -m 0755 %{buildroot}%{_var}/cache/%{pkg_name}/compress
%{__install} -d -m 0755 %{buildroot}%{_var}/log/www/%{pkg_name}
%{__install} -d -m 0755 %{buildroot}%{_var}/log/www/%{pkg_name}/server
%{__install} -d -m 0750 %{buildroot}%{_var}/log/www/%{pkg_name}/access
%{__install} -d -m 0750 %{buildroot}%{_var}/log/www/%{pkg_name}/error

(cd %{name}-init-%{version} && \
 %{__make} DESTDIR=%{buildroot} \
	prefix=%{_prefix} \
        sysconfdir=%{_sysconfdir} \
	libdir=%{_libdir}/%{pkg_name} \
        fillupdir=%{_var}/adm/fillup-templates \
        permissionsdir=%{_sysconfdir}/permissions.d \
        install)
%if 0%{?with_geoip} == 0
%{__rm} -f %{buildroot}%{_sysconfdir}/lighttpd/conf.d/geoip.conf
%endif
%{__ln_s} ../../%{initdir}/lighttpd %{buildroot}%{_sbindir}/rclighttpd

%{__install} -d -m 0750 %{buildroot}%{_sysconfdir}/%{pkg_name}/ssl

# susefirewall config file
%if 0%{?with_susefirewall_config}
%{__install} -D -m 0644 %{S:3} \
    %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/lighttpd
%{__install} -D -m 0644 %{S:4} \
    %{buildroot}/etc/sysconfig/SuSEfirewall2.d/services/lighttpd-ssl
%endif

# remove the .la files. we dont need them.
%{__rm} -vf %{buildroot}%{_libdir}/%{pkg_name}/*.la

%clean
test "%{buildroot}" != "/" && test -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%post
level=${1:-0}
%fillup_and_insserv %{pkg_name}

# in any case remove service first
if test -L /service/%{pkg_name} -a -x /service/%{pkg_name}/run ; then
  cd /service/%{pkg_name}
  %{__rm} /service/%{pkg_name}
  svc -dx . log
  %{__rm} -fr supervise || :
  %{__rm} -fr log/supervise || :
fi

# add service now
if test $level -eq 1 ; then
  touch %{_sysconfdir}/%{pkg_name}/down
  touch %{_sysconfdir}/%{pkg_name}/log/down
fi
%{__ln_s} %{_sysconfdir}/%{pkg_name} /service/%{pkg_name}

%preun
level=${1:-0}
test $level -eq 0 || exit 0
# stop and remove service
if test -L /service/%{pkg_name} ; then
  cd /service/%{pkg_name}
  %{__rm} /service/%{pkg_name}
  svc -dx . log
fi
%{__rm} -fr %{_sysconfdir}/%{pkg_name}/supervise || :
%{__rm} -fr %{_sysconfdir}/%{pkg_name}/log/supervise || :

%postun
%restart_on_update %{pkg_name}
%{insserv_cleanup}

%files
%define confattr %attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime)
%defattr(-,root,root)
%doc doc/lighttpd.conf doc/lighttpd.user README INSTALL NEWS COPYING AUTHORS
%doc doc/*.dot
%doc doc/spawn-php.sh
%doc doc/accesslog.txt
%doc doc/access.txt
%doc doc/alias.txt
%doc doc/authentication.txt
%doc doc/cgi.txt
%doc doc/compress.txt
%doc doc/configuration.txt
%doc doc/expire.txt
%doc doc/fastcgi-state.txt
%doc doc/fastcgi.txt
%doc doc/features.txt
%doc doc/performance.txt
%doc doc/plugins.txt
%doc doc/proxy.txt
%doc doc/redirect.txt
%doc doc/rewrite.txt
%doc doc/scgi.txt
%doc doc/secdownload.txt
%doc doc/security.txt
%doc doc/setenv.txt
%doc doc/simple-vhost.txt
%doc doc/skeleton.txt
%doc doc/ssi.txt
%doc doc/ssl.txt
%doc doc/state.txt
%doc doc/status.txt
%doc doc/traffic-shaping.txt
%doc doc/userdir.txt
%if 0%{?with_susefirewall_config}
%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/lighttpd*
%endif
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/init.d/%{pkg_name}
%attr(0644,root,root) %{_sysconfdir}/permissions.d/%{pkg_name}
%attr(1755,root,%{pkg_group}) %dir %{_sysconfdir}/%{pkg_name}
%attr(0750,root,%{pkg_group}) %dir %{_sysconfdir}/%{pkg_name}/conf.d
%attr(0750,root,%{pkg_group}) %dir %{_sysconfdir}/%{pkg_name}/vhosts.d
%attr(0750,root,%{pkg_group}) %dir %{_sysconfdir}/%{pkg_name}/env
%attr(0750,root,%{pkg_group}) %dir %{_sysconfdir}/%{pkg_name}/ssl
%attr(0755,root,root) %dir %{_prefix}/share/%{pkg_name}
%attr(0744,root,root) %dir %{_sysconfdir}/%{pkg_name}/log
%attr(0644,root,root) %ghost %{_sysconfdir}/%{pkg_name}/down
%attr(0644,root,root) %ghost %{_sysconfdir}/%{pkg_name}/log/down
%attr(0744,root,root) %config(noreplace) %{_sysconfdir}/%{pkg_name}/run
%attr(0744,root,root) %config(noreplace) %{_sysconfdir}/%{pkg_name}/log/run
%verify(not md5 size mtime) %ghost %config(missingok,noreplace) %{_sysconfdir}/%{pkg_name}/env/*
%confattr %{_sysconfdir}/%{pkg_name}/lighttpd.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/accesslog.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/auth.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/cgi.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/compress.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/debug.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/dirlisting.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/evhost.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/expire.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/fastcgi.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/mime.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/proxy.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/scgi.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/secdownload.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/simple_vhost.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/ssi.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/ssl.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/status.conf
%confattr %{_sysconfdir}/%{pkg_name}/conf.d/userdir.conf
%confattr %{_sysconfdir}/%{pkg_name}/vhosts.d/vhosts.template
%dir %{_libdir}/%{pkg_name}
%{_libdir}/%{pkg_name}/mod_access.so
%{_libdir}/%{pkg_name}/mod_accesslog.so
%{_libdir}/%{pkg_name}/mod_alias.so
%{_libdir}/%{pkg_name}/mod_auth.so
%{_libdir}/%{pkg_name}/mod_cgi.so
%{_libdir}/%{pkg_name}/mod_compress.so
%{_libdir}/%{pkg_name}/mod_dirlisting.so
%{_libdir}/%{pkg_name}/mod_evasive.so
%{_libdir}/%{pkg_name}/mod_evhost.so
%{_libdir}/%{pkg_name}/mod_expire.so
%{_libdir}/%{pkg_name}/mod_extforward.so
%{_libdir}/%{pkg_name}/mod_fastcgi.so
%{_libdir}/%{pkg_name}/mod_flv_streaming.so
%{_libdir}/%{pkg_name}/mod_indexfile.so
%{_libdir}/%{pkg_name}/mod_proxy.so
%{_libdir}/%{pkg_name}/mod_redirect.so
%{_libdir}/%{pkg_name}/mod_rewrite.so
%{_libdir}/%{pkg_name}/mod_scgi.so
%{_libdir}/%{pkg_name}/mod_secdownload.so
%{_libdir}/%{pkg_name}/mod_setenv.so
%{_libdir}/%{pkg_name}/mod_simple_vhost.so
%{_libdir}/%{pkg_name}/mod_ssi.so
%{_libdir}/%{pkg_name}/mod_staticfile.so
%{_libdir}/%{pkg_name}/mod_status.so
%{_libdir}/%{pkg_name}/mod_userdir.so
%{_libdir}/%{pkg_name}/mod_usertrack.so
%{_mandir}/*
%{_sbindir}/*
%attr(0755,root,root) %{_prefix}/share/%{pkg_name}/create-config
%attr(0755,root,root) %{_prefix}/share/%{pkg_name}/create-log-config
%attr(0644,root,root) %{_var}/adm/fillup-templates/sysconfig.%{pkg_name}
%attr(751,%{pkg_user},%{pkg_group}) %dir %{pkg_home}
%attr(751,%{pkg_user},%{pkg_group}) %dir %{pkg_home}/sockets
%attr(751,%{pkg_user},%{pkg_group}) %{_var}/cache/%{pkg_name}
%attr(0750,nobody,%{pkg_group}) %dir %{_var}/log/www/%{pkg_name}
%attr(0755,nobody,nobody) %dir %{_var}/log/www/%{pkg_name}/server
%attr(0750,%{pkg_user},%{pkg_group}) %dir %{_var}/log/www/%{pkg_name}/access
%attr(0750,%{pkg_user},%{pkg_group}) %dir %{_var}/log/www/%{pkg_name}/error

%files mod_rrdtool
%defattr(-,root,root,-)
%doc doc/rrdtool.txt
%doc doc/rrdtool-graph.sh
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/rrdtool.conf
%{_libdir}/%{pkg_name}/mod_rrdtool.so

%files mod_cml
%defattr(-,root,root,-)
%doc doc/cml.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/cml.conf
%{_libdir}/%{pkg_name}/mod_cml.so

%files mod_magnet
%defattr(-,root,root,-)
%doc doc/magnet.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/magnet.conf
%{_libdir}/%{pkg_name}/mod_magnet.so

%files mod_mysql_vhost
%defattr(-,root,root,-)
%doc doc/mysqlvhost.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/mysql_vhost.conf
%{_libdir}/%{pkg_name}/mod_mysql_vhost.so

%files mod_trigger_b4_dl
%defattr(-,root,root,-)
%doc doc/trigger_b4_dl.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/trigger_b4_dl.conf
%{_libdir}/%{pkg_name}/mod_trigger_b4_dl.so
%if 0%{?with_geoip}

%files mod_geoip
%defattr(-,root,root,-)
%doc doc/geoip.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/geoip.conf
%{_libdir}/%{pkg_name}/mod_geoip.so
%endif

%files mod_webdav
%defattr(-,root,root,-)
%doc doc/webdav.txt
%attr(640,root,%{pkg_group}) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{pkg_name}/conf.d/webdav.conf
%{_libdir}/%{pkg_name}/mod_webdav.so

%changelog
* Tue Nov 03 2009 - Bernhard Graf <graf@movingtarget.de> 1.4.24-0
- upgraded to 1.4.24

* Fri Apr 03 2009 - Bernhard Graf <graf@movingtarget.de> 1.4.22-0
- upgraded to 1.4.22

* Tue Dec 09 2008 - Bernhard Graf <graf@movingtarget.de> 1.4.20-0
- upgraded to 1.4.20

* Sat Mar 29 2008 - Bernhard Graf <graf@movingtarget.de> 1.4.19-1
- make a few configure settings configurable for RPM building

* Thu Mar 13 2008 - Bernhard Graf <graf@movingtarget.de> 1.4.19-0
- upgraded to 1.4.19

* Mon Feb 18 2008 - Bernhard Graf <graf@movingtarget.de> 1.4.18-3
- patch to fix a zombie bug in "include_shell" when lighttpd started with
  option -D
- bug fix: services were removed on update due to brain-dead order of
  %post, %postun, %pre and %preun .

* Fri Feb 15 2008 - Bernhard Graf <graf@movingtarget.de> 1.4.18-2
- lots of filesystem layout and configuration changes to make it compatible
  with openSUSE's version of lighttpd

* Tue Sep 11 2007 - Bernhard Graf <graf@movingtarget.de> 1.4.18-1
- upgraded to 1.4.18

* Tue Apr 19 2007 - Bernhard Graf <graf@movingtarget.de> 1.4.15
- upgraded to 1.4.15

* Mon Dec 18 2006 - Bernhard Graf <graf@movingtarget.de> 1.4.13
- SuSE package to run under daemontools

* Thu Sep 30 2004 12:41 <jan@kneschke.de> 1.3.1
- upgraded to 1.3.1

* Tue Jun 29 2004 17:26 <jan@kneschke.de> 1.2.3
- rpmlint'ed the package
- added URL
- added (noreplace) to start-script
- change group to Networking/Daemon (like apache)

* Sun Feb 23 2003 15:04 <jan@kneschke.de>
- initial version
