from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from playsound import playsound
import time

myPlanURL = "https://myplan.uw.edu/plan/#/sp22"
email = ""
password = ""
delay = 3

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", options=options)

def login(email, password, myPlanURL):
  while True:
    print("Attempting to login...")
    driver.get(myPlanURL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-netid"]')))
    driver.find_element(By.XPATH, '//*[@id="login-netid"]').click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="weblogin_netid"]')))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="weblogin_password"]')))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit_button"]')))
    driver.find_element(By.XPATH, '//*[@id="weblogin_netid"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="weblogin_password"]').send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/form/ul[2]/li/input").click()
    try:
      WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="react_app"]/div[2]/header/div/div[1]/a')))
      print("Login successful!\n")
      break
    except:
      print("Login unsuccessful, trying again...")
      time.sleep(delay)

def checkForOpenSeats(myPlanURL):
  print("Checking seat availability...")
  driver.execute_script("location.reload(true);")
  try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div[2]/div/div/div[2]/main/div[2]/div/div[1]/div[2]/div[2]/ul/li/ul/li/div[1]/div[2]/div[2]/span[2]/span[1]')))
    seatsAvailable = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/main/div[2]/div/div[1]/div[2]/div[2]/ul/li/ul/li/div[1]/div[2]/div[2]/span[2]/span[1]').text
    if (int(seatsAvailable) > 0):
      print(seatsAvailable + " seat(s) available!\n")
      return True
    else:
      print("No seats available.")
      return False
  except:
    ("An error occured, try again.")
    return False

def register(myPlanURL):
  print("Attempting to register...")
  driver.get(myPlanURL)
  try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[2]/a')))
    driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[2]/a').click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="doneDiv"]/table[3]/tbody/tr/td[1]/h1')))
    time.sleep(delay)
    errorMessage = driver.find_elements(By.XPATH, "//*[contains(text(), 'Schedule not updated')]")
    if len(errorMessage) < 1:
      print("\nRegistration successful!")
      return True
    else:
      print("Registration failed. Trying again in " + str(delay) + " seconds.")
      return False
  except:
    print("Registration failed. Trying again in " + str(delay) + " seconds.")
    return False

time.sleep(3)
print("\n----------------------\nUW REGISTRATION BOT v1\n----------------------")
login(email, password, myPlanURL)
while True:
  time.sleep(delay)
  driver.get(myPlanURL)
  if checkForOpenSeats(myPlanURL):
    playsound('alert.mp3')
    if register(myPlanURL):
      break
