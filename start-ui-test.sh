# purpose of this script is to run the extensive test suite for dbservice
#
# author Abhijeet Padwal [apadwal@tibco.com]

#!/bin/sh
docker network disconnect flogoconnuiautomation_dbservice_ui_test_net flogo-studio

docker-compose -f docker-compose.test.yml rm -fv postgres_dbui_test
docker-compose -f docker-compose.test.yml rm -fv mysql_dbui_test
# docker-compose -f docker-compose.test.yml rm -fv sqlserver_dbui_test
docker-compose -f docker-compose.test.yml up -d --build
sleep 5
docker network connect flogoconnuiautomation_dbservice_ui_test_net flogo-studio
cd UI/
python3 dbUITests.py
# cd ..
# docker-compose -f docker-compose.test.yml down
docker network disconnect flogoconnuiautomation_dbservice_ui_test_net flogo-studio
