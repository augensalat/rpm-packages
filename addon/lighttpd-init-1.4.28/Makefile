DESTDIR = ""
CFLAGS = -O
LD = $(CC)
LDFLAGS = -s
chmod = /bin/chmod
cp = /bin/cp
install = /usr/bin/install
sed = /usr/bin/sed
touch = /usr/bin/touch

prefix = /usr/local
sysconfdir = /etc
libdir = $(prefix)/lib
sharedir = $(prefix)/share/lighttpd
rcinitdir = $(sysconfdir)/init.d
lighttpddir = $(sysconfdir)/lighttpd
fillupdir = /var/adm/fillup-templates
permissionsdir = $(sysconfdir)/permissions.d

all:

install:
	$(install) -d -m 1755 $(DESTDIR)$(lighttpddir)
	$(install) -d -m 0750 $(DESTDIR)$(lighttpddir)/conf.d
	$(install) -d -m 0750 $(DESTDIR)$(lighttpddir)/env
	$(install) -d -m 0755 $(DESTDIR)$(lighttpddir)/log
	$(install) -d -m 0750 $(DESTDIR)$(lighttpddir)/vhosts.d
	$(install) -d -m 0755 $(DESTDIR)$(rcinitdir)
	$(install) -d -m 0755 $(DESTDIR)$(fillupdir)
	$(install) -d -m 0755 $(DESTDIR)$(sharedir)
	$(install) -d -m 0755 $(DESTDIR)$(permissionsdir)
	$(install) -m 0640 etc/lighttpd/lighttpd.conf $(DESTDIR)$(lighttpddir)
	$(install) -m 0640 etc/lighttpd/conf.d/*.conf $(DESTDIR)$(lighttpddir)/conf.d
	$(install) -m 0640 etc/lighttpd/env/* $(DESTDIR)$(lighttpddir)/env
	$(install) -m 0640 etc/lighttpd/vhosts.d/* $(DESTDIR)$(lighttpddir)/vhosts.d
	$(install) -m 0644 etc/permissions.d/lighttpd $(DESTDIR)$(permissionsdir)
	$(install) -m 0744 etc/lighttpd/run $(DESTDIR)$(lighttpddir)
	$(install) -m 0744 etc/lighttpd/log/run $(DESTDIR)$(lighttpddir)/log
	$(touch) $(DESTDIR)$(lighttpddir)/down
	$(touch) $(DESTDIR)$(lighttpddir)/log/down
	$(install) -m 0744 etc/init.d/lighttpd $(DESTDIR)$(rcinitdir)/lighttpd
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.lighttpd $(DESTDIR)$(fillupdir)
	$(sed) -e "s:###LIBDIR###:$(libdir):g" -e "s:###CONFDIR###:$(lighttpddir)/conf.d:g" \
		usr/share/lighttpd/create-config \
		>$(DESTDIR)$(sharedir)/create-config
	$(chmod) 0755 $(DESTDIR)$(sharedir)/create-config
	$(install) -m 0755 usr/share/lighttpd/create-log-config $(DESTDIR)$(sharedir)

