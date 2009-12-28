DESTDIR = ""
install = /usr/bin/install
cp = /bin/cp

prefix = /usr/local
sharedir = $(prefix)/share/cvm
sysconfdir = /etc
rcinitdir = $(sysconfdir)/init.d
cvmdir = $(sysconfdir)/cvm
fillupdir = /var/adm/fillup-templates
permissionsdir = $(sysconfdir)/permissions.d
logdir = /var/log

all:

install:
	$(install) -d -m 0755 $(DESTDIR)$(rcinitdir)
	$(install) -d -m 0755 $(DESTDIR)$(permissionsdir)
	$(install) -d -m 0755 $(DESTDIR)$(fillupdir)
	$(install) -d -m 0755 $(DESTDIR)$(sharedir)
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.cvm $(DESTDIR)$(fillupdir)
	$(install) -m 0644 etc/permissions.d/* $(DESTDIR)$(permissionsdir)
	for n in cvm-qmail-local cvm-qmail-udp cvm-vmailmgr-local \
	    cvm-vmailmgr-udp cvm-vmlookup-local cvm-vmlookup-udp ; do \
	  $(install) -d -m 1755 $(DESTDIR)$(sysconfdir)/$$n ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/$$n/env ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/$$n/log ; \
	  $(install) -m 0754 etc/$$n/run $(DESTDIR)$(sysconfdir)/$$n/run ; \
	  $(install) -m 0754 etc/$$n/log/run $(DESTDIR)$(sysconfdir)/$$n/log/run ; \
	  $(install) -m 0644 etc/$$n/env/* $(DESTDIR)$(sysconfdir)/$$n/env ; \
	  $(install) -m 0755 usr/share/cvm/create-config-$$n $(DESTDIR)$(sharedir) ; \
	  $(install) -m 0755 usr/share/cvm/create-log-config-$$n $(DESTDIR)$(sharedir) ; \
	  $(install) -d -m 0700 $(DESTDIR)$(logdir)/$$n ; \
	done
	for n in cvm-qmail-local cvm-qmail-udp cvm-vmailmgr-local cvm-vmailmgr-udp ; do \
	  $(install) -m 0744 etc/init.d/$$n $(DESTDIR)$(rcinitdir)/$$n ; \
	  $(install) -m 0644 var/adm/fillup-templates/sysconfig.$$n $(DESTDIR)$(fillupdir) ; \
	done
