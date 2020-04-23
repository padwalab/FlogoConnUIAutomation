# purpose of this script is to setup required DBs
#
# author Abhijeet Padwal [apadwal@tibco.com]

#!/bin/sh
pg_restore -h postgres_test -p 5432 -U postgres -d dvdrental /home/apadwal/dvdrental.tar
