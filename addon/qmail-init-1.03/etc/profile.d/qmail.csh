[ -r /etc/qmail/env/QMAIL_DEFAULTDELIVERY ]
if ($status == 0) then
	set tmpmail=`head -1 /etc/qmail/env/QMAIL_DEFAULTDELIVERY | sed -e '/^[^.]/d' -e "s|^|${HOME}/|" -e 's|/\./|/|g' | tail -1`
	if ("$tmpmail" != "") then
		setenv MAIL "$tmpmail"
	endif
	unset tmpmail
else
	setenv MAIL "${HOME}/Maildir/"
endif
setenv MAILDIR "$MAIL"

[ -d ./Maildir ]
if ($status != 0) then
	maildirmake Maildir
endif
