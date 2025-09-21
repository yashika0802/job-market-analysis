#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from bs4 import BeautifulSoup

def getDataFromURL(url):
    print('Scrapping:', url)
    data = {}
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

    try:
        data['URL'] = url
        #url = "https://www.google.com/search?q=data+scientist+jobs+near+San+Francisco,+CA&sca_esv=9e59dd3bcd3ab1f6&sca_upv=2&biw=1440&bih=779&udm=8&sxsrf=ADLYWII9eoOQg4uS6qdo_x3DEgRt2vbY_A:1727637652643&ei=lKj5Zq6CJ6yf0PEPxcTYoAY&uact=5&oq=data+scientist+jobs&gs_lp=Egxnd3Mtd2l6LXNlcnAiE2RhdGEgc2NpZW50aXN0IGpvYnMyBBAjGCcyBBAjGCcyCxAAGIAEGJECGIoFMgsQABiABBiRAhiKBTILEAAYgAQYkQIYigUyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEiICVD9AVjJBHABeAGQAQCYAVigAaoBqgEBMrgBA8gBAPgBAZgCA6ACuwHCAgoQABiwAxjWBBhHwgIIEAAYgAQYkgPCAg4QABiABBiRAhjJAxiKBZgDAIgGAZAGCJIHATOgB-gP&sclient=gws-wiz-serp&jbr=sep:0&llpgabe=CggvbS8wZDZscA#vhid=vt%3D20/docid%3DwjAqiEXOY5pO7VkJAAAAAA%3D%3D&vssid=jobs-detail-viewer"
        driver.get(url)

        time.sleep(3)
        
        div_viewer_element = driver.find_element(By.XPATH, "//div[@class='A8mJGd NDuZHe']")
        div_viewerinternal_element = div_viewer_element.find_element(By.XPATH, "//div[@class='BIB1wf EIehLd fHE6De Emjfjd']")
        
        div_for_buttons = div_viewerinternal_element.find_elements(By.XPATH, "//div[@class='nNzjpf-cS4Vcb-PvZLI-enNyge-KE6vqe-ma6Yeb nNzjpf-cS4Vcb-PvZLI-gV0Xcb-TzA9Ye nNzjpf-cS4Vcb-PvZLI-qiD3me-vJ7A6b']")
        for index, div in enumerate(div_for_buttons):
            if (div.accessible_name != ''):
                #print(index, div.accessible_name)
                div.click()
                time.sleep(2)
        
        parent_div_html = driver.find_element(By.XPATH, "//div[@class='A8mJGd NDuZHe']").get_attribute('outerHTML')
        soup = BeautifulSoup(parent_div_html, 'html.parser')
        soup_display_card_div = soup.find('div', class_='JmvMcb')
        job_title = soup_display_card_div.find('h1', class_='LZAQDf cS4Vcb-pGL6qe-IRrXtf').get_text()
        #print('BS - job_title:', job_title)
        data['Job title'] = job_title
        
        
        job_subheading = soup_display_card_div.find('div', class_='waQ7qe cS4Vcb-pGL6qe-ysgGef').get_text()
        #print('BS - job_subheading:', job_subheading)
        
        subHeadingList = job_subheading.split(' • ')
        data['Job sub-headings'] = job_subheading
        data['Company'] = subHeadingList[0]
        for i in range(1, len(subHeadingList)):
            text = subHeadingList[i]
            if text.find('via') != -1:
                data['Source'] = text.split('via ')[1]
            else:
                data['Location'] = text
            
        
        soup_additional_job_details_element = soup_display_card_div.find('div', class_='mLdNec')
        additional_details = []
        for element in soup_additional_job_details_element.find_all('span', class_='RcZtZb'):
            text = element.get_text()
            if text != '':
                additional_details.append(text)
                if text.find('an hour') != -1 or text.find('a year') != -1 or text.find('a month') != -1:
                    data['Salary'] = text
                elif text.find('ago') != -1:
                    data['Posted'] = text
                elif text.find('-time') != -1 or text.find('Internship') != -1 or text.find('Contractor') != -1:
                    data['Type'] = text
                elif text.find('Work from home') != -1:
                    data['Work from home'] = text
                elif text.find('No Degree Mentioned') != -1:
                    data['No Degree Mentioned'] = text
                    
        #print('BS - additional_details:', additional_details)
        data['Job additional data'] = additional_details
        

        soup_div_data_element = soup.find('div', class_='NgUYpe')
        
        job_desc = ''
        soup_jd_h3_elemnt = soup_div_data_element.find('h3', class_='FkMLeb cS4Vcb-pGL6qe-IRrXtf')
        soup_jd_span_elements = soup_jd_h3_elemnt.find_next_siblings('span')
        for element in soup_jd_span_elements:
            text_content = element.get_text()
            job_desc += text_content
        #print('BS - job_desc:', job_desc)
        data['Job Description'] = job_desc
        
        #span_job_highlight = div_data_element.find_element(By.XPATH, "//span[@jsname='v5rbLc']")
        soup_job_highlight_span_elemnt = soup_div_data_element.find('span', attrs={'jsname': 'v5rbLc'})
        #h4_job_highlight_elemets = span_job_highlight.find_elements(By.XPATH, 'h4')
        soup_h4_job_highlight_elemets = soup_job_highlight_span_elemnt.find_all('h4')
        job_high = {}
        for element in soup_h4_job_highlight_elemets:
            #next_element = element.find_element(By.XPATH, 'following-sibling::*')
            title = element.get_text()
            soup_next_element = element.find_next_sibling()
            text_content = soup_next_element.get_text()
            job_high[title] = text_content
            data[title] = text_content
        #print('BS - job_high:', job_high)
        
    except:
        print('Error parsing')
         
    finally:
        driver.quit()
        return data
    
    return data

