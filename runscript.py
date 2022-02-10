from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime, json, time, csv


#An annoying workaround to the "Shadow Root" DOM element on Wordle.  This is why all selections are done using the "By" class with CSS_SELECTOR
def get_game_root(driver):
    return driver.find_element(By.CSS_SELECTOR, "game-app").shadow_root


#Closes the popup tutorial on wordle.  Not necessary for functionality, but it looks nicer
def close_modal(driver):
    shadow_host = driver.find_element(By.CSS_SELECTOR, "game-app").shadow_root
    modal_root = shadow_host.find_element(By.CSS_SELECTOR, 'game-modal').shadow_root
    modal_root.find_element(By.CSS_SELECTOR, '.close-icon').click()


#returns true if word is valid, false if invalid
def valid_word(word, row_number, driver):
    actions = ActionChains(driver)  #allows me to input text on site without needing to select a specific element to input to
    actions.send_keys(word)
    actions.send_keys(Keys.RETURN)
    actions.perform()
    actions.send_keys(Keys.BACK_SPACE * 5) #erase the input word (only does something if the word is invalid)
    actions.perform()
    time.sleep(2) #Wait for wordle animation to play
    game_root = get_game_root(driver)
    rows = game_root.find_elements(By.CSS_SELECTOR, "game-row")
    if rows[row_number].get_attribute('letters') == word: #checks the row the word was input on.  If the row still has the word in it's HTML attributes (hasn't been erased by backspacing) then it is valid
        return True
    else:
        return False


def get_words():
    words = []
    with open('five_letter_words.json') as f:
        data = json.load(f)
        for word in data:
            if word[0] == 'u' or word[0] == 'v' or word[0] == 'w' or word[0] == 'x' or word[0] == 'y' or word[0] == 'z':
                words.append(word)
    print("estimated time to complete is " + str(datetime.timedelta(seconds=(len(words)* 2.2))))
    return words


def write_valid_words_to_csv(valid_words):
    with open('valid_words.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerow(valid_words)


def runscript():
    start_time = time.time()
    valid_words = []
    driver = webdriver.Chrome()
    driver.get("https://www.powerlanguage.co.uk/wordle/")
    driver.maximize_window() #fullscreen (just looks nicer)
    close_modal(driver)
    words = get_words()
    row = 0
    for word in words:
        if row > 5: #if wordle rows are full close and re-open the site
            row = 0
            driver.close()
            driver = webdriver.Chrome()
            driver.get("https://www.powerlanguage.co.uk/wordle/")
            driver.maximize_window()
            close_modal(driver)
        if valid_word(word, row, driver):
            print(word + ' is a valid word')
            valid_words.append(word)
            row += 1
        else:
            print(word + " is not a valid word")
    write_valid_words_to_csv(valid_words)
    print("Actual time to complete was " + str(datetime.timedelta(seconds = (time.time() - start_time))))


runscript()