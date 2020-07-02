#!/usr/bin/python3

# /**
# * @author Abhijeet Padwal
# * @email apadwal@tibco.com
# * @create date 2020-07-02 16: 19: 02
# * @modify date 2020-07-02 16: 19: 02
# * @desc[description]
# */

import json
import glob
import time
import sys
import subprocess
import shutil
import os
import platform

buildTag = str(sys.argv[1])  # enter build tag
automationRoot = str(sys.argv[2])
connectors = json.loads(sys.argv[3])
automationHome = automationRoot + "AutomationHome" + buildTag
reportHome = automationHome + '/reports/'
report = reportHome + buildTag
waitTime = 300

connectors = {
    'Zoho-CRM': [
        'flogo-zoho',
        '1.0.1',
        'V11.0.2-GA',
        'wi-zoho-tests:V16'
    ]
}


def killFlogoStudio():
    killfl = "ps aux | grep ./run-studio | awk '{print $2}'"
    procList = os.popen(killfl).read().split('\n')
    for item in procList[:-1]:
        finalKill = 'kill -9 '+item+' > /dev/null 2>&1'
        os.system(finalKill)
        print("\t[INFO] Killing flogo Id is: "+finalKill)


def automationHomeSetup():  # automationHome
    if os.path.isdir(automationHome):
        print("\n\t[INFO] Automation Home is Present #", buildTag)
        os.chdir(automationHome)
        if not os.path.isdir(report):
            os.mkdir(report)
        else:
            shutil.rmtree(report)
            os.mkdir(report)
        print(os.getcwd())
    else:
        print("\n\t[SETUP] Setting Up AutomationHome")
        os.mkdir(automationHome)
        os.chdir(automationHome)
        os.mkdir(reportHome)
        os.mkdir(report)
        print(os.getcwd())


def getTciDeployer(buildTag):
    os.chdir(automationHome)
    if not os.path.isfile('tci-deployer.sh'):
        print("\n\t[SETUP] Fetching TciDeployer")
        print('\n\t[INFO]', os.getcwd())
        getTciDeployerCmd = 'docker run --rm reldocker.tibco.com/tci/tci-deployer:' + \
            buildTag + ' runner > tci-deployer.sh'
        subprocess.call(getTciDeployerCmd, shell=True)
        permissionCmd = "chmod 777 tci-deployer.sh"
        subprocess.call(permissionCmd, shell=True)
    else:
        print('\n\t[INFO] TciDeployer is Present')


def getFlogoEnterprise():
    os.chdir(automationHome)
    if not os.path.isdir('tmp'):
        cmd = './tci-deployer.sh flogo-enterprise gen-runner'
        print('\n\t[SETUP] Fetching FLOGO enterprise')
        subprocess.call(cmd, shell=True)
    else:
        print('\n\t[INFO] FE is present')


def recreateQAsetup():
    os.chdir(automationHome)
    if not os.path.isdir('automation/'):
        connectorGit = goBringThatString(connectors)
        os.mkdir('automation/')
        cmd = './tci-deployer.sh recreateQASetup -ms fe-cli-tools-tests'
        if connectorGit != '':
            cmd += ' -ci '+connectorGit
        print(cmd)
        subprocess.call(cmd, shell=True)
    else:
        print('\n\t[INFO] Automation Framework is already Present')


def moveTmpToFe():
    global waitTime
    os.chdir(automationHome)
    if not os.path.isdir('automation/FE/tmp/'):
        cmd = 'cp -r tmp/ automation/FE/'
        subprocess.call(cmd, shell=True)
        removeTmp = 'rm -rf tmp/'
        os.system(removeTmp)
        waitTime = 500
    else:
        print('\n\t[INFO]Tmp is already present in FE')
        waitTime = 80
        print('\n')
    os.system('ls -ltr automation/FE/')


def startFlogo():  # tested
    os.chdir(automationHome)
    print('\n\t[INFO] Starting FLOGO Studio')
    os.chdir(glob.glob('aut*/FE/tmp/flo*/2.*/bin')[0])
    startflogostudio = 'gnome-terminal -e "./run-studio.sh eula-accept"'
    os.system(startflogostudio)


def goBringThatString(connectors):
    thatString = ''
    for key, value in connectors.items():
        thatString += 'reldocker.tibco.com/wasp/'+value[3]+','
    return thatString[:-1]


print('\n[SETUP] Killing flogo studio')
killFlogoStudio()
automationHomeSetup()
getTciDeployer(buildTag)
getFlogoEnterprise()
recreateQAsetup()
moveTmpToFe()
startFlogo()
print('\n\t[INFO] WaitTime is ', waitTime)
time.sleep(waitTime)
