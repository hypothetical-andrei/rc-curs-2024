openssl req -x509 -newkey rsa:4096 -keyout serv.key -out serv.crt -days 365 -nodes \
-subj "/C=RO/ST=State/L=City/O=Organization/OU=Department/CN=localhost"
# export SSLKEYLOGFILE=~/sslkeylog.log
