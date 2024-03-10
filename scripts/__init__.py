import time
from log import logger
from selenium import webdriver
from typing import Optional, Union
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, Tag, ResultSet
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
