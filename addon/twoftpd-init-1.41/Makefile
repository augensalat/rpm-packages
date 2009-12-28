DESTDIR = ""
install = /usr/bin/install
touch = /usr/bin/touch
test = /usr/bin/test

prefix = /usr/local
bindir = $(prefix)/bin
sharedir = $(prefix)/share/twoftpd
sysconfdir = /etc
rcinitdir = $(sysconfdir)/init.d
fillupdir = /var/adm/fillup-templates
permissionsdir = $(sysconfdir)/permissions.d
logdir = /var/log

all:

install:
	$(install) -d -m 0755 $(DESTDIR)$(rcinitdir)
	$(install) -d -m 0755 $(DESTDIR)$(permissionsdir)
	$(install) -d -m 0755 $(DESTDIR)$(fillupdir)
	$(install) -d -m 0755 $(DESTDIR)$(sharedir)
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.twoftpd $(DESTDIR)$(fillupdir)
	$(install) -d -m 1755 $(DESTDIR)$(sysconfdir)/twoftpd
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/twoftpd/env
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/twoftpd/log
	$(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/twoftpd/rules
	$(install) -m 0754 etc/twoftpd/run $(DESTDIR)$(sysconfdir)/twoftpd/run
	$(install) -m 0754 etc/twoftpd/log/run $(DESTDIR)$(sysconfdir)/twoftpd/log/run
	$(touch) $(DESTDIR)$(sysconfdir)/twoftpd/down
	$(touch) $(DESTDIR)$(sysconfdir)/twoftpd/log/down
	$(install) -m 0754 etc/init.d/twoftpd $(DESTDIR)$(rcinitdir)/twoftpd
	$(install) -m 0644 etc/twoftpd/env/* $(DESTDIR)$(sysconfdir)/twoftpd/env
	$(install) -m 0644 etc/twoftpd/rules/Makefile $(DESTDIR)$(sysconfdir)/twoftpd/rules/Makefile
	$(install) -m 0644 etc/twoftpd/rules/data $(DESTDIR)$(sysconfdir)/twoftpd/rules/data
	$(install) -m 0644 etc/twoftpd/rules/include $(DESTDIR)$(sysconfdir)/twoftpd/rules/include
	( cd $(DESTDIR)$(sysconfdir)/twoftpd/rules; tcprules data.cdb data.tmp <data )
	$(install) -m 0644 etc/permissions.d/twoftpd $(DESTDIR)$(permissionsdir)/twoftpd
	$(install) -m 0755 usr/share/twoftpd/create-config $(DESTDIR)$(sharedir)
	$(install) -m 0755 usr/share/twoftpd/create-log-config $(DESTDIR)$(sharedir)
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.twoftpd $(DESTDIR)$(fillupdir)
	$(install) -d -m 0700 $(DESTDIR)$(logdir)/twoftpd
