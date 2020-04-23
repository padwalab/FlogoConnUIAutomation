from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import string
import random


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def waitForElementToBeVisible(browser, elementTYpe, elementValue, delay=20):
    if elementTYpe == "id":
        try:
            WebDriverWait(browser, delay).until(
                lambda x: x.find_elements_by_id(elementValue))
            return True
        except TimeoutException:
            print("[ERROR] unable to locate element:",
                  elementValue, "[type: ", elementTYpe, "]")
            return False
    elif elementTYpe == "class":
        try:
            WebDriverWait(browser, delay).until(
                lambda x: x.find_elements_by_class_name(elementValue))
            return True
        except TimeoutException:
            print("[ERROR] unable to locate element:",
                  elementValue, "[type: ", elementTYpe, "]")
            return False
