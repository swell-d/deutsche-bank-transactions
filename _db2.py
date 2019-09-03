from selenium import webdriver
import time
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime, timedelta
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def clr(text):
    return re.sub(r'\s+', ' ', str(text)).strip()

if __name__ == '__main__':
    
    login = "test@test.com" # from FIX ME
    passw = "password" #  FIX ME
    to = "test@test.com" #  FIX ME
    smtp_server = "smtp.test.com" #  FIX ME
    smtp_port = 465 #  FIX ME

    try:
        driver = webdriver.Chrome()
        driver.get("https://meine.deutsche-bank.de/trxm/db/")
        time.sleep(1)
        element1 = driver.find_element_by_name("branch")
        element1.send_keys("123") #  FIX ME
        element2 = driver.find_element_by_name("account")
        element2.send_keys("1234567") #  FIX ME
        element3 = driver.find_element_by_name("pin")
        element3.send_keys("12345") #  FIX ME
        element4 = driver.find_element_by_name("loginType")
        element4.click()

        # окно запроса включения двухфакторной авторизации
        i = 0
        while not driver.page_source.find('Nicht aktivieren und'):
            i += 1
            time.sleep(1)
            if i == 10: break
        driver.find_element_by_name('method').click()

        i = 0
        while not driver.page_source.find('Umsatzanzeige'):
            i += 1
            time.sleep(1)
            if i == 10: raise ConnectionError
        element5 = driver.find_element_by_link_text("Umsatzanzeige")
        element5.click()

        day = datetime.strftime(datetime.now() - timedelta(days=1), "%d")
        month = datetime.strftime(datetime.now() - timedelta(days=1), "%m")

        element11 = driver.find_element_by_name("periodStartDay")
        element11.clear()
        element11.send_keys(day)
        element12 = driver.find_element_by_name("periodStartMonth")
        element12.clear()
        element12.send_keys(month)
        element13 = driver.find_element_by_name("periodEndDay")
        element13.clear()
        element13.send_keys(day)
        element14 = driver.find_element_by_name("periodEndMonth")
        element14.clear()
        element14.send_keys(month)
        element15 = driver.find_element_by_xpath('//*[@id="accountTurnoversForm"]/div/span[2]/input')
        element15.click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(login, passw)

            for each in soup.find_all('tr', class_='hasSEPADetails'):
                tds = each.find_all('td')
                # date1 = clr(tds[0].text)
                # date2 = clr(tds[1].text)
                company = clr(tds[2].text).replace('SEPA-Gutschrift von ', '')
                sum = clr(tds[4].text)
                descr = clr(each.find_next_siblings('tr')[0].table)
                if sum:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = f"Einkommen:  {company}  -  {sum} EUR"
                    msg['From'] = login
                    msg['To'] = to
                    msg.attach(MIMEText(f"<h1>{company} - {sum} EUR</h1><br><br>{descr}", 'html'))
                    server.sendmail(login, to, msg.as_string())
    except:
        pass
    try:
        driver.quit()
    except:
        pass
