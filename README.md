# FlogoConnUIAutomation
Flogo dbconnectors ui automation framework, validate query, verify schema

## Prerequisites DBConnectors UI automation:
	1. Docker, Docker-compose
	2. python3 + pip
	3. chromedriver (please find the compatible chromedriver)

## To Run DBConnectors UI automation:
	./start-ui-test.sh

## To explore test suites and modify:
	./tests-manager.sh


## How the automation works:

### Step 1:
#### A. Either have FECLI automation run as parent script
OR
#### B. Fulfill therse reqs:
	1. Make sure you have flogo up and running(if you're skipping the FECLI** setup)
	2. Also, You need the dbconnectors* installed

### Step 2:
	1. run ./start-ui-test.sh
