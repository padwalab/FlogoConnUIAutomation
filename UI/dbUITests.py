#!/usr/bin/python3

import json
import glob
import time
from setupHelper import install
try:
    from selenium import webdriver
except ImportError:
    install("selenium")
    install("chromedriver")
from ConnManager import getConnectionPool, handleConnection
from flowSetup import deleteFlow, randomString, setupFlowEnv
from suiteSetup import setupTestSuiteEnv
from SqlQueryTester import runTestSuite

reportFile = "./reports/reportFile"+randomString(3)+".txt"


def FlogoInit():
    # options = Options()
    # options.add_argument("--headless")
    # browser = webdriver.Chrome(options=options)
    # browser = webdriver.Chrome()
    browser = webdriver.Chrome(executable_path='../webdriver/chromedriver')

    browser.get("http://localhost:8090/")
    return browser


f = open('connection.json', 'r')
connections = json.load(f)
print("[INFO] Initializing the Flogo Studio...")
brwsr = FlogoInit()
print("[INFO] Addition connections...")
for conn in connections:
    handleConnection(brwsr, conn)
cns = getConnectionPool()
print("[INFO] Connections Added...", cns)

for testJson in glob.glob("tests/*/"):
    print("[INFO] Running test cases in ", testJson)
    for suites in glob.glob(testJson+"*.json"):
        print("[INFO] Setting up the flow environment...")
        b, AName = setupFlowEnv(brwsr)
        fo = open(suites, 'r')
        suite = json.load(fo)
        fo.close()
        print("[INFO] Setting up the TestSuites ...")
        if suite.get("config").get("connectionName") in cns:
            brwsr = setupTestSuiteEnv(brwsr, suite.get("config"))
            print("[INFO] Running tests from ",
                  suite.get("suitename"), "...")
            with open(reportFile, 'a') as routfile:
                routfile.write("\nDBUiTests " + testJson + ": " +
                               suite.get("suitename") + "\t \n")
                routfile.close()
            testCaseList = suite.get("testcases")
            for test in testCaseList:
                print("[INFO] Running test case ", test.get("testName"))
                runTestSuite(brwsr, test, reportFile)
                time.sleep(5)
        else:
            print("[ERROR] Connection ->", suite.get("config").get("connectionName"),
                  " used in testSuite ", suite.get("suitename"), "\nis not validated, check the connection details")
        print("[INFO] Cleaning the created apps...")
        deleteFlow(brwsr, AName)

time.sleep(5)

brwsr.close()

# def ScraperSetup():
#     # options = Options()
#     # options.add_argument("--headless")
#     # browser = webdriver.Chrome(options=options)
#     browser = webdriver.Chrome()
#     FLOGO_URL = 'http://localhost:8090'

#     browser.get(FLOGO_URL)
#     return browser
# # connection test folder structure:
# # - AutomationHome10559
# #   - automation/
# #       - connectors/
# #           - SQLServer/
# #               - content/
# #                   - ui-e2e-tests/
# #                       - dbtests/
# #                           - connections/
# #                               - conn.json
# #                           - tests/
# #                               - test.json


# print("[INFO] Setting up Scraper Setup...")
# sc = ScraperSetup()
# createConnections(sc)
