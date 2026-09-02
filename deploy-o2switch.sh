#!/usr/bin/env bash
# Déploie le site statique sur artcadres.lu (o2switch) via FTP.
# NE PAS lancer tant que la carte 301 n'est pas prête (SEO/REDIRECTIONS-301.md)
# et qu'une sauvegarde WordPress n'a pas été faite. mirror --delete EFFACE le WP.
# Au cutover : SITE_URL = https://artcadres.lu dans build.py, puis ce script.
# Usage :
#   export FTP_USER="votre_user"
#   export FTP_PASS="votre_pass"
#   ./deploy-o2switch.sh
set -euo pipefail
cd "$(dirname "$0")"

: "${FTP_USER:?Définir FTP_USER}"
: "${FTP_PASS:?Définir FTP_PASS}"

FTP_HOST="${FTP_HOST:-artcadres.lu}"
FTP_DIR="${FTP_DIR:-public_html}"

python3 build.py

command -v lftp >/dev/null || { echo "Installer lftp : brew install lftp"; exit 1; }

# .htaccess : index.html avant WordPress (o2switch uniquement)
cat > /tmp/artcadres-htaccess <<'HT'
DirectoryIndex index.html index.php
Options -Indexes
HT

lftp -u "$FTP_USER","$FTP_PASS" "$FTP_HOST" <<EOF
set ssl:verify-certificate no
set ftp:ssl-allow yes
cd $FTP_DIR
put /tmp/artcadres-htaccess -o .htaccess
mirror -R --verbose --delete --exclude .git/ --exclude '*.py' --exclude README.md --exclude deploy-o2switch.sh \
  . .
bye
EOF

echo "OK — https://artcadres.lu/ (vider le cache navigateur si besoin)"
