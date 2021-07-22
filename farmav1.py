from random import randint
import string
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from typing import Tuple,List
import random
import time
import os.path
import smtplib
import ssl
import re
import traceback
from selenium.webdriver.common.keys import Keys
import math
import json

# Login and menus paths

world_path = '//*[@id="home"]/div[3]/div[4]/div[10]/div[3]/div[2]/div[1]/a[{}]/span'
login_button_path = '//*[@id="login_form"]/div/div/a'
farmer_menu = '//*[@id="manager_icon_farm"]'
menu_paths = ['//*[@id = "menu_row"]/td[2]/a', '//*[@id="header_menu_link_map"]/a', '//*[@id="menu_row"]/td[4]/a',
             '//*[@id="menu_row"]/td[5]/a', '//*[@id="menu_row"]/td[10]/a', '//*[@id="menu_row"]/td[12]/a', '//*[@id="topdisplay"]/div/a']
overview_path = '//*[@id="menu_row"]/td[2]/a'
village_view_path = '//*[@id="menu_row2_village"]/a'
production_path = '//*[@id="overview_menu"]/tbody/tr/td[2]/a'
stable_tower_path = '//*[@id="map"]/area[13]'
village_name_path = '//*[@id="menu_row2_village"]/a'
stable_class_path = 'visual-label-stable'

# Cords for custom attack
send_light_path = '//*[@id="unit_input_light"]'
place_path = '//*[@id="map"]/area[2]'
attack_button_path = '//*[@id="target_attack"]'
confrim_attack_button_path = '//*[@id="troop_confirm_go"]'
coord_input_path = '//*[@id="place_target"]/input'

# Army paths
piks_path = '//*[@id="spear"]'
swords_path = '//*[@id="sword"]'
axes_path = '//*[@id="axe"]'
light_path = '//*[@id = "light"]'
max_light_path = '/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/form/table/tbody/tr[{}]/td[3]'
piks_pattern_path = '//*[@id="content_value"]/div[2]/div/form[1]/table/tbody/tr[2]/td[1]/input'
swords_pattern_path = '//*[@id="content_value"]/div[2]/div/form[1]/table/tbody/tr[2]/td[2]/input'
axes_pattern_path = '//*[@id="content_value"]/div[2]/div/form[1]/table/tbody/tr[2]/td[3]/input'
light_pattern_path = '//*[@id="content_value"]/div[2]/div/form[2]/table/tbody/tr[2]/td[5]/input'
scout_tech_path = '/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table[3]/tbody/tr[2]/td[2]/div/span/span/span'
# Starts from 1- second page is 1 third 2 etc
farm_page_path = '//*[@id="plunder_list_nav"]/table/tbody/tr/td/a[{}]'
captcha_id = 'recaptcha-anchor-label'

receiver_email = ""

def init_browser() -> webdriver.Chrome:
    '''Create instance of driver
    '''
    opts = ChromeOptions()
    opts.add_experimental_option("detach", True)
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    return browser

def send_mail(msg: str):
    '''Send mail to gmail acc
  
    '''
    password = 'thpobiop12'
    smtp_server = "smtp.gmail.com"
    sender_email = 'arararagisan13@gmail.com'
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    message = 'Subject: {}\n\n'.format(msg)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def switch_page(actions: ActionChains, browser: webdriver.Chrome, page: int) -> ActionChains:
    '''Function to switch page from farming menu to given one

    '''
    element = browser.find_element_by_xpath(
        farm_page_path.format(page))
    actions.move_to_element(element).perform()
    element.click()
    check_capcha(browser)
    return(ActionChains(browser))

