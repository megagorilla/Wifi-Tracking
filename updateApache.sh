rm -rf /var/www/htmlold
mv /var/www/html /var/www/htmlold
rm -rf /var/www/html
cp -a html /var/www/html
cp -a SQL /var/www/html/SQL
