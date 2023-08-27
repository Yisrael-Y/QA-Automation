from appium import webdriver

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'Your_Device_Name',
    'appPackage': 'com.your.app.package',
    'appActivity': 'com.your.app.MainActivity',
    # Other desired capabilities...
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# Locate and click the 'Approve' button
approve_button = driver.find_element_by_id('com.your.app:id/approve_button')
approve_button.click()

# Close the driver after use
driver.quit()
