#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

from utils import waitForElementToBeVisible, xpath_soup
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys


def checkResults(br):
    waitForElementToBeVisible(br, "class", "errorMessage text-danger show")
    soup = BeautifulSoup(br.page_source, "html.parser")
    if soup.find("div", {"class": "errorMessage text-danger show"}):
        print("[RESULT] Query failed")
        return True
    else:
        print("[RESULT] Qoery succcess")
        return False


def runTestSuite(br, query, reportFile):
    if waitForElementToBeVisible(br, "id", "Query"):
        soup = BeautifulSoup(br.page_source, "html.parser")

        inputElem = soup.find("ace-editor", {"id": "Query"})
        # print(qureyinputElem)
        qureyinputElem = xpath_soup(inputElem.find(
            "textarea", {"class": "ace_text-input"}))
        queryInputBox = br.find_element_by_xpath(qureyinputElem)
        queryInputBox.send_keys(Keys.CONTROL + 'a' +
                                Keys.NULL, query.get("query"))
        failed = checkResults(br)
        if not failed:
            with open(reportFile, 'a') as routfile:
                routfile.write("\n" + query.get("testName") + ":\t\tPassed\n")
                routfile.close()
            print("\n[INFO] @@@@@@testCase Has passed@@@@@@")
        elif failed:
            with open(reportFile, 'a') as routfile:
                routfile.write("\n" + query.get("testName") + ":\t\tFailed\n")
                routfile.close()
            print("\n[INFO] @@@@@@testCase Has Failed@@@@@@")
