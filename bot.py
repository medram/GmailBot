import os
import json
import csv
import shutil
import click


from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


executable_path  	= './bin/geckodriver.exe'
log_path 			= './logs/geckodriver.log' 
profiles_path		= r'C:\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles' % os.getlogin()



def add_emails_to_archive(p):
	profile_path = p['path']

	class MyListeners(AbstractEventListener):
		def before_close(self, driver):
			print('fire before close function.')

		def before_quit(self, driver):
			print('fire before quit function.')
			# with open('cookies/test.cks', 'w') as f:
			# 	json.dump(driver.get_cookies(), f, indent=2)
			# shutil.rmtree(profile_path, ignore_errors=True)
			# shutil.copytree(driver.firefox_profile.path, profile_path)


	fp = webdriver.FirefoxProfile(profile_path)
	driver = webdriver.Firefox(
		fp,
		executable_path=executable_path, 
		service_log_path=log_path
		# log_path = log_path
		)

	# adding events to the driver :D
	# edriver = EventFiringWebDriver(driver, MyListeners())

	driver.implicitly_wait(2)
	driver.get('https://mail.google.com/mail/u/0/#inbox')
	# print(driver.title)

	driver.implicitly_wait(10)

	if not driver.current_url.startswith('https://mail.google.com'):
		click.secho('\r[warning] {email} (May need a manual login).'.format(**p)+' '*50, fg='yellow')
	else:
		check_all = driver.find_element_by_css_selector('span.T-Jo')
		
		driver.implicitly_wait(5)
		# check_all_emails.send_keys(Keys.RETURN)
		# ActionChains(driver).send_keys(Keys.ENTER)
		ActionChains(driver).click(check_all).perform()
		# div.ya > span[role=link]
		driver.implicitly_wait(5)
		try:
			check_all_emails = driver.find_element_by_css_selector('div.ya > span[role=link]')
		except NoSuchElementException:
			# delete emails less than max per page
			ActionChains(driver).send_keys('e').perform()
		else:
			# delete all emails on primary section.
			ActionChains(driver).click(check_all_emails).pause(1).send_keys('e').send_keys(Keys.ENTER).perform()


		try:
			wait = WebDriverWait(driver, 30)
			element = (By.CSS_SELECTOR, 'div.vh > span.aT')
			wait.until(EC.presence_of_element_located(element))
			wait.until_not(EC.presence_of_element_located(element))
		except Exception as e:
			pass
			# print(e)
		finally:
			# edriver.quit()
			driver.quit()



if __name__ == '__main__':
	"""
	get all profiles
	loop through them and fire "add_emails_to_archive" function
	
	"""
	with open('profiles.csv') as f:
		profiles = csv.DictReader(f)
		# remove the default profile.
		all_profiles = [os.path.join(profiles_path, d) for d in os.listdir(profiles_path) if os.path.isdir(os.path.join(profiles_path, d)) and 'default' not in d]

		# get the profiles paths depends on profiles.csv
		valid_profiles = []
		for profile in profiles:
			username = profile['email'].split('@')[0]
			for p in all_profiles:
				if p.endswith(username):
					profile['path'] = p
					valid_profiles.append(profile)

		
		# the the task with whese profiles.
		for profile in valid_profiles:
			try:
				click.secho('[Processing] {email}...'.format(**profile), fg='bright_cyan', nl=False)
				add_emails_to_archive(profile)
			except Exception as e:
				print(e)
			else:
				click.secho('\r[Done] {email}'.format(**profile)+' '*50, fg='bright_green')

		click.secho('Finished.', fg='bright_magenta')




























# driver.get("https://login.yahoo.com/?.src=ym&.lang=en-BE&.intl=be&.done=https%3A%2F%2Fmail.yahoo.com%2Fd")
# driver.maximize_window()
# assert "Python" in driver.title
# email = driver.find_element_by_id("login-username")
# email.clear()
# email.send_keys("eleonoreguernon13@yahoo.com")
# email.send_keys(Keys.RETURN)

# # switch to password window.
# driver.implicitly_wait(2)
# print(driver.window_handles)
# pass_window = driver.window_handles.pop()
# driver.switch_to.window(pass_window)
# print(pass_window)

# password = driver.find_element_by_id('login-passwd')
# password.clear()
# password.send_keys('HJxUXq5S')
# password.send_keys(Keys.ENTER)

