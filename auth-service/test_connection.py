import os
import sys

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'HOST_NO_ENCONTRADO')
REDIS_HOST = os.environ.get('REDIS_HOST', 'HOST_NO_ENCONTRADO')

if POSTGRES_HOST == 'HOST_NO_ENCONTRADO':
    print("ERROR: POSTGRES_HOST no fue inyectada.")
    sys.exit(1)

print(f"POSTGRES_HOST: {POSTGRES_HOST}")
print(f"REDIS_HOST: {REDIS_HOST}")