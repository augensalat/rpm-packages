DESTDIR = ""
install = /usr/bin/install
touch = /usr/bin/touch
test = /usr/bin/test

prefix = /usr/local
bindir = $(prefix)/bin
sharedir = $(prefix)/share/qmail
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
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.mailfront $(DESTDIR)$(fillupdir)
	for n in imapd imapsd pop3d pop3sd qmqpd qmtpd smtpd smtpsd submissiond; do \
	  $(install) -d -m 1755 $(DESTDIR)$(sysconfdir)/mailfront-$$n ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/mailfront-$$n/env ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/mailfront-$$n/log ; \
	  $(install) -d -m 0755 $(DESTDIR)$(sysconfdir)/mailfront-$$n/rules ; \
	  $(install) -m 0754 etc/mailfront-$$n/run $(DESTDIR)$(sysconfdir)/mailfront-$$n/run ; \
	  $(install) -m 0754 etc/mailfront-$$n/log/run $(DESTDIR)$(sysconfdir)/mailfront-$$n/log/run ; \
	  $(touch) $(DESTDIR)$(sysconfdir)/mailfront-$$n/down ; \
	  $(touch) $(DESTDIR)$(sysconfdir)/mailfront-$$n/log/down ; \
	  $(install) -m 0754 etc/init.d/mailfront-$$n $(DESTDIR)$(rcinitdir)/mailfront-$$n ; \
	  $(install) -m 0644 etc/mailfront-$$n/env/* $(DESTDIR)$(sysconfdir)/mailfront-$$n/env ; \
	  $(install) -m 0644 etc/mailfront-$$n/rules/Makefile $(DESTDIR)$(sysconfdir)/mailfront-$$n/rules/Makefile ; \
	  $(install) -m 0644 etc/mailfront-$$n/rules/data $(DESTDIR)$(sysconfdir)/mailfront-$$n/rules/data ; \
	  $(install) -m 0644 etc/mailfront-$$n/rules/include $(DESTDIR)$(sysconfdir)/mailfront-$$n/rules/include ; \
	  ( cd $(DESTDIR)$(sysconfdir)/mailfront-$$n/rules; tcprules data.cdb data.tmp <data ) ; \
	  if $(test) -d etc/mailfront-$$n/ssl ; then \
	    $(install) -d -m 0750 $(DESTDIR)$(sysconfdir)/mailfront-$$n/ssl ; \
	    $(install) -m 0644 etc/mailfront-$$n/ssl/openssl.cnf $(DESTDIR)$(sysconfdir)/mailfront-$$n/ssl/openssl.cnf ; \
	  fi ; \
	  $(install) -m 0644 etc/permissions.d/mailfront-$$n $(DESTDIR)$(permissionsdir)/mailfront-$$n ; \
	  $(install) -m 0755 usr/share/mailfront/create-config-mailfront-$$n $(DESTDIR)$(sharedir) ; \
	  $(install) -m 0755 usr/share/mailfront/create-log-config-mailfront-$$n $(DESTDIR)$(sharedir) ; \
	  $(install) -m 0644 var/adm/fillup-templates/sysconfig.mailfront-$$n $(DESTDIR)$(fillupdir) ; \
	  $(install) -d -m 0700 $(DESTDIR)$(logdir)/mailfront-$$n; \
	done
