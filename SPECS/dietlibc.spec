#
# spec file for package dietlibc (Version 0.32)
#
# Copyright  (c)  2001-2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# norootforbuild

Name:           dietlibc
License:        GPL v2 or later
Group:          Development/Languages/C and C++
Provides:       diet
AutoReqProv:    on
Version:        0.32
Release:        0
Source0:        http://www.fefe.de/dietlibc/%{name}-%{version}.tar.bz2
Patch1:         %{name}-%{version}-tcsetattr.diff
Patch6:         long-double-workaround.diff
Patch7:         %{name}-%{version}-features.diff
Patch32:        %{name}-%{version}-pause.diff
Url:            http://www.fefe.de/dietlibc/
Summary:        A Libc Optimized for Small Size
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Diet libc is optimized for small size. It can be used to create small
statically-linked binaries for Linux on many platforms.



Authors:
--------
    Felix von Leitner <felix-dietlibc@fefe.de>

%define prefix   /opt/dietlibc
%debug_package
%prep
%setup -q
%patch1
%patch6
%patch7
%patch32

%build
MY_RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e 's,-O2,-Os,' \
   -e 's/-D_FORTIFY_SOURCE[=0-9]*//' \
   -e 's/-ffortify[=0-9]*//' \
   -e 's/-fstack-protector//')
make %{?jobs:-j%jobs} prefix=%{prefix} CFLAGS="`echo $CFLAGS $MY_RPM_OPT_FLAGS` -fno-strict-aliasing"

%install
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}
%ifarch hppa
export RPM_ARCH=parisc
%endif
%ifarch %arm
export RPM_ARCH=arm
%endif

%{__mkdir_p} %{buildroot}{%{_bindir},%{prefix}/{bin-$RPM_ARCH,lib-$RPM_ARCH},%{_mandir}/man1}
cd bin-$RPM_ARCH
%{__mv} -f dietlibc.a libc.a
%{__mv} -f diet-i diet
%{__install} -m644 start.o lib*.a %{buildroot}%{prefix}/lib-$RPM_ARCH
%{__install} -m755 diet elftrunc %{buildroot}%{prefix}/bin-$RPM_ARCH
%{__install} -m644 ../diet.1 %{buildroot}%{_mandir}/man1
%{__cp} -a ../include %{buildroot}%{prefix}
%{__ln_s} -fv lib-$RPM_ARCH %{buildroot}%{prefix}/lib
%{__ln_s} -fv bin-$RPM_ARCH %{buildroot}%{prefix}/bin
%{__ln_s} -fv %{prefix}/bin-$RPM_ARCH/{diet,elftrunc} %{buildroot}%{_bindir}

