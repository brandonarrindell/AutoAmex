import csv, time, string
from random import choice
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def GenPasswd2(length=8, chars=string.ascii_letters + string.digits):
  return ''.join([choice(chars) for i in range(length)])


def genRandomText():
  return GenPasswd2(8,string.digits) + GenPasswd2(15,string.ascii_letters)


def collectOfferNames(driver):
  offer_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Add to Card') \
    or contains(text(), 'Save Promo Code')]/../../..")
  tmpnames = [n.text.encode('ascii', 'ignore').decode('utf-8', 'ignore') for n in offer_elements if n.text]
  tmpnames = [n.split('\n')[1] if '\n' in n else n for n in tmpnames]
  offernames = ', '.join(sorted(tmpnames))
  return offernames


def getDriver(browser):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--incognito")
  chrome_options.add_argument("--window-size=1440,900")
  if browser.lower() == 'firefox':
    driver = webdriver.Firefox()
  elif browser.lower() == 'chrome':
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
  elif browser.lower() == 'chrome_linux':
    driver = webdriver.Chrome('./chromedriver_linux64', chrome_options=chrome_options)
  elif browser.lower() in ('phantomjs', 'headless'):
    driver = webdriver.PhantomJS()
  else:
    print("WARNING: browser selection not valid, use PhantomJS as default")
    driver = webdriver.PhantomJS()
  return driver


def loadConfig(filename):
  res = []
  with open(filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader: res.append(row)
  return res


def closeFeedback(driver):
  try:
    driver.find_element(By.CLASS_NAME, "srCloseBtn").click()
  except: pass
  try:
    driver.find_element(By.CLASS_NAME, "fsrCloseBtn").click()
  except: pass
  try:
    driver.find_element(By.CLASS_NAME, "dls-icon-close").click()
  except: pass


def clickOnOffers(driver):
  for t in range(3):
    if not collectOfferNames(driver): return
    for e in driver.find_elements(By.XPATH, '//*[@title="Add to Card"]') + \
            driver.find_elements(By.XPATH, '//*[@title="Save Promo Code"]'):
      try:
        driver.execute_script("arguments[0].click();", e)
      except Exception as e:
        pass
      time.sleep(2)
    if t != 2:
      driver.refresh()
      time.sleep(1)


def amexLogIn(driver, usr, pwd, emailFieldID='lilo_userName', passFieldID='lilo_password'):
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, emailFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, emailFieldID)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, passFieldID)).clear()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, passFieldID)).send_keys(pwd)
  try:
      driver.find_element(By.ID, 'loginSubmit').click()
  except:
      pass
  time.sleep(1)


def amexLogOut(driver):
  while driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]'):
    try: driver.find_element(By.XPATH, '//*[contains(text(), "Log Out")]').click()
    except: pass
    time.sleep(1)


def twitterLogIn(driver, usr, pwd):
  signInLinkID = "signin-link"
  loginBtnClass = "submit"
  emailField = "session[username_or_email]"
  pwdField = "session[password]"
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, signInLinkID)).click()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.NAME,emailField)).send_keys(usr)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.NAME,pwdField)).send_keys(pwd)
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.CLASS_NAME, loginBtnClass)).click()


def twitterLogOut(driver):
  userDropdownID = "user-dropdown-toggle"
  signOutBtn = "js-signout-button"
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.ID, userDropdownID)).click()
  WebDriverWait(driver, 10).until(lambda driver:
    driver.find_element(By.CLASS_NAME, signOutBtn)).click()


def getBalance(driver):
  try:
    e = driver.find_element(By.XPATH, '//*[contains(text(), "Total Balance")]')
    return e.find_element(By.XPATH, '../..').text.split('\n')[1]
  except:
    return "Error"

