#
# spec file for package perl-5010001 (Version 5.10.1)
#
# Copyright  (c)  2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# must be set to a true value (1) for a perl developer version
%define perl_devel 0

# by default build a threadless Perl
%define with_threads 0
# commandline overrides: rpm -ba|--rebuild --with 'xxx'
%{?_with_threads: %{expand: %%define with_threads 1}}

%define package_name	perl
%define version		5.10.1
%define identity	5010001
%define release		2

%define prefix /opt/%{package_name}/%{version}

Name:		%{package_name}-%{identity}
Version:        %{version}
Release:        %{release}
Summary:        The Perl interpreter
License:        Artistic License .. ; GPL v2 or later
Group:          Development/Languages/Perl
AutoReq:    	1
AutoProv:	0
Url:            http://www.perl.org/
Source:         %{package_name}-%{version}.tar.bz2
Patch:		perl-%{version}-gracefull-net-ftp.diff
Patch1:		perl-%{version}-fix_dbmclose_call.diff
Patch2:		perl-%{version}-regexp-refoverflow.diff
Patch3:		perl-%{version}-nroff.diff
Patch4:		perl-%{version}-netcmdutf8.diff
Patch5:		perl-%{version}-utf8cache.diff
Patch6:		perl-%{version}-utf8regex.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  db-devel gdbm-devel ncurses-devel zlib-devel
PreReq:         %{name}-base = %{version}
Recommends:     %{name}-doc = %{version}

%description
perl - Practical Extraction and Report Language

Perl is optimized for scanning arbitrary text files, extracting
information from those text files, and printing reports based on that
information.  It is also good for many system management tasks. Perl is
intended to be practical (easy to use, efficient, and complete) rather
than beautiful (tiny, elegant, and minimal).

Some of the modules available on CPAN can be found in the "perl"
series.

This Perl distribution is meant to be installed in PARALLEL to the
standard Perl installation, that comes bundled with openSUSE.
The are two reasons for parallel installs:
- Always have a recent or any appropriate Perl available.
- Update modules from CPAN without interfering with RPM-installed Perl
  modules.

To use this perl as default, add the following line to your ~/.bashrc:

  export PATH="/opt/perl/%{version}/bin:$PATH"

Authors:
--------
    Larry Wall, Louis J. LaBash, Jr. <llabash@siue.edu>

%package base
License:        Artistic License .. ; GPL v2 or later
Group:          Development/Languages/Perl
Summary:        The Perl interpreter
AutoReq:    	1
AutoProv:	0
Requires:       %{name} = %{version}

%description base
perl - Practical Extraction and Report Language

Perl is optimized for scanning arbitrary text files, extracting
information from those text files, and printing reports based on that
information.  It is also good for many system management tasks.

Perl is intended to be practical (easy to use, efficient, and complete)
rather than beautiful (tiny, elegant, and minimal).

This package contains only some basic modules and the perl binary
itself.



Authors:
--------
    Larry Wall, Louis J. LaBash, Jr. <llabash@siue.edu>

%package doc
License:        Artistic License .. ; GPL v2 or later
Group:          Development/Languages/Perl
Summary:        Perl Documentation
AutoReq:    	1
AutoProv:	0
Requires:       %{name} = %{version}

%description doc
Perl man pages and pod files.

Authors:
--------
    Larry Wall, Louis J. LaBash, Jr. <llabash@siue.edu>

%debug_package

%prep
%setup -q -n %{package_name}-%{version}
%patch0
%patch1
%patch2
%patch3
%patch4
%patch5 -p1
%patch6 -p1

%build
export SUSE_ASNEEDED=0
export BZIP2_LIB=%{_libdir}
export BZIP2_INCLUDE=%{_includedir}
export BUILD_BZIP2=0
options="-Doptimize='$RPM_OPT_FLAGS -Wall -pipe'"
%ifarch alpha
# -mieee needed for bad alpha gcc optimization
options="-Doptimize='$RPM_OPT_FLAGS -Wall -pipe -mieee'"
%endif
%ifarch ppc ppc64
options="$options -Duse64bitint"
%endif
# always use glibc's setenv
options="$options -Accflags='-DPERL_USE_SAFE_PUTENV'"
chmod 755 ./configure.gnu
./configure.gnu \
	--prefix="%{prefix}" \
%if 0%{?perl_devel}
	-Dusedevel \
	-Uversiononly \
