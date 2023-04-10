from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Launch the browser and navigate to the page
driver = webdriver.Chrome()
driver.get("https://www.flightradar24.com/data/airports/tlv/arrivals")

# Wait for 10 seconds
time.sleep(5)

# Accept cookies
try:
    cookies_accept = driver.find_element(By.CSS_SELECTOR, ".cookie-bar .fr24-cookie-action")
    cookies_accept.click()
    time.sleep(2)
except:
    print("Cookies already accepted or not found")

# Find the "Load earlier flights" button and click it until it disappears from the page
while True:
    load_earlier_button = driver.find_element(By.CSS_SELECTOR, "button.btn-flights-load")
    if 'disabled' in load_earlier_button.get_attribute('class'):
        break
    load_earlier_button.click()
    time.sleep(2)  # Wait for the new data to load

# Find the table element containing the data
try:
    table = driver.find_element(By.CSS_SELECTOR, "table.table-condensed.table-hover.data-table.m-n-t-15")
except:
    print('Error: Table element not found on page.')
    driver.quit()
    exit()

# Extract the data from the table
data = []
for row in table.find_elements(By.TAG_NAME, "tr"):
    cols = [col.text.strip() for col in row.find_elements(By.TAG_NAME, "td")]
    if len(cols) == 7:  # Make sure there are exactly 7 columns of data
        data.append(cols)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data, columns=['Time', 'From', 'Airline', 'Flight', 'Gate', 'Status', 'Details'])

# Print the DataFrame
#df.to_csv('scraped_data.csv', index=False)
print(df)

# Close the browser
driver.quit()