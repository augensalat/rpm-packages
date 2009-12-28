DESTDIR = ""
install = /usr/bin/install
sysconfdir = /etc
sfw2servicesdir = $(sysconfdir)/sysconfig/SuSEfirewall2.d/services

all:

install:
	$(install) -d -m 0755 $(DESTDIR)$(sfw2servicesdir)
	$(install) -m 0644 etc/sysconfig/SuSEfirewall2.d/services/qmail* $(DESTDIR)$(sfw2servicesdir)
