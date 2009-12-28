PREFIX = ""
install = /usr/bin/install
cp = /bin/cp

sysconfdir = /etc
vmailmgrdir = $(sysconfdir)/vmailmgr
rcinitdir = $(sysconfdir)/init.d
fillupdir = /var/adm/fillup-templates
suseconfdir = /sbin/conf.d
servicedir = /var/service
permissionsdir = /etc/permissions.d
tcpcontroldir = /etc/tcpcontrol

all:

install:
	$(install) -d -m 0755 $(PREFIX)$(vmailmgrdir)/env
	$(install) -d -m 0755 $(PREFIX)$(servicedir)
	$(install) -d -m 0755 $(PREFIX)$(rcinitdir)
	$(install) -d -m 0755 $(PREFIX)$(fillupdir)
	$(install) -d -m 0755 $(PREFIX)$(suseconfdir)
	$(install) -d -m 0755 $(PREFIX)$(permissionsdir)
	$(install) -m 0644 etc/permissions.d/vmailmgr-courier-imap $(PREFIX)$(permissionsdir)
	$(install) -m 0644 var/adm/fillup-templates/sysconfig.vmailmgr $(PREFIX)$(fillupdir)
	$(install) -m 0744 sbin/conf.d/SuSEconfig.vmailmgr $(PREFIX)$(suseconfdir)
	@for n in local tcp ; do \
	  $(install) -d -m 1744 $(PREFIX)$(servicedir)/vmailmgr-$$n; \
	  $(install) -m 0744 var/service/vmailmgr-$$n/run $(PREFIX)$(servicedir)/vmailmgr-$$n; \
	  if test -d var/service/vmailmgr-$$n/log; then \
	    $(install) -d -m 0744 $(PREFIX)$(servicedir)/vmailmgr-$$n/log; \
	    $(install) -m 0744 var/service/vmailmgr-$$n/log/run $(PREFIX)$(servicedir)/vmailmgr-$$n/log; \
	  fi; \
	  test -f "etc/init.d/vmailmgrd-$$n" && \
	  $(install) -m 0744 etc/init.d/vmailmgrd-$$n $(PREFIX)$(rcinitdir)/vmailmgrd-$$n; \
	  test -f "var/adm/fillup-templates/sysconfig.vmailmgr-$$n" && \
	    $(install) -m 0644 var/adm/fillup-templates/sysconfig.vmailmgr-$$n $(PREFIX)$(fillupdir); \
	  test -f "sbin/conf.d/SuSEconfig.vmailmgr-$$n" && \
	    $(install) -m 0744 sbin/conf.d/SuSEconfig.vmailmgr-$$n $(PREFIX)$(suseconfdir); \
	done
	$(install) -d -m 0755 $(PREFIX)$(tcpcontroldir)
	$(install) -m 0644 etc/tcpcontrol/vmailmgr.rules $(PREFIX)$(tcpcontroldir)
	cd $(PREFIX)$(tcpcontroldir) && tcprules vmailmgr.cdb vmailmgr.tmp <vmailmgr.rules
