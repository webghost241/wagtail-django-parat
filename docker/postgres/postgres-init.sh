#!/usr/bin/env bash

set -e
set -o pipefail

if [ -f /var/tmp/parat.dump ]; then
	pg_restore -U "$POSTGRES_USER" -v -d parat --no-acl /var/tmp/parat.dump || true
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$dbname" <<-EOSQL ;
	ALTER SCHEMA "production-parat" RENAME TO ${DJANGO_ENVIRONMENT};
	EOSQL
	pg_restore -U "$POSTGRES_USER" -v -d parat --no-acl /var/tmp/parat.dump || true
else
	for dbname in template1 "$POSTGRES_DB"; do
		psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$dbname" <<-EOSQL ;
			CREATE SCHEMA IF NOT EXISTS "${DJANGO_ENVIRONMENT}";
		EOSQL
	done
fi
