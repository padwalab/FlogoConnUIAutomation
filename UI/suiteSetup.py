#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

import time
from bs4 import BeautifulSoup
from utils import waitForElementToBeVisible, xpath_soup


def addConnection(br, cnToBeSelected):
    if waitForElementToBeVisible(br, "id", "Connection"):
        soup = BeautifulSoup(br.page_source, "html.parser")
        time.sleep(2)
        br.find_element_by_xpath(
            "//select[@id='Connection']/option[text()='" + cnToBeSelected + "']").click()
        print("[INFO] Selecting Connection for activity Connection: ", cnToBeSelected)
        time.sleep(2)
        br.find_element_by_id("explicitSaveBtn").click()
        br.find_element_by_id("catInputSettings").click()
        return br


def selectActivityTyppe(browser, actName):
    if waitForElementToBeVisible(browser, "class", "ta-types-container"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        activityContainer = soup.find("div", {"class": "ta-types-container"})
        for acts in activityContainer.findAll("div", {"class": "ta-type-label"}):
            if acts.text == actName:
                print("[INFO] Selecting Connector activity: ", actName)
                actElem = xpath_soup(acts)
                actBtn = browser.find_element_by_xpath(actElem)
                actBtn.click()
        return browser


def selectActivity(browser, config):
    if waitForElementToBeVisible(browser, "class", "form-container"):
        conFound = False
        soup = BeautifulSoup(browser.page_source, "html.parser")
        activitySidebar = soup.find(
            "div", {"class": "ta-sidebar ta-task-menu"})
        for cnctrName in activitySidebar.findAll("div", {"class": "categorySelector"}):
            if config.get("connectorname") in cnctrName.text:
                print("[INFO] Selecting Connector category: ",
                      config.get("connectorname"))
                conFound = True
                connectorTabElem = xpath_soup(cnctrName)
                connectorTabBtn = browser.find_element_by_xpath(
                    connectorTabElem)
                connectorTabBtn.click()
                break
        if conFound:
            return selectActivityTyppe(browser, config.get("activityname"))
        else:
            return browser


def setupTestSuiteEnv(browser, config):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    if waitForElementToBeVisible(browser, "class", "diagram-container"):
        addActivityElem = xpath_soup(
            soup.find("div", {"data-flogo-node-type": "node_add"}))
        addActivityButton = browser.find_element_by_xpath(addActivityElem)
        addActivityButton.click()
        print("[INFO] Adding Flow activity...")
        br = selectActivity(browser, config)
        br = addConnection(br, config.get("connectionName"))
        return br
