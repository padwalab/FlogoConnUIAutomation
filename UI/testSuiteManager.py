#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

import glob
import json


def listTestFolders():
    for idx, testfolder in enumerate(glob.glob("tests/*/")):
        print(str(idx+1) + " " + testfolder[:-1].split(sep="/")[-1])


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t\t' * (indent+1) + str(value))


def listConnections():
    connFile = open("connection.json", "r+")
    connData = json.load(connFile)
    print("Available Connections are: ")
    for idx, item in enumerate(connData):
        print(str(idx + 1) + " " + item.get("Name"))
    while True:
        cid = int(input("Select connection [0 to exit]"))
        if cid == 0:
            return
        print(json.dumps(connData[cid - 1], indent=2))


def addConnection():
    connectors = ["PostgreSQL", "MySQL"]
    ConnectionName = input("Enter Connection Name")
    while not ConnectionName:
        ConnectionName = input("Enter Connection Name")
    for cnid, cnctr in connectors:
        print(str(cnid)+" " + cnctr)
    # ConnectorName =
# def entryPointTestManger():
#     print("Available test folders: ")
#     listTestFolders()


def Greeter(i):
    switcher = {
        1: listTestFolders,
        2: listConnections,
        3: addConnection
    }
    func = switcher.get(i, lambda: menu())
    return func()


print("######################################")
print("#### The DB UI TestSuite Explorer ####")
print("######################################")


def menu():
    print("\nSelect the operation\n\
    0. Exit\n\
    1. List the test folders\n\
    2. List the Connections\n\
    3. Add connection")


def entry():
    menu()
    while True:
        choice = int(input("Choice[menu:999]: "))
        if choice == 0:
            break
        if choice == 999:
            menu()
        else:
            Greeter(choice)


entry()
