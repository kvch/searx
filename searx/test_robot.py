from os.path import dirname, join, abspath
from splinter import Browser

import pytest
import os
import subprocess

PYTHON_EXECUTABLES =  ['python2.7', 'python3']

def start_searx(python_exe):
    os.setpgrp()

    webapp = os.path.join(
        os.path.abspath(os.path.dirname(os.path.realpath(__file__))),
        'webapp.py'
    )

    os.environ['SEARX_SETTINGS_PATH'] = abspath(
        dirname(__file__) + '/settings_robot.yml')

    server = subprocess.Popen(
        [python_exe, webapp],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return server


def stop_searx(server):
    os.kill(server.pid, 9)
    del os.environ['SEARX_SETTINGS_PATH']


def get_searx_server_browser(python_executable, url):
    server = start_searx(python_executable)
    browser = Browser()
    browser.visit(url)
    return server, browser


@pytest.fixture(params=PYTHON_EXECUTABLES)
def searx_main(request):
    server, browser = get_searx_server_browser(request.param, 'http://localhost:11111')
    yield browser
    browser.quit()
    stop_searx(server)


@pytest.fixture(params=PYTHON_EXECUTABLES)
def searx_about(request):
    server, browser = get_searx_server_browser(request.param, 'http://localhost:11111/about')
    yield browser
    browser.quit()
    stop_searx(server)


@pytest.fixture(params=PYTHON_EXECUTABLES)
def searx_404(request):
    server, browser = get_searx_server_browser(request.param, 'http://localhost:11111/non-existent-page')
    yield browser
    browser.quit()
    stop_searx(server)


@pytest.fixture(scope='session', params=PYTHON_EXECUTABLES)
def searx_preferences(request):
    server, browser = get_searx_server_browser(request.param, 'http://localhost:11111/preferences')
    yield browser
    browser.quit()
    stop_searx(server)


def test_basic(searx_main):
    assert searx_main.is_text_present('searx_test')
    assert searx_main.is_text_present('about')
    assert searx_main.is_text_present('preferences')
    assert searx_main.is_text_present('a privacy-respecting, hackable metasearch engine')


def test_about(searx_about):
    assert searx_about.is_text_present('Why use searx?')


def test_404(searx_404):
    assert searx_404.is_text_present('Page not found')
    assert searx_404.is_text_present('Go to search page')


def test_preferences_content(searx_preferences):
    assert searx_preferences.is_text_present('Preferences')
    assert searx_preferences.is_text_present('General')
    assert searx_preferences.is_text_present('Engines')
    assert searx_preferences.is_text_present('Plugins')
    assert searx_preferences.is_text_present('Answerers')
    assert searx_preferences.is_text_present('Cookies')
    assert searx_preferences.is_element_present_by_xpath('//input[@value="save"]')
    assert searx_preferences.is_text_present('Reset defaults')


def test_preferences_content(searx_preferences):
    assert searx_preferences.is_element_present_by_xpath('//input[@id="checkbox_general"]')
    assert searx_preferences.is_element_present_by_xpath('//label[@for="checkbox_general"]')
    assert searx_preferences.is_element_present_by_xpath('//input[@id="checkbox_dummy"]')
    assert searx_preferences.is_element_present_by_xpath('//label[@for="checkbox_dummy"]')
    searx_preferences.find_by_xpath('//label[@for="checkbox_dummy"]').first.check()
    searx_preferences.find_by_xpath('//input[@value="save"]').first.click()
#    assert searx_preferences.url == 'http://localhost:11111'
#    assert searx_preferences.cookies['categories'] == 'generaldummy'
