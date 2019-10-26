# -*- coding: utf-8 -*-
# Scrap avito by flat
import requests
from bs4 import BeautifulSoup
import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_html(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
          }
    r = requests.get(url, headers = headers)
    #print(r.text.encode('utf-8'))
    return r.text

def send_email_account(body):
    remote_server = "smtp.yandex.ru"
    remote_port = 587
    username = "username"
    password = "password"
    email_from = "email_from"
    email_to = "email_to"
    subject = "Квартиры AVITO"
    # connect to remote mail server and forward message on
    server = smtplib.SMTP(remote_server, remote_port)
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp_sendmail_return = ""
    try:
        server.starttls()
        server.login(username, password)
        smtp_sendmail_return = server.sendmail(email_from, email_to, msg.as_string())
    except Exception:
        print('SMTP Exception:\n' + str( e) + '\n' + str( smtp_sendmail_return))
    finally:
        server.quit()            

def get_data(html):
    #body = ''
    txt = ''
    soup = BeautifulSoup(html, 'lxml')
    flats = soup.find('div', class_="catalog-list").find_all('div', class_='item_table')
    
    for one_flat in flats:
        
        try:
            title = one_flat.find('h3', class_='title item-description-title').find('a').get('title')
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + one_flat.find('h3', class_='title item-description-title').find('a').get('href')
        except:
            url = ''
        try:
            price = one_flat.find('span', class_="price").text.strip()
        except:
            price = ''
        try:
            address = one_flat.find('p', class_="address").text.strip()
        except:
            address = ''    
        try:
            date_absolute = one_flat.find('div', class_="item-date").find('div').get('data-absolute-date').strip()
            date_marker = one_flat.find('div', class_="item-date").find('div').get('data-relative-date').split()[1]
        except:
            date_item = ''
        '''    
        print(url)
        print(title)
        print(price)
        print(address)            
        print(date_absolute)
        print(date_marker)
        print()
        '''    
        
        if ('час' in date_marker) or ('часа' in date_marker) or ('часов' in date_marker) or ('день' in date_marker):# or ('дня' in date_marker) or ('дней' in date_marker):
            result = ({'price   ': price,
                    'title   ': title,
                    'address ': address,
                    'url     ': url,
                    'date    ': date_absolute
                    }      )
            txt += '\n'.join([f'{key}: {value}' for key, value in result.items()]) + ('\n'+'-------------------------------'+'\n')
            #list_txt = []
            #list_txt.append(txt)
            #list_txt.append('\n'+'-------------------------------'+'\n')
            #body += ''.join(list_txt)      
    send_email_account(txt)

def main():
    url = 'https://www.avito.ru/nizhniy_novgorod/kvartiry/prodam/3-komnatnye/ne_posledniy?pmax=6000000&pmin=3100000&q=%D1%83%D1%81%D0%B8%D0%BB%D0%BE%D0%B2%D0%B0&f=59_13990b13994.497_5187b&s=104'
    get_data(get_html(url))

if __name__ == '__main__':
    main()