def load_patterns(browser: webdriver.Chrome) -> Tuple[List[int], List[int]]:
    '''Function used to load patterns from farming menu
    '''
    a_pattern, b_pattern = [], [0, 0, 0]

    a_pattern.append(int(browser.find_element_by_xpath(
        piks_pattern_path).get_attribute('value')))
    a_pattern.append(int(browser.find_element_by_xpath(
        swords_pattern_path).get_attribute('value')))
    a_pattern.append(int(browser.find_element_by_xpath(
        axes_pattern_path).get_attribute('value')))
    a_pattern.append(0)

    b_pattern.append(int(browser.find_element_by_xpath(
        light_pattern_path).get_attribute('value')))
    return a_pattern, b_pattern

def find_last_element(browser: webdriver.Chrome, path: str) -> int:
    '''Function used to find number of attacks on single page
    '''
    last = 3
    pat = path.format(last)
    try:
        while(True):
            browser.find_element_by_xpath(pat)
            last += 1
            pat = path.format(last)
    except:
        return last - 1

def attack(path: str, browser: webdriver.Chrome):
    '''Perform a single attack
    '''
    r = random.uniform(0.7, 1.1)
    time.sleep(r)
    browser.find_element_by_xpath(path).click()

def check_pattern(pattern: List[int], piks: int, swords: int, axes: int, light: int, n: int) -> bool:
    '''Check if with avaliable army, is it possible to send given number of attacks using given pattern
    '''
    if(pattern[0] * n <= piks):
        if(pattern[1] * n <= swords):
            if(pattern[2] * n <= axes):
                if(pattern[3] * n <= light):
                    return True
    return False

def custom_attack(customCords: List[str], browser: webdriver.Chrome):
    '''Try to send custom attack using given cords
    '''
    browser.find_element_by_xpath(village_view_path).click()
    check_capcha(browser)
    time.sleep(random.uniform(3.0, 4.0))

    browser.find_element_by_xpath(place_path).click()
    check_capcha(browser)

    for i in customCords:
        x = i.split('|')
        #Check village
        if(browser.find_element_by_xpath(village_name_path).text[2] == x[3]):
            #X
            browser.find_element_by_xpath(coord_input_path).send_keys(x[0])
            time.sleep(random.uniform(1.0, 2.0))
            browser.find_element_by_xpath(coord_input_path).send_keys('|')
            time.sleep(random.uniform(1.0, 2.0))
            #Y
            browser.find_element_by_xpath(coord_input_path).send_keys(x[1])
            time.sleep(random.uniform(1.0, 2.0))
            #Number of lk
            browser.find_element_by_xpath(send_light_path).send_keys(int(x[2]))
            time.sleep(random.uniform(3.0, 4.0))
            #Click attack
            browser.find_element_by_xpath(attack_button_path).click()
            WebDriverWait(browser, 6).until(
                EC.presence_of_element_located((By.XPATH, confrim_attack_button_path))).click()
        check_capcha(browser)

def check_capcha(browser: webdriver.Chrome):
    try:
        frame = browser.find_element_by_xpath(
            '//iframe[contains(@src, "recaptcha")]')
        browser.switch_to.frame(frame)
        browser.find_element_by_xpath("//*[@id='recaptcha-anchor']")
        send_mail("Capcha")
        input()
    except:
        return

#Returns list of cords [xxx|yyy|k] k = number of lk, and dict {vilNum:requiredLight}
def read_custom_attack_from_file(fname: str) -> Tuple[List[str],int,int]:
    '''Read custom attacks from file and return list of cords
    '''
    lines = []
    if(os.path.isfile(fname)):
        with open(fname) as f:
            lines = f.read().splitlines()

        #Remove special characters
        lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
        if(len(lines) >= 2):
            n = lines[0]
            required = {}
            for line in lines[1:]:
                light_count = int(line.split('|')[2])
                vil_num = line.split('|')[3]
                try:
                    required[vil_num] = light_count + required[vil_num]
                except:
                    required[vil_num] = light_count
            return lines[1:], int(n), required
        else:
            return [], 0, -1
    else:
        return [], 0, -1

