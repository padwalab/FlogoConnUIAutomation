#!/usr/bin/python3

import time
from setupHelper import install
try:
    from bs4 import BeautifulSoup
except ImportError:
    install("BeautifulSoup")
from utils import randomString, waitForElementToBeVisible, xpath_soup


def subCreateApp(browser, appName):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    nameAppElem = xpath_soup(
        soup.find("input", {"id": "applicationName"}))
    nameAppButton = browser.find_element_by_xpath(nameAppElem)
    nameAppButton.send_keys(appName)

    createElem = xpath_soup(
        soup.find("span", {"translate": "TROPOS_APPS_CREATE.CREATE"}))
    createBtn = browser.find_element_by_xpath(createElem)
    createBtn.click()
    # time.sleep(2)
    return browser


def createApp(browser, appName):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    createAppElem = xpath_soup(
        soup.find("button", {"id": "tropos-create-app"}))
    createAppButton = browser.find_element_by_xpath(createAppElem)
    createAppButton.click()
    print("[INFO] Creating the app:", appName)
    # time.sleep(2)
    return subCreateApp(browser, appName)


def subCreateFlow(browser, flowName):
    time.sleep(5)
    if waitForElementToBeVisible(browser, "id", "flowName", 20):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        nameFlowElem = xpath_soup(
            soup.find("input", {"id": "flowName"}))
        nameFlowButton = browser.find_element_by_xpath(nameFlowElem)
        nameFlowButton.send_keys(flowName)

        createElem = xpath_soup(
            soup.find("button", {"id": "nextCreateFlow"}))
        createBtn = browser.find_element_by_xpath(createElem)
        createBtn.click()
        time.sleep(2)
        return browser


def createFlow(browser, flowName):
    if waitForElementToBeVisible(browser, "id", "createFlow"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        createFlowElem = xpath_soup(
            soup.find("button", {"id": "createFlow"}))
        createFlowButton = browser.find_element_by_xpath(createFlowElem)
        createFlowButton.click()
        print("[INFO] Setting up flow...")
        time.sleep(2)
        return subCreateFlow(browser, flowName)


def setupFlowEnv(browser):
    browser.get("http://localhost:8090/applications")
    if waitForElementToBeVisible(browser, "class", "tropos-inline-block-right"):
        appName = randomString()
        bwsr = createApp(browser, appName)
        flowName = randomString()
        bwsr = createFlow(bwsr, flowName)
        time.sleep(5)
        return bwsr, appName


def performDelete(browser):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    appDeleteElem = xpath_soup(soup.find(
        "button", {"class": "tc-buttons tc-buttons-primary tc-modal-content-right-margin"}))
    appDeleteBtn = browser.find_element_by_xpath(appDeleteElem)
    appDeleteBtn.click()
    time.sleep(2)
    print('[INFO] App deleted...')


def deleteFlow(browser, appName):
    print("deleteFlow ", appName)
    browser.get("http://localhost:8090/applications")
    if waitForElementToBeVisible(browser, "class", "tropos-inline-block-right"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        appListElem = soup.find(
            "div", {"class": "tropos-applications-main-panel"})
        time.sleep(2)
        for apps in appListElem.findAll("div", {"class": "tropos-appbox-main-panel col-md-12"}):
            if appName in apps.find("div", {"class": "tropos-appbox-content-name-app ng-binding"}).text:
                print("found the app [", appName, "]")
                dpdwn = xpath_soup(
                    apps.find("div", {"class": "tropos-apps-actions ng-isolate-scope"}))
                dpdownbtn = browser.find_element_by_xpath(dpdwn)
                dpdownbtn.click()
                dltelem = xpath_soup(
                    apps.find("a", {"class": "tropos-apps-delete-app mchNoDecorate"}))
                dltBtn = browser.find_element_by_xpath(dltelem)
                dltBtn.click()
                time.sleep(2)
                performDelete(browser)


# brwsr = FlogoInit()

# b, AName = setupFlowEnv(brwsr)
# fo = open('tests/query/selects.json', 'r')
# suite = json.load(fo)
# br = setupTestSuiteEnv(b, suite.get("config"))
# GiveInput(br, "query")

# deleteFlow(brwsr, AName)