%endif
	-Dvendorprefix="%{prefix}" \
	-Dprivlib="%{prefix}/lib" \
	-Dsitelib="%{prefix}/lib/site_perl" \
	-Dvendorlib="%{prefix}/lib/vendor_perl" \
%if 0%{?with_threads}
	-Dusethreads \
%endif
	-Di_db \
	-Di_dbm \
	-Di_ndbm \
	-Di_gdbm \
	-Duseshrplib=\'true\' \
	-Dman3ext=3pm \
	$options

%{__make}
mv libperl.so savelibperl.so
mv lib/Config.pm saveConfig.pm
mv lib/Config_heavy.pl saveConfig_heavy.pl
%{__make} clobber
./configure.gnu \
	--prefix="%{prefix}" \
%if 0%{?perl_devel}
	-Dusedevel \
	-Uversiononly \
%endif
	-Dvendorprefix="%{prefix}" \
	-Dprivlib="%{prefix}/lib" \
	-Dsitelib="%{prefix}/lib/site_perl" \
	-Dvendorlib="%{prefix}/lib/vendor_perl" \
%if 0%{?with_threads}
	-Dusethreads \
%endif
	-Di_db \
	-Di_dbm \
	-Di_ndbm \
	-Di_gdbm \
	-Dman3ext=3pm \
	$options
%{__make}
%ifnarch %arm

%check
export SUSE_ASNEEDED=0
%{__make} test
%endif

%install
prefix="%{prefix}"
libdir="%{prefix}/lib"
%{__make} install DESTDIR=$RPM_BUILD_ROOT
cpa=`echo $RPM_BUILD_ROOT%{prefix}/lib/*/CORE | sed -e 's@/CORE$@@'`
cp=`echo "$cpa" | sed -e 's@/[^/]*$@@'`
install -m 555 savelibperl.so $cpa/CORE/libperl.so
install -m 444 saveConfig.pm $cpa/Config.pm
install -m 444 saveConfig_heavy.pl $cpa/Config_heavy.pl
pushd /usr/include
( rpm -ql glibc-devel | fgrep '.h' 
  find /usr/include/asm/ -name \*.h
  find /usr/include/asm-generic -name \*.h
) | while read f; do
  $RPM_BUILD_ROOT%{prefix}/bin/perl -I$cp -I$cpa $RPM_BUILD_ROOT%{prefix}/bin/h2ph -d $cpa ${f/\/usr\/include\//} || : 
done
popd
d="`gcc -print-file-name=include`"
test -f "$d/stdarg.h" && (cd $d ; $RPM_BUILD_ROOT/usr/bin/perl -I$cp -I$cpa $RPM_BUILD_ROOT/usr/bin/h2ph -d $cpa stdarg.h stddef.h float.h)
$RPM_BUILD_ROOT%{prefix}/bin/perl -e '$r=chr(128)."\\x{100}";/$r/'
# test perl-regexp-refoverflow.diff
$RPM_BUILD_ROOT%{prefix}/bin/perl -e '/\6666666666/'
%if 1
# remove unrelated target/os manpages
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlaix.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlamiga.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlapollo.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlbeos.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlbs2000.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlcygwin.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perldgux.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perldos.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlepoc.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlfreebsd.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlhpux.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlhurd.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlirix.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlmachten.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlmacos.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlmacosx.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlmint.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlnetware.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlopenbsd.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlos2.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlos390.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlos400.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlplan9.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlqnx.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlsolaris.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perltru64.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perluts.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlvmesa.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlvms.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlvos.1*
rm $RPM_BUILD_ROOT%{prefix}/man/man1/perlwin32.1*
%endif
cat << EOF > perl-base-filelist
$libdir/Carp.pm
$libdir/Carp/
$libdir/Class/
$libdir/Config/
$libdir/Digest.pm
$libdir/Digest/
$libdir/Exporter.pm
$libdir/Exporter/
$libdir/File/
$libdir/Getopt/
$libdir/IPC/
$libdir/Text/
$libdir/Tie/Hash.pm
$libdir/warnings.pm
$libdir/warnings/
$libdir/AutoLoader.pm
$libdir/FileHandle.pm
$libdir/SelectSaver.pm
$libdir/Symbol.pm
$libdir/attributes.pm
$libdir/base.pm
$libdir/bytes.pm
$libdir/bytes_heavy.pl
$libdir/constant.pm
$libdir/fields.pm
$libdir/feature.pm
$libdir/integer.pm
$libdir/locale.pm
$libdir/overload.pm
$libdir/strict.pm
$libdir/utf8.pm
$libdir/utf8_heavy.pl
$libdir/vars.pm
$libdir/version.pm
$libdir/*-linux*/Data/
$libdir/*-linux*/Digest/
$libdir/*-linux*/File/
$libdir/*-linux*/List/
$libdir/*-linux*/Scalar/
$libdir/*-linux*/IO.pm
$libdir/*-linux*/IO/Dir.pm
$libdir/*-linux*/IO/File.pm
$libdir/*-linux*/IO/Handle.pm
$libdir/*-linux*/IO/Pipe.pm
$libdir/*-linux*/IO/Poll.pm
$libdir/*-linux*/IO/Seekable.pm
$libdir/*-linux*/IO/Select.pm
$libdir/*-linux*/IO/Socket.pm
$libdir/*-linux*/IO/Socket/
$libdir/*-linux*/B.pm
$libdir/*-linux*/B/Deparse.pm
$libdir/*-linux*/Config.pm
$libdir/*-linux*/Config_heavy.pl
$libdir/*-linux*/Cwd.pm
$libdir/*-linux*/DynaLoader.pm
$libdir/*-linux*/Errno.pm
$libdir/*-linux*/Fcntl.pm
$libdir/*-linux*/POSIX.pm
$libdir/*-linux*/Socket.pm
$libdir/*-linux*/XSLoader.pm
$libdir/*-linux*/auto/Data/
$libdir/*-linux*/auto/Digest/
$libdir/*-linux*/auto/Fcntl/
$libdir/*-linux*/auto/File/
$libdir/*-linux*/auto/IO/
$libdir/*-linux*/auto/List/
$libdir/*-linux*/auto/Cwd/
$libdir/*-linux*/auto/DynaLoader/
$libdir/*-linux*/auto/Socket/
$libdir/*-linux*/auto/POSIX/POSIX.bs
$libdir/*-linux*/auto/POSIX/POSIX.so
$libdir/*-linux*/auto/POSIX/autosplit.ix
$libdir/*-linux*/auto/POSIX/load_imports.al
$libdir/*-linux*/lib.pm
$libdir/*-linux*/re.pm
EOF
p="${prefix:1}"
sed -e 's/^/%%exclude /' perl-base-filelist
(
  cd $RPM_BUILD_ROOT
  for i in "$p"/lib/pod/*; do
    case $i in */perldiag.pod) ;;
    *) echo "%%exclude /$i" ;;
    esac
  done
) > perl-base-excludes