def load_options():
    '''Read options from 'Options.json' file
    '''
    if(os.path.isfile('Options.json')):
        with open('Options.json') as f:
            return json.load(f)
            

def count_max_light(browser: webdriver.Chrome,vil_num: str) -> int:
    '''Count maxium avaliable number of light cavalery
    '''

    try:
        ActionChains(browser).key_down(Keys.NUMPAD7).key_up(Keys.NUMPAD7).perform()
        scout = ''
        try:
            scout = browser.find_element_by_xpath(scout_tech_path).text
        except:
            pass
        result = int((browser.find_element_by_xpath(
            max_light_path.format(3)).text).split('/')[1])
        if(result <= 0 or scout == 'Stajnia (Poziom 1)'):
            result = int((browser.find_element_by_xpath(max_light_path.format(2)).text).split('/')[1])
        browser.find_element_by_xpath(village_name_path).click()
        return result
    except:
        browser.find_element_by_xpath(village_name_path).click()
        return 0


def select_world(browser: webdriver.Chrome,world_number: int) -> str:
    for i in range(10):
        try:
            text = browser.find_element_by_xpath(world_path.format(i)).text
            if text[6:] == world_number:
                browser.find_element_by_xpath(world_path.format(i)).click()
                return
        except:
            text = browser.find_element_by_xpath('//*[@id="home"]/div[3]/div[4]/div[10]/div[3]/div[2]/div[1]/a/span').text
            if text[6:] == str(world_number):
                browser.find_element_by_xpath(
                    '//*[@id="home"]/div[3]/div[4]/div[10]/div[3]/div[2]/div[1]/a/span').click()
                return
            continue

