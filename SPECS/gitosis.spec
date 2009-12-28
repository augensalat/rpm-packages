#
# spec file for package gitosis (Version 0.2)
#
# Copyright  (c)  2009  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define gitexecdir %(git --exec-path)
 
Name:		gitosis
Version:	0.2
Release:	20080825git.0
Distribution:	%(head -n1 /etc/SuSE-release)
Summary:	Git repository hosting application
Group:		Development/Tools/Version Control
License:	GPL+
URL:		http://eagain.net/gitweb/?p=gitosis.git
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# $ git-clone --bare git://eagain.net/gitosis.git gitosis
# $ cd gitosis
# $ git-archive --format=tar --prefix=gitosis-0.2/ 73a032520493f6b4186185d4826d12edb5614135 | bzip2 > ../gitosis-0.2.tar.bz2
Source:		gitosis-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	python-devel python-setuptools git-core
%py_requires
Requires(pre):	shadow-utils
Requires:	git-core openssh

%description
Gitosis aims to make hosting git repos easier and safer. It manages
multiple repositories under one user account, using SSH keys to identify
users. End users do not need shell accounts on the server, they will talk
to one shared account that will not let them run arbitrary commands.

%prep
%setup -q -n gitosis-%{version}

%build
%{__python} setup.py build

%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

export CFLAGS="%{optflags}"
%{__python} setup.py install \
	--root="%{buildroot}" \
	--skip-build \
	--prefix="%{_prefix}" \
        --record-rpm=INSTALLED_FILES
%{__install} -d -m 0755 %{buildroot}/srv/gitosis/repositories
%{__install} -d -m 0755 "%{buildroot}%{gitexecdir}"
(
  cd "%{buildroot}%{gitexecdir}"
  for n in init run-hook serve; do
    %{__ln_s} %{_bindir}/gitosis-$n git-gitosis-$n
  done
)

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%pre
# Add "gitosis" user
/usr/sbin/groupadd -r gitosis &>/dev/null || :
/usr/sbin/useradd -r -g gitosis -d /srv/gitosis -m -s /bin/sh -c "gitosis repository hosting" gitosis &>/dev/null || :

%post
install_count=$1
if [ "$install_count" = 1 ]
then # first time installation
  %{__cat} <<ETX
What's next:

If you don't have an SSH key yet, create one now on your *LOCAL* computer:
$ ssh-keygen -t dsa
   (just hit <Enter> on all questions)

Issue the following command on your *LOCAL* computer to copy your public
SSH key to this host (aka your Gitosis server):
$ scp ~/.ssh/id_dsa.pub USER@SERVER:/tmp
   (USER is your user id on SERVER (aka *THIS* host, aka your Gitosis server)

On *THIS* host issue the following as root:
$ sudo -H -u gitosis git gitosis-init </tmp/id_dsa.pub

ETX
fi

%files
%defattr(-,root,root,-)
%doc COPYING example.conf README.rst TODO.rst gitweb.conf lighttpd-gitweb.conf
%{_bindir}/gitosis-init
%{_bindir}/gitosis-run-hook
%{_bindir}/gitosis-serve
%{gitexecdir}/*
%{py_sitedir}/*
%dir %attr(0755,gitosis,gitosis) /srv/gitosis/repositories

%changelog
* Thu Aug 20 2009 - Bernhard Graf <graf@movingtarget.de>
- Initial release
