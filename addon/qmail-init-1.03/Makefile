DESTDIR = ""
chmod = /bin/chmod
cp = /bin/cp
install = /usr/bin/install
sed = /usr/bin/sed
touch = /usr/bin/touch

prefix = /usr/local
bindir = $(prefix)/bin
libdir = $(prefix)/lib
sharedir = $(prefix)/share/qmail
sysconfdir = /etc
rcinitdir = $(sysconfdir)/init.d
fillupdir = /var/adm/fillup-templates
permissionsdir = $(sysconfdir)/permissions.d

all:

install:
	$(install) -d -m 0755 $(DESTDIR)$(rcinitdir)
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/cron.hourly
	$(install) -m 0755 etc/cron.hourly/qmail-newusers $(DESTDIR)$(sysconfdir)/cron.hourly/qmail-newusers
	$(install) -d -m 0755 $(DESTDIR)$(permissionsdir)
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/profile.d
	$(install) -m 0755 etc/profile.d/qmail.* $(DESTDIR)$(sysconfdir)/profile.d
	for n in qmail qmail-pop3d qmail-qmqpd qmail-qmtpd qmail-smtpd ; do \
	  $(install) -d -m 1755 $(DESTDIR)$(sysconfdir)/$$n ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/$$n/env ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/$$n/log ; \
	  $(install) -m 0755 etc/$$n/run $(DESTDIR)$(sysconfdir)/$$n/run ; \
	  $(install) -m 0755 etc/$$n/log/run $(DESTDIR)$(sysconfdir)/$$n/log/run ; \
	  $(install) -m 0755 etc/init.d/$$n $(DESTDIR)$(rcinitdir)/$$n ; \
	  $(install) -m 0644 etc/permissions.d/$$n $(DESTDIR)$(permissionsdir)/$$n ; \
	done
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/qmail/alias
	$(install) -m 0644 etc/qmail/alias/.qmail-msglog $(DESTDIR)$(sysconfdir)/qmail/alias/.qmail-msglog
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/qmail-qstat
	$(install) -m 0755 etc/qmail-qstat/run $(DESTDIR)$(sysconfdir)/qmail-qstat/run
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/qmail-qread
	$(install) -m 0755 etc/qmail-qread/run $(DESTDIR)$(sysconfdir)/qmail-qread/run
	for n in pop3d qmqpd qmtpd smtpd ; do \
	  $(touch) $(DESTDIR)$(sysconfdir)/qmail-$$n/down ; \
	  $(touch) $(DESTDIR)$(sysconfdir)/qmail-$$n/log/down ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/qmail-$$n/rules ; \
	  $(install) -m 0644 etc/qmail-$$n/rules/Makefile $(DESTDIR)$(sysconfdir)/qmail-$$n/rules/Makefile ; \
	  $(install) -m 0644 etc/qmail-$$n/rules/data $(DESTDIR)$(sysconfdir)/qmail-$$n/rules/data ; \
	  ( cd $(DESTDIR)$(sysconfdir)/qmail-$$n/rules; tcprules data.cdb data.tmp <data ) ; \
	done
	$(install) -d -m 0755 $(DESTDIR)$(bindir)
	$(install) -m 0755 usr/bin/* $(DESTDIR)$(bindir)
	$(install) -d -m 0755 $(DESTDIR)$(sharedir)
	$(install) -m 0755 usr/share/qmail/create-* $(DESTDIR)$(sharedir)
	$(install) -d -m 0755 $(DESTDIR)$(fillupdir)
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.qmail* $(DESTDIR)$(fillupdir)