def main():
    browser = init_browser()
    actions = ActionChains(browser)

    browser.get('https://www.plemiona.pl/')

    global receiver_email
    options = load_options()
    receiver_email,custom = options['Email'],options['CustomAttack']
    browser.find_element_by_name("username").send_keys(options['Username'])
    browser.find_element_by_name("password").send_keys(options['Password'])
    browser.find_element_by_xpath(login_button_path).click()
    input("Wciśnij dowolny przycisk aby kontynuować")
    select_world(browser,options['World'])
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, farmer_menu))).click()
    check_capcha(browser)
    #Number of default attacks in one serie
    n = 14

    downTime = input(
        "Podaj gorny zakres ocekiwania miedzy atakami (Domyslnie 30)")
    if downTime:
        downTime = int(downTime)
    else:
        downTime = 30
    upTime = input(
        "Podaj gorny zakres ocekiwania miedzy atakami (Domyslnie 75)\n")
    if upTime:
        upTime = int(upTime)
    else:
        upTime = 75

    if(options['Premium'] == 1):
        villages = '//*[@id="production_table"]/tbody/tr[{}]/td[2]/span/span/a[1]/span'
        B_path = '/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[4]/div/table/tbody/tr[{}]/td[10]/a'
        A_path = '/html/body/table/tbody/tr[2]/td[2]/table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[4]/div/table/tbody/tr[{}]/td[9]/a'
    else:
        villages = '//*[@id="production_table"]/tbody/tr[{}]/td[1]/span/span/a[1]/span'
        A_path = "/html/body/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[4]/div/table/tbody/tr[{}]/td[9]/a"
        B_path = "/html/body/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[4]/div/table/tbody/tr[{}]/td[10]/a"

    startB = 3
    end_a = startB + options['APatternAttacs']
    try:
        A_pattern, B_pattern = load_patterns(browser)
        customCords, k, requriedToCustom = read_custom_attack_from_file(
            'Cords.txt')
        customCounter = k

        if(k == 0):
            custom = False
    except:
        send_mail("Wywrotka")
        return
    avaliablePages = []
    farm = True


    # To count iterations, tells when update max light count
    iteration = 0
    autoPattern = {}

    try:
        while(True):
            # Tells how many pixels to scroll down to get village
            scroll = 10
            for village in range(1, options['NumVillages'] + 1):
                # Select village
                try:
                    if (not options['Premium'] and not village == 1):
                        browser.find_element_by_xpath(overview_path).click()
                        time.sleep(2)
                        browser.find_element_by_xpath(production_path).click()
                        try:
                            WebDriverWait(browser, 3).until(
                                EC.presence_of_element_located((By.XPATH, villages.format(village)))).click()
                        except:
                            element = browser.find_element_by_xpath(
                                villages.format(village))

                            # Scroll a bit to get village avaliable
                            while(True):
                                try:
                                    element.click()
                                    break
                                except:
                                    browser.execute_script("window.scrollBy(0,{})".format(scroll))
                                    scroll += 5
                                    continue
                            scroll = 0
                        time.sleep(1)

                    # Get village number
                    vilNum = int(browser.find_element_by_xpath(
                        village_name_path).text[0]) * 100
                    vilNum = int(browser.find_element_by_xpath(
                        village_name_path).text[1]) * 10 + vilNum
                    vilNum = str(int(browser.find_element_by_xpath(
                        village_name_path).text[2]) + vilNum)
                    if(vilNum in options['NoFarm']):
                        farm = False
                    else:
                        farm = True

                    if(iteration == 0):
                        autoPattern[vilNum] = count_max_light(browser,vilNum)

                    if (farm):
                        WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.XPATH, farmer_menu))).click()
                        # Reset actions to prevent stale element reference error
                        actions = ActionChains(browser)
                        check_capcha(browser)
                        # Move to first element
                        element = browser.find_element_by_xpath(
                            B_path.format(startB))
                        actions.move_to_element(element).perform()

                        # Get number of avaiable soliders
                        piks = int(
                            browser.find_element_by_xpath(piks_path).text)
                        swords = int(
                            browser.find_element_by_xpath(swords_path).text)
                        axes = int(
                            browser.find_element_by_xpath(axes_path).text)
                        light = int(
                            browser.find_element_by_xpath(light_path).text)
                        # Infrom if we already moved to last elemnt
                        last = True

                        try:
                            acceptVillage = requriedToCustom[vilNum] <= light
                        except:
                            acceptVillage = False

                        # Send custom attacks
                        if(acceptVillage and custom == 1 and customCounter % k == 0):
                            custom_attack(customCords, browser)
                            #Go back to farmer menu
                            time.sleep(random.uniform(3.0, 4.0))
                            browser.find_element_by_xpath(farmer_menu).click()
                            check_capcha(browser)
                            time.sleep(random.uniform(2.0, 4.0))
                            actions = ActionChains(browser)

                        # Update light number
                        light = int(
                            browser.find_element_by_xpath(light_path).text)
                        currentN = n
                        # Attacks from pattern
                        if(options['Mode'] == 0):
                            # Pattern is a dictionary {vilNum:attacksNum}
                            for villagePattern in options['Pattern']:
                                if(int(villagePattern) == vilNum):
                                    currentN = options['Pattern'][villagePattern]
                                    break
                        else:
                            for villagePattern in autoPattern:
                                if(villagePattern == vilNum):
                                    currentN = autoPattern[villagePattern] // (
                                        options['Split'] * B_pattern[3])
                                    break

                        # Try send B pattern
                        if(check_pattern(B_pattern, piks, swords, axes, light, currentN-2)):
                            element = browser.find_element_by_id(
                                'farm_pagesize')
                            attacksOnPage = int(element.get_attribute('value'))
                            endSerie = False

                            if(len(avaliablePages) == 0 or len(avaliablePages) < int(currentN/attacksOnPage + 2)):
                                # Create set of unique pages to send attack
                                avaliablePages = [
                                    k for k in range(1, options['Pages'])]
                                # Send more attacks to closer targets
                                for i in range(1, math.ceil(options['Pages']*0.5)):
                                    avaliablePages.append(i)
                                    if(i == 1):
                                        avaliablePages.append(i)
                                        avaliablePages.append(i)
                                random.shuffle(avaliablePages)
                            
                            page = avaliablePages.pop()
                            if(page != 1):
                                page -= 1
                                actions = switch_page(actions, browser, page)

                            endB = find_last_element(browser, B_path)

                            for page in range(1, int(currentN/attacksOnPage + 2)):
                                # Do one page
                                # Try to detect capcha while sendind attacks
                                try:
                                    actions = ActionChains(browser)
                                    for i in range(startB, endB):
                                        # When almost ended move to last element
                                        if(i > 0.65 * endB and last):
                                            element = browser.find_element_by_xpath(
                                                B_path.format(endB))
                                            actions.move_to_element(
                                                element).perform()
                                            last = False
                                        # Every 4 attacks move down to show next 6 fields
                                        elif(i % 4 == 0 and startB+i+6 <= endB and last):
                                            element = browser.find_element_by_xpath(
                                                B_path.format(startB+i+6))
                                            actions.move_to_element(
                                                element).perform()
                                        # Perform single attack
                                        attack(B_path.format(i), browser)
                                        if((i - 2 + (page-1) * attacksOnPage) >= currentN):
                                            endSerie = True
                                            break
                                except:
                                    send_mail("Capcha")
                                    input()

                                if(endSerie):
                                    break

                                page = avaliablePages.pop()

                                actions = switch_page(actions, browser, page)
                                last = True
                                time.sleep(2)

                            # Return to first page
                            actions = ActionChains(browser)
                            vil = browser.find_element_by_xpath(
                                village_name_path)
                            actions.move_to_element(vil).perform()
                            actions = actions = switch_page(actions, browser, 1)
                            time.sleep(1)
                            browser.refresh()
                            check_capcha(browser)
                            actions = ActionChains(browser)

                        last = True
                        # Try send A pattern
                        if(check_pattern(A_pattern, piks, swords, axes, light, end_a - startB)):
                            # GoUp(browser)
                            for i in range(startB, end_a):
                                #When almost ended move to last element
                                if(i > 0.75 * end_a and last):
                                    element = browser.find_element_by_xpath(
                                        A_path.format(end_a))
                                    actions.move_to_element(element).perform()
                                    last = False
                                # Every 4 attacks move down to show next 6 fields
                                elif(i % 3 == 0 and last):
                                    element = browser.find_element_by_xpath(
                                        A_path.format(startB+i+6))
                                    actions.move_to_element(element).perform()
                                #Perform single attack
                                attack(A_path.format(i), browser)
                        check_capcha(browser)
                        # Go back to overview
                        time.sleep(2)
                except:
                    traceback.print_stack()
                    send_mail("Wywalilo sie")
                    input()
                    actions = ActionChains(browser)
                    continue
                if options['Premium']:
                    # In premium we can simply move between villaged using 'd' key
                    action_key_down_d = ActionChains(browser).key_down("d")
                    action_key_down_d.perform()

            if(iteration == 0):
                iteration = 1
            # Jump beetwen random menus
            for i in range(randint(3, 5)):
                # Go to random menuPaths option
                menu_option = randint(0, 6)
                browser.find_element_by_xpath(menu_paths[menu_option]).click()
                check_capcha(browser)
                time.sleep(random.uniform(downTime, upTime))
                # Go back to farming menuPaths
            browser.find_element_by_xpath(farmer_menu).click()
            check_capcha(browser)
            customCounter += 1

            try:
                # Return to the first village
                browser.find_element_by_xpath(overview_path).click()
                time.sleep(2)
                browser.find_element_by_xpath(production_path).click()
                WebDriverWait(browser, 3).until(
                    EC.presence_of_element_located((By.XPATH, villages.format(1)))).click()
            except:
                print("Cannot switch to first village")
                continue

    except:
        traceback.print_exc()
        send_mail("Koniec")


if __name__ == "__main__":
    main()
