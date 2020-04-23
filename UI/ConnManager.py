#!/usr/bin/python3

import time
from utils import waitForElementToBeVisible, xpath_soup
from bs4 import BeautifulSoup
from selenium import webdriver


connPool = []


def addConnectionToPool(cnName):
    connPool.append(cnName)


def getConnectionPool():
    return connPool


def deleteConnection(browser, connName):
    # time.sleep(1)
    if waitForElementToBeVisible(
            browser, "class", "wi-card-detail-title-container-connection"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        connection = soup.find(
            "div", {"class": "wi-card-detail-title-container-connection"})
        if connection.find("div", {"class": "wi-card-detail-subtitle-connection"}).text == connName:
            deleteButton = xpath_soup(connection.find(
                "button", {"class": "wi-tc-buttons-link pull-left"}))
            deleteElem = browser.find_element_by_xpath(deleteButton)
            deleteElem.click()


def fillConnectionDetails(browser, conn):
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    connForm = soup.find(
        "div", {"class": "wi-modal-form-builder-container largeForm"})

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

    ConnectElem = xpath_soup(
        soup.find("button", {"class": "btn btn-primary pull-right"}))
    ConnetButton = browser.find_element_by_xpath(ConnectElem)
    ConnetButton.click()

    if waitForElementToBeVisible(browser, "class", "wi-connections-ta-sidebar"):
        addConnectionToPool(conn.get("Name"))
        print("Connection Successful!")
    else:
        print("Connection Fialed")


def subCreateConnection(brwsr, conn):
    if waitForElementToBeVisible(
            brwsr, "class", "wi-card-modal-container-connection-type"):
        soup = BeautifulSoup(brwsr.page_source, "html.parser")
        connTile = soup.find(
            "div", {"class": "wi-card-modal-container-connection-type"})
        for connectorConnectionTiles in connTile.findAll("div", {"class": "wi-card-background-connection-type"}):
            if connectorConnectionTiles.find("div", {"class": "wi-card-title-connector wide-card-title"}).text == conn.get("ConnectorName") + " Connector":
                tileElem = xpath_soup(connectorConnectionTiles)
                tileButton = brwsr.find_element_by_xpath(tileElem)
                tileButton.click()
                print("[INFO] Filling the connection details...")
                fillConnectionDetails(brwsr, conn)


def createConnection(browser, connSidebar, conn):
    createElem = xpath_soup(connSidebar.find(
        "div", {"class": "wi-connections-title-add-connection pull-left"}))
    createButton = browser.find_element_by_xpath(createElem)
    createButton.click()
    subCreateConnection(browser, conn)


def handleConnection(browser, connDetails):
    browser.get("http://localhost:8090/wistudio/connections")
    if waitForElementToBeVisible(browser, "class", "wi-connections-ta-sidebar"):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        connectionSidebar = soup.find(
            "div", {"class": "wi-connections-ta-sidebar"})

        for conntiles in connectionSidebar.findAll("div", {"class": "wi-card-header-container-connector"}):
            if conntiles.find("div", {"class": "wi-card-subtitle-connector"}).text == connDetails.get("Name"):
                showDelete = xpath_soup(
                    conntiles.find("div", {"class": "wi-card-subtitle-connector"}))
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
