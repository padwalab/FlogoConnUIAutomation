#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */


from selenium.webdriver.common.action_chains import ActionChains
from utils import randomString, waitForElementToBeVisible, xpath_soup
from setupHelper import install
import time

try:
    from bs4 import BeautifulSoup
except ImportError:
    install("BeautifulSoup")


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
    if soup.find("div", {"class": "empty-add"}):
        createAppElem = xpath_soup(
            soup.find("div", {"id": "ng-listing-create"}))
    else:
        createAppElem = xpath_soup(
            soup.find("button", {"id": "ng-listing-create"}))
    createAppButton = browser.find_element_by_xpath(createAppElem)
    createAppButton.click()
    # print("[INFO] Creating the app:", appName)
    time.sleep(2)
    # return subCreateApp(browser, appName)


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
        appName = soup.find("div", {"id": "ng-details-edit-name"}).text
        createFlowElem = xpath_soup(
            soup.find("button", {"id": "createFlow"}))
        createFlowButton = browser.find_element_by_xpath(createFlowElem)
        createFlowButton.click()
        print("[INFO] Setting up flow...")
        time.sleep(2)
        return subCreateFlow(browser, flowName), appName


def setupFlowEnv(browser):
    browser.get("http://localhost:8090/applications")
    # if waitForElementToBeVisible(browser, "class", "empty-mode"):

    if waitForElementToBeVisible(browser, "id", "ng-listing-create"):
        appName = randomString()
        bwsr = createApp(browser, appName)
        flowName = randomString()
        bwsr, appName = createFlow(browser, flowName)
        time.sleep(5)
        return bwsr, appName


def performDelete(browser):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    if waitForElementToBeVisible(browser, "id", "ng-listing-delete-ok"):
        appDeleteElem = xpath_soup(soup.find(
            "button", {"id": "ng-listing-delete-ok"}))
        appDeleteBtn = browser.find_element_by_xpath(appDeleteElem)
        appDeleteBtn.click()
        time.sleep(2)
        print('[INFO] App deleted...')


def deleteFlow(browser, appName):
    print("deleteFlow ", appName)
    browser.get("http://localhost:8090/applications")
    if waitForElementToBeVisible(browser, "class", "appListTable"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        appListElem = soup.find(
            "div", {"class": "appListTable"})
        time.sleep(2)
        for apps in appListElem.findAll("div", {"class": "ng-table-row info custom-table-row"}):
            if apps.find("div", {"title": appName}):
                print("found the app [", appName, "]")
                actbtns = xpath_soup(apps.find(
                    "div", {"class": "action-btns"}))
                actbtnselem = browser.find_element_by_xpath(actbtns)
                hov = ActionChains(browser).move_to_element(actbtnselem)
                hov.perform()
                if waitForElementToBeVisible(browser, "class", "row-btn ng-ic ng-ic-delete"):
                    dpdwn = xpath_soup(
                        apps.find("div", {"class": "row-btn ng-ic ng-ic-delete"}))
                    dpdownbtn = browser.find_element_by_xpath(dpdwn)
                    dpdownbtn.click()
                    # dltelem = xpath_soup(
                    #     apps.find("a", {"class": "tropos-apps-delete-app mchNoDecorate"}))
                    # dltBtn = browser.find_element_by_xpath(dltelem)
                    # dltBtn.click()
                    time.sleep(5)
                    performDelete(browser)


# brwsr = FlogoInit()

# b, AName = setupFlowEnv(brwsr)
# fo = open('tests/query/selects.json', 'r')
# suite = json.load(fo)
# br = setupTestSuiteEnv(b, suite.get("config"))
# GiveInput(br, "query")

# deleteFlow(brwsr, AName)
