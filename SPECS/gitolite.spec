#
# spec file for package gitolite (Version 1.5.8)
#
# Copyright  (c)  2011  Bernhard Graf <graf@movingtarget.de>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%global gitolite_home  /home/git
%global gitolite_user  git
%global gitolite_group git

Name:           gitolite
Version:        1.5.8
Release:        0
Distribution:	%(head -n1 /etc/SuSE-release)
Summary:        Highly flexible server for git directory version tracker
Group:		Development/Tools/Version Control
License:        GPL v2
URL:            http://github.com/sitaramc/gitolite
Source:         %{name}-%{version}.tar.bz2
Patch:          %{name}-%{version}.rpm.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       git >= 1.6.2 perl openssh pwdutils 
Provides:       perl(%{name}) = %{version}-%{release}
# Conflicts:      gitosis

%if 0%{?suse_version} > 1110
BuildArch: noarch
%endif

%description
Gitolite is an access control layer on top of git, which allows access control
down to the branch level, including specifying who can and cannot rewind a given
branch.

%prep
%setup -q
%patch

%build
%{__rm} -f src/gl-easy-install

%install
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"
# Directory structure
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}%{perl_vendorlib}
%{__install} -m 0755 -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 0750 -d %{buildroot}%{gitolite_home}/.ssh

%{__install} -m 0755 src/gl-* %{buildroot}%{_bindir}
%{__install} -m 0755 src/sshkeys-lint %{buildroot}%{_bindir}
%{__install} -m 0644 src/*.pm %{buildroot}%{perl_vendorlib}
%{__cp} -a conf hooks %{buildroot}%{_datadir}/%{name}

touch %{buildroot}%{gitolite_home}/.ssh/authorized_keys

%clean
test "%{buildroot}" != "/" -a -d "%{buildroot}" && %{__rm} -rf "%{buildroot}"

%pre
# Add user and group
/usr/sbin/groupadd -r %{gitolite_group} &>/dev/null || :
/usr/sbin/useradd -r -g %{gitolite_user} -d /home/git -m -s /bin/sh -c "git repository hosting" git &>/dev/null || :

%files
%defattr(-,root,root)
%{_bindir}/gl-*
%{_bindir}/sshkeys-lint
%{perl_vendorlib}/*.pm
%{_datadir}/%{name}
%attr(750,%{gitolite_user},%{gitolite_group}) %{gitolite_home}/.ssh
%config(noreplace) %attr(640,%{gitolite_user},%{gitolite_group}) %{gitolite_home}/.ssh/authorized_keys
%attr(644,-,-) %doc doc/COPYING doc/*


%changelog
* Thu Jan 13 2011 graf@movingtarget.de
- version 1.5.8
- auto-create git user and group
- adding dependencies and provides
* Thu Dec 16 2010 asn@cynapses.org
- Initial package version 1.5.7
