__author__ = 'bankar'



from selenium import webdriver
import os
# import zipfile
import shutil
import time
import logging
import datetime
import sys

from lxml import etree as ET
locallib = os.environ.get('QA_USE_PYTHON_LIB')
if locallib is not None:
    sys.path.append(locallib)
else:
    sys.path.append('c:\\vapp_automation')

print(sys.path)
from selenium.webdriver.remote.remote_connection import LOGGER

from selenium.common.exceptions import *
from utilities.custom_logger import customLogger
LOGGER.setLevel(logging.WARNING)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

locallib = os.environ.get('QA_USE_LOCAL_LIB')

URL = 'https://10.228.200.65:5480/vappmgr/#/login'



def browser_setup(context,timeout=30,**kwargs):
    context.logger.info("path is :{}".format(sys.path))
    if 'BROWSER' in context.config.userdata.keys():
        if context.config.userdata['BROWSER'] is None:
            BROWSER = 'chrome'
        else:
            BROWSER = context.config.userdata['BROWSER']
    else:
        BROWSER = 'chrome'

    context.logger.info("browser is {}".format(BROWSER))
    print('browser is {}'.format(BROWSER))
    if BROWSER == 'chrome':
        chromedriver = 'C:\learn\drivers\chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver

        context.browser = webdriver.Chrome(chromedriver)
    elif BROWSER == 'firefox':
        context.browser = webdriver.Firefox()

    elif BROWSER == 'ie':
        iedriver = 'C:\learn\drivers\IEDriverServer'
        os.environ['webdriver.ie.driver'] = iedriver

        context.browser = webdriver.Ie(iedriver)

    else:
        context.logger.error("Browser {} is not supported")
        sys.exit(1)

    context.browser.maximize_window()
    try:
        context.url = context.config.userdata['URL']
        context.logger.info('user specified URL is used.')
    except KeyError:
        context.logger.info('URL is not provided by the user.Default url being used')
        context.url = URL
    context.logger.info('URL being used.({})'.format(context.url))
    # yield context.browser
    # context.browser.quit()
    try:
        context.browser.get(context.url)
        context.markvalid=True
    except WebDriverException as e:
        context.logger.error('Invalid Url {}'.format(e.message))
        context.logger.error('message:',exc_info=True)
        context.markvalid = False
        context.browser.quit()

def before_all(context):

     results_path = os.path.join(os.getcwd(), "results")

     if not os.path.exists(results_path):
         os.makedirs(results_path)

     context.logger = customLogger(logging.DEBUG)



def before_feature(context, feature):

    if 'BROWSER' in context.config.userdata.keys():
        if context.config.userdata['BROWSER'] is None:
            BROWSER = 'chrome'
        else:
            BROWSER = context.config.userdata['BROWSER']
    else:
        BROWSER = 'chrome'

    context.logger.info("browser is {}".format(BROWSER))
    print('browser is {}'.format(BROWSER))
    if BROWSER == 'chrome':
        chromedriver = 'C:\learn\drivers\chromedriver'
        os.environ["webdriver.chrome.driver"] = chromedriver

        context.browser = webdriver.Chrome(chromedriver)
    elif BROWSER == 'firefox':
        context.browser = webdriver.Firefox()

    elif BROWSER == 'ie':
        iedriver = 'C:\learn\drivers\IEDriverServer'
        os.environ['webdriver.ie.driver'] = iedriver

        context.browser = webdriver.Ie(iedriver)

    else:
        context.logger.error("Browser {} is not supported")
        sys.exit(1)

    context.browser.maximize_window()
    try:
        context.url = context.config.userdata['URL']
        context.logger.info('user specified URL is used.')
    except KeyError:
        context.logger.info('URL is not provided by the user.Default url being used')
        context.url = URL
    context.logger.info('URL being used.({})'.format(context.url))



# Scenario level objects are popped off context when scenario exit

def before_scenario(context, scenario):
    context.logger.info("************************************")
    context.logger.info("Starting Scenario: '{}'".format(scenario.name))


    try:
        context.browser.get(context.url)
        context.markvalid=True
    except WebDriverException as e:
        context.logger.error('Invalid Url {}'.format(e.message))
        context.logger.error('message:',exc_info=True)
        context.markvalid = False
        context.browser.quit()

    if context.markvalid is False:
         scenario.mark_skipped()



