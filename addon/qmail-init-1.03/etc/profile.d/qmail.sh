MAIL=${HOME}/Maildir/
MAILDROP="$MAIL"
export MAIL MAILDROP

test -d Maildir || maildirmake Maildir