# switch to inbox window.
# driver.switch_to.frame(0)


	# archive = driver.find_element_by_css_selector('div.G-Ni.G-aE div.T-I')
	# driver.execute_script("""
	# 	function shortcut({chr, ctrlKey = false, altKey = false}) {
	# 	    var lowerChr = chr.toLowerCase();
	# 	    var upperChr = chr.toUpperCase();
	# 	    var keydownCode = upperChr.charCodeAt(0);
	# 	    var e = new KeyboardEvent("keydown", {
	# 	        key: lowerChr,
	# 	        code: "Key" + upperChr,
	# 	        ctrlKey,
	# 	        altKey,
	# 	        keyCode: keydownCode,
	# 	        which: keydownCode
	# 	    });
	# 	    var keypressCode = lowerChr.charCodeAt(0);
		    
	# 	    document.documentElement.dispatchEvent(e);
	# 	    var e = new KeyboardEvent("keypress", {
	# 	        key: lowerChr,
	# 	        ctrlKey,
	# 	        altKey,
	# 	        charCode: keypressCode,
	# 	        keyCode: keypressCode,
	# 	        which: keypressCode
	# 	    });
	# 	    document.documentElement.dispatchEvent(e);

	# 	    var e = new KeyboardEvent("keyup", {
	# 	        key: lowerChr,
	# 	        ctrlKey,
	# 	        altKey,
	# 	        charCode: keypressCode,
	# 	        keyCode: keypressCode,
	# 	        which: keypressCode
	# 	    });
	# 	    document.documentElement.dispatchEvent(e);
	# 	}

	# 	let check_all = document.querySelector('span.T-Jo')
	# 	//let archive = document.querySelector('div.G-Ni.G-aE div.T-I')

	# 	console.log('Select all emails.')
	# 	check_all.click()

	# 	setTimeout(function(){
	# 		console.log('Add emails to Archive.')
	# 		//archive.click()
	# 		shortcut({chr:'e'})
	# 	}, 2000)
	# """)



# # action = ActionChains(driver)
# # action.move_to_element(spam_link)
# # action.click(spam_link)
# # action.perform()

# # emails = driver.find_elements(By.CLASS_NAME, 'c27KHO0_n')

# # print(driver.window_handles)
# # spam messages.
# messages = driver.find_elements_by_css_selector('button[data-test-id=icon-btn-checkbox]')

# # for message in messages:
# # 	if random.random() <= 0.5:
# # 		message.send_keys(Keys.RETURN)
# # 		# message.click()
# driver.implicitly_wait(2)
# # print(messages)
# # https://readthedocs.org/projects/selenium-python/downloads/pdf/latest/
# # https://www.programcreek.com/python/example/100026/selenium.webdriver.FirefoxProfile

# driver.execute_script("""
# 	console.log(arguments[0]);
# 	arguments[0].map(b => {
# 			if (Math.random() < 0.5)
# 				b.click();
# 		});

# 		setTimeout(() => {
# 			document.querySelector("button[data-test-id=toolbar-not-spam]").click();
# 		}, 2000)
# """, messages)

# try:
# 	WebDriverWait(driver, 6).until(EC.presence_of_element_located(driver.find_elements_by_css_selector("div[role=status] div#notifications")))
# except (NoAlertPresentException, TimeoutException) as py_ex:
# 	pass

# driver.implicitly_wait(2)
# driver.get("https://mail.yahoo.com/d/folders/1")
# driver.implicitly_wait(10)


# # Mark as read in messages inbox.
# messages = driver.find_elements_by_css_selector('button[data-test-id=icon-btn-checkbox]')

# driver.execute_script("""
# 	arguments[0].map(b => {
# 			if (Math.random() < 0.5)
# 				b.click();
# 		});

# """, messages)
# ActionChains(driver).key_down(Keys.SHIFT).send_keys('K').key_up(Keys.SHIFT).perform()
# driver.implicitly_wait(20)


# # adding stars to the inbox messages.
# messages = driver.find_elements_by_css_selector('button[data-test-id=icon-btn-checkbox]')
# driver.execute_script("""
# 	console.log('ADDING STARS...')
# 	document.querySelector("button[data-test-id=checkbox]").click();
# 	arguments[0].map(b => {
# 			if (Math.random() < 0.2)
# 				b.click();
# 		});
# """, messages)
# ActionChains(driver).send_keys('l').perform()


# shutil.copytree(fp.path, './profiles')

# fp.update_preferences()

# driver.close()