def before_step(context,step):
    context.logger.info("Starting Step:'{}'".format(step.name))

def after_step(context,step):
    context.logger.info("Ending Step:'{}'*****".format(step.name))
    context.logger.info('Step status:{}'.format(step.status))
    fmt = datetime.datetime.now().strftime("%y%m%d")
    fileName = step.name+ "_" + fmt + ".png"
    screenshot_directory = '../screenshots/'+fmt +"/"
    relativeFileName = screenshot_directory + fileName
    currentDirectory = os.path.dirname(__file__)
    destinationFile = os.path.join(currentDirectory, relativeFileName)
    destinationDirectory = os.path.join(currentDirectory, screenshot_directory)
    try:
        context.logger.info('{},{},{},{}'.format(relativeFileName,currentDirectory,destinationFile,destinationDirectory))
        if not os.path.exists(destinationDirectory):
            os.makedirs(destinationDirectory)

        if step.status not in ('Passed', 'passed'):
            context.browser.save_screenshot(destinationFile)
            context.logger.info('screenshot saved to dir {}'.format(destinationDirectory))
    except Exception as e:
        context.logger.error('error in creating screenshot {}'.format(e.__str__()))



def after_scenario(context, scenario):
    context.logger.info("Scenario status:'{}'*****".format(scenario.status))
    #context.browser.close()
    # context.browser.quit()


def after_feature(context, feature):
    print("\nAfter Feature.Generating XML file of the result")
    context.logger.info("feature status:{}".format(feature.status))
    loc = os.environ.get('PATH_VAPP_SCRIPT')
    fmt = datetime.datetime.now().strftime("%y%m%d")
    if loc is None:
        results_path = os.path.join(os.getcwd(),"results",fmt)
    else:
        results_path=os.path.join(loc,'results',fmt)

    if not os.path.exists(results_path):
        os.makedirs(results_path)

    'if -o <> is provided. results would be captured in given filename'
    if context.config.outfiles is None:
        results_file = os.path.join(results_path,os.path.basename(feature.filename)+".xml")
    else:
        results_file = os.path.join(results_path,os.path.splitext(os.path.basename(context.config.outfiles[0]))[0]+ ".xml")


    top = ET.Element('testcase', name=feature.name,result=feature.status)
    tp={}
    for tps in feature.scenarios:
        tp['name'] = tps.name
        tp['result'] = tps.status
        testpoint = ET.SubElement(top,'test_point',tp)
        error_message=""
        if tps.status == 'skipped':
            error_message="NOT RUN"
        for step in tps.steps:
            step_status = step.status
            testpoint_steps = ET.SubElement(testpoint, 'steps',name=step.name,result=step_status)
            if step.text is not None:
                ET.SubElement(testpoint_steps,'description').text=step.text
            if step.table is not None:
                headings = ",".join(step.table.headings)
                ET.SubElement(testpoint_steps, 'description').text = headings
                for rows in step.table.rows:

                    ET.SubElement(testpoint_steps, 'description').text = ",".join(rows.cells)
            if step.error_message:
                error_message = error_message + step.error_message

        if error_message is not None:
            ET.SubElement(testpoint, 'error_message').text = error_message
    xml_content = ET.tostring(top,pretty_print=True,xml_declaration=True,encoding='UTF-8')
    print(xml_content)
    context.logger.info("xml file is {}".format(xml_content))
    with open(results_file,"w") as f:
        f.write(ET.tostring(top,pretty_print=True,xml_declaration=True,encoding='UTF-8'))

    context.browser.quit()


def after_all(context):

    # behave -D ARCHIVE=Yes
    if 'ARCHIVE' in context.config.userdata.keys():
        if os.path.exists("failed_scenarios_screenshots"):
            os.rmdir("failed_scenarios_screenshots")
            os.makedirs("failed_scenarios_screenshots")
        if context.config.userdata['ARCHIVE'] == "Yes":
            shutil.make_archive(
    time.strftime("%d_%m_%Y"),
    'zip',
     "failed_scenarios_screenshots")
            #os.rmdir("failed_scenarios_screenshots")
            print("Executing after all")

    # if context.browser:
    for handlers in context.logger.handlers:
        handlers.close()
        context.logger.removeHandler(handlers)
    # context.browser.quit()

