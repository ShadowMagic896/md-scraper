import logging

firefox_binary_location: str = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
# The location of your "firefox.exe" file. This is what gets launched when you run Firefox normally.
# The default value, "C:\\Program Files\\Mozilla Firefox\\firefox.exe", is the default location for Firefox on Windows.

geckodriver_location: str = "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe"
# The location of your "geckodriver.exe" file. This is what gets launched when you run Firefox normally.
# The default value, "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe", is the default location for Firefox on Windows.

bypass_confim_dialogs: bool = True
# If True, the script will automatically click skip any pause dialogs that appear from this program.
# Such as: Before attempting error fixing and after entering user info

headless: bool = True
# If True, the script will run Firefox in headless mode. This means that the browser will not be visible.
# This is useful if you want to run the script on a server or in the background.

logging_level: int = logging.DEBUG
# The logging level. This is how much information will be printed to the console.
# From most verbose to least: logging.DEBUG [default], logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
