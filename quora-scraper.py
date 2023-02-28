import random
import requests
import selenium
import time
from alive_progress import alive_bar
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from csv import DictReader
import openai
import airtable as at

openai.api_key = ''  # Insert your openai api key

# Webdriver options
PATH = 'driver/chromedriver'
options = webdriver.ChromeOptions()


# options.add_argument('--incognito')

def get_cookies(file):
    """
    This function read file with cookies and return it to dict
    :param file: file with cookies
    :return: cookies in dict
    """
    with open(file, encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
    return list_of_dicts


# options.add_argument('--headless')
def progress_bar(timer):
    """
    Function generate progress bar
    :param timer: time from 0 to 100
    :return: printing bar
    """
    with alive_bar(100, force_tty=True) as bar:
        for i in range(100):
            time.sleep(timer)
            bar()


def generate_answer(question):
    """
    Generate answer based on openai api
    :param question: scraped question from quora
    :return: answer from openai
    """
    prompt_eng = question

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_eng,  # Tutaj podmiana promptu w zależności od języka
        max_tokens=3000,
        temperature=0.8,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text


def post_answer(answer):
    """
    This function posting answer.
    var links: List of texts with links to our affilate sites.
    param answer: answer from generate_answer function
    :return: None
    """
    links = ['You can learn more about it on -> https://bit.ly/go-to-fiverr-2023',
             'This site helped me when I tried to hire a freelancer: https://bit.ly/go-to-fiverr-2023',
             "I hope I've answered your question.",
             "I've improved my skills with courses here: https://bit.ly/go-to-fiverr-2023"
             "Cheers.", "Peeace.", "I hope this helps."]

    # Textarea in quora answering popup
    textarea = driver.find_element(By.CSS_SELECTOR, '#root > div > div:nth-child(2) > div > div > div > div > '
                                                    'div.q-flex.ModalContainerInternal___StyledFlex-s8es4q-2.gXhqYs'
                                                    '.modal_content_inner.qu-flexDirection--column.qu-bg--white.qu-overflowY'
                                                    '--auto.qu-borderAll.qu-alignSelf--center > div > '
                                                    'div.q-flex.qu-flexDirection--column.qu-overflowY--auto > '
                                                    'div.q-relative.qu-display--flex.qu-flexDirection--column > div > div.q-box '
                                                    '> div:nth-child(2) > div > div > div > div > div.q-box > div > div')

    textarea.send_keys(generate_answer(question=answer))

    progress_bar(0.4)

    # Button post while answering
    driver.find_element(By.CSS_SELECTOR, '#root > div > div:nth-child(2) > div > div > div > div > '
                                         'div.q-flex.ModalContainerInternal___StyledFlex-s8es4q-2.gXhqYs'
                                         '.modal_content_inner.qu-flexDirection--column.qu-bg--white.qu-overflowY'
                                         '--auto.qu-borderAll.qu-alignSelf--center > div > '
                                         'div.q-flex.qu-flexDirection--column.qu-overflowY--auto > '
                                         'div.q-sticky.qu-bg--white.qu-borderTop > div > '
                                         'div.q-flex.qu-justifyContent--flex-end.qu-alignItems--center > button').click()


def login_quora(driver):
    """
    This function login to quora with cookies
    :param driver: webdriver from folder
    :return: None
    """
    quora_login = 'https://pl.quora.com/'
    driver.get(quora_login)
    cookies = get_cookies('quora_cookies.csv')
    for i in cookies:
        driver.add_cookie(i)
    driver.refresh()


def quora_panel():
    """
    This function scrape questions from quora panel.
    """
    for _ in range(60):
        for number in range(1, 4):
            try:
                driver.get('https://quora.com/answer')
                progress_bar(0.05)

                question_text = driver.find_element(By.CSS_SELECTOR,
                                                    f'#mainContent > div > div > div:nth-child(2) > div > div:nth-child(2) > div:nth-child({number}) > div > div > div > div > div > div > div > div.q-box.qu-display--flex > div.q-text.qu-dynamicFontSize--regular_title.qu-fontWeight--bold.qu-color--gray_dark_dim.qu-passColorToLinks.qu-lineHeight--regular.qu-wordBreak--break-word > span > span > a > div > div > div > div > span').text
                driver.find_element(By.XPATH,
                                    f'//*[@id="mainContent"]/div/div/div[2]/div/div[2]/div[{number}]/div/div/div/div/div/div/div/div[3]/div/div/div[1]/button[1]').click()

                progress_bar(0.1)
                post_answer(question_text)
            except selenium.common.exceptions.NoSuchElementException:
                driver.refresh()


def quora_airtable():
    """
    This function connecting script with airtable and get urls selected questions for answering.
    """
    for todo in todo_list:
        todo_status = todo['fields']
        if todo_status['Status'] == 'Todo':
            progress_bar(0.15)
            todo_id = todo['id']
            todo_quora_url = todo_status['Quora URL']

            driver.get(todo_quora_url)
            question = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/div/div[1]/div['
                                                     '1]/div/div[1]/span/span/div/div/div/span/span').text
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/div/div[1]/div[1]/div/div['
                                          '2]/div/div/div[1]/button[1]').click()

            progress_bar(0.05)

            campaing_list = ['You can start earn money here -> https://bit.ly/get-paid-social-media-2023',
                             'When I was young, I earned first money online here -> https://bit.ly/get-paid-social-media-2023',
                             'I hope this helps you https://bit.ly/get-paid-social-media-2023']

            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div['
                                          '1]/div/div[1]/div[2]/div/div/div/div/div[1]/div/div/div').send_keys(
                generate_answer(question=question) + '\n' + f'{random.choice(campaing_list)}')

            progress_bar(0.7)
            answer = driver.find_element(By.CSS_SELECTOR, '#root > div > div:nth-child(2) > div > div > div > div > '
                                                          'div.q-flex.ModalContainerInternal___StyledFlex-s8es4q-2'
                                                          '.gXhqYs.modal_content_inner.qu-flexDirection--column.qu-bg'
                                                          '--white.qu-overflowY--auto.qu-borderAll.qu-alignSelf'
                                                          '--center > div > '
                                                          'div.q-flex.qu-flexDirection--column.qu-overflowY--auto > '
                                                          'div.q-relative.qu-display--flex.qu-flexDirection--column > '
                                                          'div > div.q-box > div:nth-child(2) > div > div > div > div '
                                                          '> div.q-box > div > div:nth-child(3) > div > div').text

            print(answer)

            driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[2]/div['
                                          '2]/div/div[2]/button').click()
            try:
                table.update(todo_id, {'Question': question})
                table.update(todo_id, {'Answer': answer})
                table.update(todo_id, {'Status': 'Done'})
            except requests.exceptions.ConnectionError:
                print('Bląd airtable api')


if __name__ == "__main__":
    table = at.Table(at.api_key, at.base_id, 'Quora')
    todo_list = table.all()
    driver = webdriver.Chrome(PATH, chrome_options=options)
    login_quora(driver)
    option = input('What do you want to do? 1. Questions from panel / 2. Questions from airtable -> ')
    # You can choose automated answering from questions scraped or selected.
    if option == '1':
        quora_panel()
    elif option == '2':
        quora_airtable()
