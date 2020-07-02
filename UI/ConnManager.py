#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

import time
from utils import waitForElementToBeVisible, xpath_soup
from setupHelper import install
try:
    from bs4 import BeautifulSoup
except ImportError:
    install("bs4")
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


connPool = []


def addConnectionToPool(cnName):
    connPool.append(cnName)


def getConnectionPool():
    return connPool


def deleteConnection(browser, connName):
    # time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    if waitForElementToBeVisible(
            browser, "id", "ng-listing-delete-ok"):
        deleteButton = xpath_soup(soup.find(
            "button", {"id": "ng-listing-delete-ok"}))
        # if connection.find("div", {"class": "text-muted"}).text == connName:
        #     deleteButton = xpath_soup(connection.find(
        #         "button", {"id": "ng-listing-delete-ok"}))
        deleteElem = browser.find_element_by_xpath(deleteButton)
        deleteElem.click()


def fillConnectionDetails(browser, conn):
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    connForm = soup.find(
        "div", {"class": "connection-modal ui-dialog ui-widget ui-widget-content ui-corner-all ui-shadow"})
    time.sleep(2)
    NameElem = xpath_soup(connForm.find("input", {
                          "id": "name"}))
    nameInput = browser.find_element_by_xpath(NameElem)
    nameInput.send_keys(conn.get("Name"))

    HostElem = xpath_soup(connForm.find("input", {
                          "id": "host"}))
    hostInput = browser.find_element_by_xpath(HostElem)
    hostInput.send_keys(conn.get("Host"))

    PortElem = xpath_soup(connForm.find("input", {
                          "id": "port"}))
    portInput = browser.find_element_by_xpath(PortElem)
    portInput.clear()
    portInput.send_keys(conn.get("Port"))

    DBElem = xpath_soup(connForm.find("input", {
        "id": "databaseName"}))
    DBInput = browser.find_element_by_xpath(DBElem)
    DBInput.send_keys(conn.get("DatabaseName"))

    UserElem = xpath_soup(connForm.find("input", {
        "id": "user"}))
    UserInput = browser.find_element_by_xpath(UserElem)
    UserInput.send_keys(conn.get("User"))

    PwdElem = xpath_soup(connForm.find("input", {
        "id": "password"}))
    PwdInput = browser.find_element_by_xpath(PwdElem)
    PwdInput.send_keys(conn.get("Password"))
    time.sleep(5)
    ConnectElem = xpath_soup(
        soup.find("button", {"class": "btn btn-primary pull-right"}))
    ConnetButton = browser.find_element_by_xpath(ConnectElem)
    ConnetButton.click()

    if waitForElementToBeVisible(browser, "class", "listing-body"):
        addConnectionToPool(conn.get("Name"))
        print("Connection Successful!")
    else:
        print("Connection Fialed")


def subCreateConnection(browser, conn):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    if waitForElementToBeVisible(
            browser, "class", "ng-modal-content"):
        connTile = soup.find(
            "div", {"class": "ng-modal-content"})
        for connectorConnectionTiles in connTile.findAll("div", {"class": "conn-tile"}):
            if connectorConnectionTiles.find("div", {"class": "conn-name"}).text == conn.get("ConnectorName") + " Connector":
                tileElem = xpath_soup(connectorConnectionTiles)
                tileButton = browser.find_element_by_xpath(tileElem)
                tileButton.click()
                print("[INFO] Filling the connection details...")
                fillConnectionDetails(browser, conn)


def createConnection(browser, connSidebar, conn):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    createElem = xpath_soup(soup.find(
        "button", {"id": "ng-listing-create"}))
    createButton = browser.find_element_by_xpath(createElem)
    createButton.click()
    subCreateConnection(browser, conn)


def handleConnection(browser, connDetails):
    browser.get("http://localhost:8090/connections")
    if waitForElementToBeVisible(browser, "id", "ng-listing-create"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        connectionSidebar = soup.find(
            "div", {"class": "conn-list-table"})
        connrows = connectionSidebar.findAll(
            "div", {"class": "ng-table-row info"})
        for conntiles in connrows:
            if conntiles.find("span", {"class": "conn-name"}).text == connDetails.get("Name"):
                if conntiles.find("div", {"class": "row-btn ng-ic ng-ic-delete disabled"}):
                    print(
                        "\n[INFO]Connection with same name exists\nCan't delete connection because it is being used in app...\n")
                    return
                # actbtns = browser.find_element_by_class_name(
                    # "action-btns")
                actbtns = xpath_soup(conntiles.find(
                    "div", {"class": "action-btns"}))
                actbtnselem = browser.find_element_by_xpath(actbtns)
                hov = ActionChains(browser).move_to_element(actbtnselem)
                hov.perform()
                showDelete = xpath_soup(
                    conntiles.find("div", {"class": "row-btn ng-ic ng-ic-delete"}))
                elem = browser.find_element_by_xpath(showDelete)
                elem.click()
                print("[INFO] Connection Exists... Re-creating and validating conn: ",
                      connDetails.get("Name"))
                deleteConnection(browser, connDetails.get("Name"))
                break
        print("[INFO] Creating connection...")
        createConnection(browser, connectionSidebar, connDetails)


# f = open('connection.json', 'r')
# conn = json.load(f)
# brwsr = FlogoInit()
# for item in conn:
#     handleConnection(brwsr, item)