'''output = getDataFromURL('https://www.google.com/search?q=data+analyst+jobs+california&sca_esv=4b1ed64a7070598d&sca_upv=1&udm=8&ei=DSn6ZtmcOOGB0PEPmpXq0Qo&ved=0ahUKEwiZ18Kn6umIAxXhADQIHZqKOqoQ4dUDCA8&uact=5&oq=data+analyst+jobs+california&gs_lp=Egxnd3Mtd2l6LXNlcnAiHGRhdGEgYW5hbHlzdCBqb2JzIGNhbGlmb3JuaWEyCxAAGIAEGJECGIoFMgUQABiABDIFEAAYgAQyBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHkiyF1DFBVjPD3ABeAGQAQCYAV2gAesFqgECMTC4AQPIAQD4AQGYAgugAosGwgIKEAAYsAMY1gQYR5gDAIgGAZAGCJIHAjExoAeQSQ&sclient=gws-wiz-serp&jbr=sep:0#vhid=vt%3D20/docid%3DwP6VzeaFNgfb-eh7AAAAAA%3D%3D&vssid=jobs-detail-viewer')
print(output)'''

def runScrapper():
    job_links_file_path = 'JobLinks.csv'
    job_data_file_path = 'JobData.csv'
    
    job_link_df = pd.read_csv(job_links_file_path)
    old_job_data_df = pd.read_csv(job_data_file_path)
    job_data_list = []
    
    try:
        for index, row in job_link_df.iterrows():
            url = row['URL']
            scrapped = row['Scrapped']
            if scrapped == 0:
                job_data_list.append(getDataFromURL(url))
                job_link_df.at[index, 'Scrapped'] = 1
    finally:
        if len(job_data_list) > 0:
            print('Writing data')
            job_link_df.to_csv(job_links_file_path, index=False)
            new_job_data_df = pd.DataFrame(job_data_list)
            job_data_df = pd.concat([old_job_data_df, new_job_data_df], ignore_index=True)
            job_data_df.to_csv(job_data_file_path, index=False)

runScrapper()