%files base -f perl-base-filelist
%defattr(-,root,root)
%dir %{prefix}/lib
%dir %{prefix}/lib/*-linux*
%dir %{prefix}/lib/*-linux*/auto
%dir %{prefix}/lib/*-linux*/B
%dir %{prefix}/lib/*-linux*/auto/POSIX
%{prefix}/bin/perl

%files -f perl-base-excludes 
%defattr(-,root,root)
%exclude %{prefix}/bin/perl
%exclude %{prefix}/lib/Unicode/*/*.txt
%exclude %{prefix}/lib/unicore/*.txt
%{prefix}/bin/*
%{prefix}/lib/*

%files doc
%defattr(-,root,root)
%exclude %{prefix}/lib/pod/perldiag.pod
%doc %{prefix}/man/man1/*
%doc %{prefix}/man/man3/*
%doc %{prefix}/lib/pod
%doc %{prefix}/lib/Unicode/*/*.txt
%doc %{prefix}/lib/unicore/*.txt

%changelog
* Wed Dec 09 2009 graf@movingtarget.de - 5010001-2
- patch to fix occasional runtime errors with utf8 strings and regular
  expressions, perl #60508
  http://rt.perl.org/rt3/Public/Bug/Display.html?id=60508
* Sat Nov 21 2009 graf@movingtarget.de - 5010001-1
- improved filesystem layout to enable parallel version install
- don't build shared libperl
* Tue Oct 13 2009 graf@movingtarget.de - 5010001-0
- install as parallel Perl under /opt
* Thu Sep  3 2009 mls@suse.de
- update to perl-5.10.1 to get rid of some patches
  (the update mostly consists of changes in the
  experimental features)
* Tue Jul  7 2009 coolo@novell.com
- disable as-needed as it breaks at least make test
* Tue Jul  7 2009 coolo@novell.com
- fix macros file
* Mon Jun 29 2009 chris@computersalat.de
- spec mods
  o added lost Provides/Obsoletes perl-macros
  o cleanup tags
* Fri Jun 26 2009 chris@computersalat.de
- fix for perl_gen_filelist
  o add test for
  - f "${RPM_BUILD_ROOT}/var/adm/perl-modules/{name}"
* Fri Jun 26 2009 mls@suse.de
- add macros.perl, README.macros files contributed by
  Christian <chris@computersalat.de>
- move perl specific macros from rpm macro file to macros.perl
* Wed Jun 10 2009 mls@suse.de
- fixed off-by-one in zlib inflate code [bnc#511241]
- fixed errorcount initialization [bnc#498425]
- fixed utf8 handling in Net::Cmd [bnc#493978]
- fixed performace degradation in syslog [bnc#489114]
* Wed Jan 14 2009 mls@suse.de
- work around nroff change [bnc#463444]
- fix another rmtree vulnerability [bnc#450385]
* Wed Jan  7 2009 olh@suse.de
- obsolete old -XXbit packages (bnc#437293)
* Wed Nov 26 2008 mls@suse.de
- add perl-base to baselibs.conf [bnc#448884]
- include everything arch dependand in baselibs packages
* Wed Nov 19 2008 mls@suse.de
- fix ph file generation [bnc#413218]
* Fri Aug 29 2008 rguenther@suse.de
- Add Tie/Hash.pm to perl-base.  [bnc#421191]
* Mon Jul 14 2008 schwab@suse.de
- Fix another regexp backref overflow crash.
- Reenable testsuite on ppc64.
* Mon Jul 14 2008 mls@suse.de
- fix regexp backref overflow crash fix
* Fri Jul 11 2008 mls@suse.de
- fix bug File:Path that made synlink targets world-writable [bnc#402660]
- fix regexp backref overflow crash [bnc#372331]
* Tue May  6 2008 aj@suse.de
- Fix missing return value in configure script to silence rpmlint
  checks.
* Fri Apr 11 2008 mls@suse.de
- compile with -DPERL_USE_SAFE_PUTENV [bnc#377543]
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Mon Mar 17 2008 coolo@suse.de
- fix path for generated perl bindings (bnc#371713)
* Sat Mar 15 2008 coolo@suse.de
- pod/perldiag.pod is needed in the base distribution
* Tue Mar 11 2008 coolo@suse.de
- after several discussions on how to decrease size of perl
  distribution: split out perl-doc
- preparing blacklists for temporarly autorequires
* Mon Mar 10 2008 pth@suse.de
- Fix call to dbmclose in ext/ODBM_File/ODBM_File.xs
- Run 'make check' in %%check
* Tue Feb 19 2008 mls@suse.de
- fix bug in regexp engine [bnc#355233]
* Fri Jan 18 2008 mls@suse.de
- obsolete more packages
- fix bug in enc2xs [#354424]
* Tue Jan 15 2008 schwab@suse.de
- Remove broken test.
* Mon Jan  7 2008 mls@suse.de
- update to perl-5.10.0
  * happy 20th birthday, perl!
  * many new features, e.g. say, switch, state, dor, smart match
  * regular expressions now even more convoluted
  * some modules are now in core, e.g. zlib, digest::sha
  * modules updated to current version
  * see perldelta to know all of the glorious details
* Tue Nov  6 2007 mls@suse.de
- fix buffer overflow in regex engine CVE-2007-5116 (#332199)
* Wed Oct 31 2007 dmueller@suse.de
- update rpmlintrc
* Fri May 25 2007 ro@suse.de
- added rpmlintrc: ignore some devel files in perl package
* Mon May 21 2007 rguenther@suse.de
- Include Config_heavy.pl in perl-base.
* Fri May 11 2007 rguenther@suse.de
- Add all required directories to perl-base.
* Mon Apr 23 2007 rguenther@suse.de
- Split off a perl-base package containing /usr/bin/perl and
  some basic modules.
- Depend on perl-base from perl.
* Mon Mar 26 2007 rguenther@suse.de
- Add gdbm-devel, ncurses-devel and zlib-devel BuildRequires.
* Wed Dec 27 2006 schwab@suse.de
- Fix makedepend.
* Wed Dec 20 2006 jw@suse.de
- graceful-net-ftp patch added.
  Lousy FTP server responses could trigger silly error messages in Net::FTP
  and had no usable status_line in LWP.
  Now it is 500 + whatever message the server responded.
* Fri Feb 17 2006 mls@suse.de
- suppress prototype warning in autouse [#151459]
* Wed Feb  1 2006 mls@suse.de
- update to perl-5.8.8
- enable use64bitint on ppc/ppc64
* Sun Jan 29 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Sat Jan 28 2006 mls@suse.de
- update to perl-5.8.8-RC1
* Fri Dec  9 2005 mls@suse.de
- fix sprintf format string issues CVE-2005-3962 (#136360)
- added workaround for hanging debugger (#135559)
- moved SuSEconfig script to /usr/lib/perl5 (#130762)
* Tue Sep  6 2005 mls@suse.de
- fix infinite warn recursion by backporting change from bleadperl
  [#115402]
* Thu Aug 18 2005 mls@suse.de
- remove postun, handle it with ghosts
* Thu Jul 28 2005 mls@suse.de
- deal with new Config_heavy.pl
* Mon Jul 25 2005 mls@suse.de
- add rmtree patch (CAN-2005-0448)
* Fri Jul 22 2005 lmuelle@suse.de
- update to perl-5.8.7
* Wed Apr  6 2005 meissner@suse.de
- moved # icecream 0 tag where it does not get removed by checkin.
* Wed Apr  6 2005 meissner@suse.de
- Disable icecream to avoid problem with gcc4 / libperl.so preload.
* Thu Mar 24 2005 uli@suse.de
- fixed to build on ARM
* Fri Feb 18 2005 mls@suse.de
- fix perlbug mail sending
* Thu Feb 17 2005 mls@suse.de
- fix broken :encoding(utf8)
* Fri Feb  4 2005 mls@suse.de
- fix CAN-2005-0155/CAN-2005-0156 (PERLIO_DEBUG)
- fix CAN-2004-0452 (File::Path::rmtree)
* Mon Nov 29 2004 mls@suse.de
- update to perl-5.8.6
* Thu Aug 26 2004 schwab@suse.de
- Remove gratuitous use of kernel header.
- Fix mkdir race.
* Wed Jul 28 2004 mls@suse.de
- update to perl-5.8.5
* Tue Mar 16 2004 mls@suse.de
- fix instmodsh tmp file usage
* Fri Feb 27 2004 mls@suse.de
- update to perl-5.8.3
* Mon Dec  8 2003 mls@suse.de
- fix setenv issue by making perl behave differently if used
  embedded in an application (turns on PERL_USE_SAFE_PUTENV).
  [#32548]
* Sun Nov  2 2003 adrian@suse.de
- add missing Requires for gzip (used in SuSEconfig.perl)
- make it possible to build as non-root
* Mon Oct  6 2003 mls@suse.de
- update to perl-5.8.1
- fix srand initialization problem [perl change #21397]
* Mon Sep 22 2003 mls@suse.de
- update to perl-5.8.1-RC5
* Fri Aug 22 2003 mls@suse.de
- update to perl-5.8.1-RC4
- added sysconfig metadata
- use /usr/lib/perl* in the filelist so /usr/lib/debug doesn't get
  picked up
* Thu Aug 21 2003 mjancar@suse.cz
- use $RPM_OPT_FLAGS
* Fri Aug  1 2003 mls@suse.de
- fixed perlcc
* Thu Jul 31 2003 mls@suse.de
- update to perl-5.8.1-RC3
* Mon Jul 14 2003 mls@suse.de
- MM_Unix: fix vendor/siteman default path
* Fri Jul 11 2003 mls@suse.de
- create auto dirs in vendor_perl
* Fri Jul 11 2003 mls@suse.de
- update to perl-5.8.1-RC2
- use buildroot
* Wed Jun 11 2003 kukuk@suse.de
- Add auto subdirectory for perl modules
* Fri May  9 2003 ro@suse.de
- fix build with db-4.1
* Thu Feb  6 2003 mls@suse.de
- add sysconfig metadata to sysconfig.suseconfig-perl
- fix memory leak in socket creation
- restart stdio read/write when receiving EINTR
* Thu Jan  9 2003 mls@suse.de
- link with -lgdbm_compat when building ODBM_File
* Tue Sep 17 2002 ro@suse.de
- get all ph-files for bi-arch platforms
* Tue Sep 17 2002 mls@suse.de
- work around a bug in .ph file generation (#19664)
* Mon Sep  9 2002 mls@suse.de
- fix permissions of libperl.so
- added missing enc2xs binary
- create more .ph header files
- fixed h2ph enum handling
- (fixes bug #19175)
* Fri Aug 23 2002 mls@suse.de
- Fix bug in conversion of literals to floating point
- Add workaround for glibc crypt_r() bug
* Fri Aug  9 2002 mls@suse.de
- fix libs to include pthreads if threads are selected and
  /lib64/libc.so.6 exists
* Thu Aug  8 2002 mls@suse.de
- enabled thread support
* Wed Aug  7 2002 mls@suse.de
- corrected file list, added obsolete entries also to provides
* Wed Jul 31 2002 mls@suse.de
- Added Obsoletes line to obsolete all modules now packed
  with the core perl
* Fri Jul 26 2002 kukuk@suse.de
- Add a Provide "perl-base" [Bug #17259]
* Tue Jul 23 2002 mls@suse.de
- Allow missing tests in 'make test'
- delete broken lib/File/Find/t/find.t test
* Tue Jul 23 2002 mls@suse.de
- MM_Unix.pm: use INSTALLARCHLIB instead of INSTALLSITEARCH to
  store the site perllocal.pod file, like the printed message says
- added missing man3 pages
* Mon Jul 22 2002 mls@suse.de
- MM_Unix.pm: allow to overwrite PREFIX in the makefile, use
  better default for installsiteman{1,3}dir
* Fri Jul 19 2002 mls@suse.de
- update to perl-5.8.0
* Fri Jul  5 2002 kukuk@suse.de
- Use %%ix86 macro
* Tue Jun 18 2002 uli@suse.de
- disable check on armv4l
* Mon Jun 10 2002 mls@suse.de
- Pod::Man: don't put the generation date in the man pages
* Thu Jun  6 2002 olh@suse.de
- disable make check on ppc64, enable lfs test on ppc
* Thu Mar 14 2002 mls@suse.de
- Allow XSUBs as AUTOLOAD functions, worked in 5.6.0, needed
  for perl-Qt
* Fri Feb 22 2002 mls@suse.de
- Fixed File::Find if no_chdir is set (Ticket 20020213990000277)
* Wed Feb 20 2002 mls@suse.de
- Build DynaLoader.a with -fPIC to make mod_perl work on s390x
* Wed Feb  6 2002 coolo@suse.de
- patch Configure to also use -fPIC on Linux - prevents crashes on
  s390x
- ported over the hints patch from 7.2-lib64
* Tue Feb  5 2002 mls@suse.de
- Use Config.pm of libperl.so build, so that apps use the right
  link options.
* Mon Feb  4 2002 mls@suse.de
- Added generation of libperl.so
* Thu Jan 24 2002 schwab@suse.de
- Fix h2ph for gcc 3.
* Mon Jan 14 2002 mls@suse.de
- Moved rc.config variable to sysconfig/suseconfig
* Mon Jan  7 2002 schwab@suse.de
- Fix dependency generation for gcc 3.1 again.
* Thu Dec  6 2001 schwab@suse.de
- Don't add /usr/local/lib and /usr/local/include to the search paths.
- Fix dependency generation for gcc 3.1.
* Tue Nov 20 2001 schwab@suse.de
- Don't generate h2ph, h2xs, pod2man manpages by hand.
* Thu Sep 27 2001 mls@suse.de
- Fixed generation of perllocal.pod, also create perllocal.3pm
* Wed Sep 12 2001 mls@suse.de
- Fixed h2ph macro expansion/redefinition bugs.
- Moved *.ph creation from SuSEconfig to spec file.
* Fri Aug 31 2001 schwab@suse.de
- Remove ia64 workarounds.
* Wed Jun 20 2001 mls@suse.de
- bzip2 source
* Wed Jun 20 2001 mls@suse.de
- Update to perl-5.6.1
- Merged linux-alpha.sh and linux-sparc.sh into linux.sh
- axp compiler workaround: add -mieee
- use /lib64:/usr/lib64 on sparc64
* Mon Jun 11 2001 schwab@suse.de
- Remove ElectricFence from neededforbuild (got added by accident).
* Fri Apr 13 2001 schwab@suse.de
- Build with -O0 on ia64.
* Mon Mar 26 2001 schwab@suse.de
- Fix equality operator for systems that don't have NV_PRESERVES_UV.
- Reenable some tests on ia64.
* Thu Feb 22 2001 schwab@suse.de
- Fix POSIX module.
* Tue Dec  5 2000 schwab@suse.de
- Disable some problematic tests on ia64.
- Merge ia64 configuration with generic linux.
* Thu Oct 26 2000 ro@suse.de
- use new db for DB_File
- perl binary is no longer linked to any db lib
* Tue Oct 10 2000 ro@suse.de
- Config.pm: set $perl to 'perl'
- bzipped sources
- added some mandir patches
* Mon Sep 25 2000 ro@suse.de
- no test for lfs on ppc
* Wed Aug 16 2000 ro@suse.de
- update to 5.6.0
* Tue Aug 15 2000 ro@suse.de
- Security fix (/bin/mail+suidperl) added (from draht@suse.de)
* Fri Jul 14 2000 kukuk@suse.de
- Add license information and group tag (Bug #3454)
* Tue Jul 11 2000 ro@suse.de
- make perllocal.SuSE script more flexible
* Sat Apr  1 2000 bk@suse.de
- some tests don't pass on s390 too, known.
* Fri Mar  3 2000 schwab@suse.de
- Add support for ia64.
* Wed Jan 19 2000 ro@suse.de
- man -> /usr/share/man ; affects all perl packages
* Tue Dec 14 1999 kukuk@suse.de
- Fixed for SPARC
* Tue Nov  2 1999 ro@suse.de
- do h2ph for stdarg and stddef (BUG#785)
* Tue Oct 19 1999 ro@suse.de
- don't print error if /usr/src/linux is not owned by a package
  (BUG#215)
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Fri Aug 27 1999 ro@suse.de
- added "gnu","net" and "rpc" to directories for h2ph
* Fri Jul  9 1999 ro@suse.de
- added "bits" to directories for h2ph (closing BUG 58)
* Thu Jul  8 1999 ro@suse.de
- fix for perldoc
- update to 5.005_03
* Mon Mar  1 1999 ro@suse.de
- t/lib/anydbm: removed test 12 : create empty record: invalid for db2
* Thu Jan  7 1999 ro@suse.de
- alpha changes ; dont "make test" on alpha for now :-(
* Mon Nov 16 1998 ro@suse.de
- update to 5.00502
- fixed manpages for h2ph, h2xs, pod2man
- use configure.gnu
- keep SuSEconfig.perl from using more time than needed
* Fri Aug 28 1998 ro@suse.de
- updated to version perl5.004_05-MAINT_TRIAL_5
- updated filelist
- temporarily disablet test op/group.t for nobody/nogroup problem
* Wed Aug 19 1998 ro@suse.de
- added security-patches for pstruct and perldoc
* Fri Jul 24 1998 bs@suse.de
- enabled bincompat3
* Thu Jul  9 1998 ro@suse.de
- added some security and glib-patches (doio.c, perl.c)
- re-added support for gdbm
* Mon Jul  6 1998 ro@suse.de
- added rc.config.perl with variables:
    CREATE_PERLLOCAL_POD="yes"
    GENERATE_PERL_SYSTEM_INCLUDES="yes"
* Mon Jul  6 1998 ro@suse.de
- added SuSEconfig.perl and perllocal.SuSE
  + check if kernel-sources have changed and call h2ph
  + check installed modules and add/delete entries in perllocal.pod
* Thu Jan 22 1998 florian@suse.de
- use a fixed path as architecture name
* Tue Nov 11 1997 florian@suse.de
- fixed file list
- update to perl 5.004_04
* Tue Oct 14 1997 ro@suse.de
- ready for autobuild
  updated file list
* Thu Oct  9 1997 florian@suse.de
- prepare for autobuild
* Tue May 20 1997 florian@suse.de
- update to version 5.004
- disable hooks to csh in perl, it is not installed on all systems
* Thu Jan  2 1997 bs@suse.de
  h2ph call in doinst.sh added.
* Thu Jan  2 1997 florian@suse.de
  update to version 5.003
  security fix for suidperl