%clean
test "%{buildroot}" != "/" -a -d %{buildroot} && %{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHOR BUGS CAVEAT CHANGES COPYING FAQ PORTING README SECURITY TODO THANKS
%doc %{_mandir}/man?/*
%{prefix}
%{_bindir}/*
%changelog
* Thu Oct 15 2009 Bernhard Graf <graf@movingtarget.de>
- update to 0.32
* Thu Feb 21 2007 - Bernhard Graf <graf@movingtarget.de>
- update to 0.31
* Thu Feb 01 2007 - dmueller@suse.de
- update to 0.30:
  * remove upstream'ed patches
- remove glibc-specific flags from RPM_OPT_FLAGS
* Sun Feb 19 2006 - dmueller@suse.de
- fix build on ppc
* Wed Jan 25 2006 - mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Nov 16 2005 - dmueller@suse.de
- fix kernel_size_t for x86_64
* Mon Nov 14 2005 - dmueller@suse.de
- use -fno-strict-aliasing
* Fri Nov 04 2005 - schwab@suse.de
- Implement pause on ia64.
* Fri Oct 21 2005 - dmueller@suse.de
- update to 0.29
* Mon Sep 12 2005 - snwint@suse.de
- olh: fix ppc syscalls (#116391)
* Tue Aug 09 2005 - schwab@suse.de
- Fix ppc64 support.
* Thu May 05 2005 - schwab@suse.de
- Fix ia64 assembler.
* Thu Mar 24 2005 - uli@suse.de
- fixed to build on ARM, GCC4
* Fri Oct 15 2004 - ro@suse.de
- define nonnull as glibc does
* Tue Mar 09 2004 - mjancar@suse.cz
- undef WANT_SYSTENTER in dietfeatures.h, breaks on uml
  kernels (#35444)
* Fri Feb 27 2004 - garloff@suse.de
- Implement pause() on AXP.
* Fri Feb 27 2004 - ro@suse.de
- fix build on i386 with regparm changes
* Wed Feb 11 2004 - ro@suse.de
- move ia64 specific ftruncate64 to ia64 dir
* Tue Feb 10 2004 - schwab@suse.de
- Copy setjmp and longjmp from glibc.
* Thu Jan 29 2004 - hare@suse.de
- Fixed setjmp() for s390 and s390x.
* Sat Jan 10 2004 - adrian@suse.de
- build as user
* Wed Dec 10 2003 - uli@suse.de
- map select to _newselect on s390*
* Fri Oct 17 2003 - schwab@suse.de
- Fix ia64 support.
- Fix use of common symbols.
* Tue Oct 07 2003 - mjancar@suse.cz
- handle '%%m' in printf
* Tue Oct 07 2003 - mjancar@suse.cz
- use $RPM_OPT_FLAGS
- cleanup the spec
- fix mmap and stat on s390 and s390x
- fix startup on ppc64
- fix fork __alarm and __time on ia64
* Thu Oct 02 2003 - mjancar@suse.cz
- update to 0.23
- kill obsolete patches
- fix startup on s390
- add missing elf definitions
- add preliminary support for s390x and ppc64
* Thu Sep 18 2003 - snwint@suse.de
- removed stray backup file (#30188)
* Sat Sep 06 2003 - schwab@suse.de
- Fix setting of environ in ia64 startup.
* Wed Aug 06 2003 - mjancar@suse.cz
- fix syscall on AMD64
* Fri Jun 27 2003 - mjancar@suse.cz
- fix realpath
- use qsort from uClibc instead of the insertsort
* Wed Feb 05 2003 - bg@suse.de
- activated support for hppa
* Mon Feb 03 2003 - meissner@suse.de
- Upgraded to 0.21, dropped atexit and s390 patch (already upstream)
- Fixed asm statement in ppc/mmap.c.
* Wed Sep 18 2002 - ro@suse.de
- removed bogus self-provides
* Mon Aug 26 2002 - garloff@suse.de
- Make exit() alias to libc_exit in atexit strong. (Better fix for
  atexit problem addressed by 2002-08-19 15:18 patch.)
* Tue Aug 20 2002 - schwab@suse.de
- Fix startup on ia64.
* Mon Aug 19 2002 - schwab@suse.de
- ia64 fixes:
  * Fix sys/types.h.
  * Implement more syscalls.
  * Fix syscall_weak macro.
* Mon Aug 19 2002 - garloff@suse.de
- Disable exit() weak alias in unified syscall in favour of exit()
  from atexit().
* Mon Aug 19 2002 - garloff@suse.de
- Split ppc diff into __powerpc__ -> powerpc stuff and the types
  corrections.
- Drop x86_64_ia64 diff, as x86_64 and ia64 support has been
  integrated into dietlibc.
- Update to dietlibc-0.20:
  * calloc and malloc fixes
  * add ucontext
  * x86_64: umount and stime support, unified syscall fix
  * realpath fix
- Update to dietlibc-0.19:
  * Resistence to hostile DNS packets
  * Avoid __thread (keyword in gcc CVS)
  * ia64: start and unified syscall fixes
  * killpg is function now
  * sparc/strlen.S added
  * ARM fixes: setjmp, syscall
  * overflows: xdr_array, calloc, fread, fwrite
  * x86_64 socket calls and mmap
- Update to dietlibc-0.18:
  * Add: stpcpy, memrchr
  * x86_64 port (Michal Ludvig)
  * iA64 port (Thomas Ogrisegg)
  * truncate64/ftruncate64/getdents64
  * ARM profiling (WIP)
  * mktime fix
  * ftell takes into account ungetc now
  * perror resistance to NULL ptr
  * sig functions don't segfault for sig 0 any longer
  * socket syscalls for PA-Risc, iA64
  * PA-Risc clone
  * rand48 init fixes
  * fnmatch infinite loop fix
  * getopt, putenv tweaks
  * DNS resolver IPv6 transport capable (WANT_IPV6_DNS)
  * cpio.h, tar.h added.
  * signal() is wrapper to sigaction now
* Fri Aug 16 2002 - ro@suse.de
- removed empty post/postun-scripts (#17826)
* Mon Jul 15 2002 - kukuk@suse.de
- Replace BuildArch with ExclusiveArch.
* Wed Jun 05 2002 - stepan@suse.de
- add support for x86-64
- add support for ia64 (not working)
* Fri May 10 2002 - garloff@suse.de
- Update to dietlibc-0.17:
  * patches (sigcontext, termios, AXP signal ...) have been merged
  * fixes (i386/getenv, long long scanf, ptrace, md5 glue,
  i386 memcpy, DNS domain search, i386 memchr,memcmp (count=0),
  getservent_r, i386 RAND_MAX ...)
  * new functions (memccpy, strncpy, regex, getdelim, getline, ...)
  * profiling support (i386 only)
- S/390 still segfaults :-(
* Fri May 10 2002 - garloff@suse.de
- Fix s390 clone().
* Tue Apr 09 2002 - ro@suse.de
- close the if in asm/sigcontext.h
* Mon Feb 25 2002 - garloff@suse.de
- Fix typo in alpha code.
* Mon Feb 25 2002 - garloff@suse.de
- Add support for signal() on alpha (osf_signal syscall does not
  work, instead use sigaction.)
* Mon Feb 25 2002 - garloff@suse.de
- types used in communiaction with kernel should be declared
  accordingly, i.e. arch dependently.
- __powerpc__ -> powerpc
* Mon Feb 25 2002 - garloff@suse.de
- struct termios differs between architectures in aux bits.
  ioctls failed because of different sizeof(termios).
* Thu Feb 21 2002 - garloff@suse.de
- Update to dietlibc-0.15:
  * Patches (alpha, fdatasync, sprintf) got integrated
  * Fixes (vfork->fork, bsearch, MIPS+HP-PA fixes, gethostbyname,
  inet_aton, fdopen, strftime, fmod, strstr, strncpy, i386
  asm getenv, grantpt, ptsname, unlockpt, getservent_r, ...)
* Thu Feb 21 2002 - garloff@suse.de
- Fix sprintf.
* Wed Feb 20 2002 - garloff@suse.de
- Support archs without __NR_fdatasync (i.e. alpha)
- Symbol address of glibc_deitlibc link guard is a .quad for alpha
* Wed Feb 20 2002 - garloff@suse.de
- Use BuildRoot.
* Wed Feb 20 2002 - garloff@suse.de
- Update to dietlibc-0.14:
  * ports to S/390 and parisc
  * various bugfixes (brk, vfork, fflush, ttyname, getpass, ...)
- Add patch for alpha
- Add fdatasync syscall
* Mon Feb 04 2002 - uli@suse.de
- yeah, maybe, but it's still armv4l, not arm4vl...
* Wed Jan 02 2002 - adrian@suse.de
- allow compile on mips and arm. It is even working ;)
* Tue Dec 18 2001 - snwint@suse.de
- fixed scanf(): %%n was broken, long long didn't work
* Mon Dec 03 2001 - mludvig@suse.cz
- Updated to version 0.12
* Mon Sep 03 2001 - kukuk@suse.de
- Remove broken #if case, compiler will optimize normal code
* Tue Aug 28 2001 - mludvig@suse.cz
- Initial release based on dietlibc-0.11
- Added support for %%n in *scanf
- Added pivot_root(2) syscall
- Synced to dietlibc's CVS
