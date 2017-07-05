import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

username = input("username: ")
password = input("password: ")
keyword = input("Job Keyword: ")
page_limit = int(input("Page Limit: "))
#username = ".."
#password = ".."
url = "https://www.upwork.com/ab/account-security/login" 

driver = webdriver.Firefox()
driver.get(url)

driver.find_element_by_name("login[username]").send_keys(username)
driver.find_element_by_name("login[password]").send_keys(password)
driver.find_element_by_class_name("m-sm-bottom.m-lg-top.btn.btn-block.btn-primary.p-lg-left-right").click()
time.sleep(15)
page = 1
i = 0
current_datetime = datetime.datetime.now()
with open("jobs.txt", "a") as textfile:
    datetime_entry = "{current_datetime}\n\n\n".format(
        current_datetime=current_datetime
        )
    textfile.write(datetime_entry)

while page <= page_limit:
    new_url = "https://www.upwork.com/o/jobs/browse/?"+"page="+str(page)+"&q="+keyword 
    #new_url = "https://www.upwork.com/o/jobs/browse/?"+"page="+str(page)+"&q=python" 
    driver.get(new_url)
    time.sleep(10)
    #driver.find_element_by_class_name("eo-truncate-toggle-text.eo-truncate-toggle-text-open").click()
    html = driver.execute_script("return document.documentElement.outerHTML")
    upwork_soup = BeautifulSoup(html, 'html.parser')
    total_jobs = upwork_soup.findAll('strong', {'class':'jobs-found'})[0].text
    website = upwork_soup.findAll('section', {'class':'job-tile air-card-hover hover'})
    with open("jobs.txt", "a") as textfile:
        total_jobs_entry = "From Page Number: {page}\n\nTotal Jobs Found: {total_jobs}\n\n\n".format(
            total_jobs=total_jobs,
            page = page 
            )
        textfile.write(total_jobs_entry)
        for data in website:
            i += 1      
            job_title = data.findAll('h2', {'class':'job-title m-0-top m-sm-bottom'})[0].text.strip(" \n\t\r").encode('utf-8')
            job_type = data.findAll('strong', {'class':'js-type'})[0].text.strip(" \n\t\r")
            job_level = data.findAll('span', {'class':'js-contractor-tier'})[0].text.strip(" - \n\t\r")
            try:
                job_budget = data.findAll('span', {'data-itemprop':'baseSalary'})[0].text.strip(" -  \n\t\r")
            except:
                job_budget = "No Data"
            try:
                job_estimated_time = data.findAll('span', {'class':'js-duration'})[0].text.strip("Est. Time -  : \n\t\r ")
            except:
                job_estimated_time = "No Data"
            job_posted_time = data.findAll('time', {'data-itemprop':'datePosted'})[0].text.strip(" -  \n\t\r")
            job_proposals = data.findAll('small', {'class':'display-inline-block m-sm-top m-md-right'})[0].text
            try:
                job_country = data.findAll('strong', {'class':'text-muted client-location'})[0].text
            except:
                job_country = "No Data"
            link = data.findAll('a', {'class':'job-title-link break visited'})
            for job_link in link:
                if job_link.has_attr('href'):
                    half_link = job_link['href']
                    job_page_link = "https://upwork.com" + half_link
                    driver.get(job_page_link)
                    time.sleep(10)
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    job_page_soup = BeautifulSoup(html, 'html.parser')
                    job_detail = job_page_soup.findAll('p', {'class':'break'})[0].text
                    try:
                        job_skill = job_page_soup.findAll('a', {'class':'o-tag-skill m-0-left m-0-top m-md-bottom'})[0].text
                    except:
                        job_skill = "No Data"
                    job_div = job_page_soup.findAll('div', {'id':'form'})[0].text
            page_line="Serial Number: {sno}\nJob Title: {job_title}\nJob Page Link: {job_page_link}\nType: {job_type}\nLevel: {job_level}\nBudget: {job_budget}\nEstimated Time: {job_estimated_time}\nPosted: {job_posted_time}\nSkill: {job_skill}\n{job_div}{proposals}\nLocation: {location}\nDetail: {job_detail}\n\n\n".format(
                sno = i,
                job_title=job_title,
                job_type=job_type,
                job_level=job_level,
                job_budget=job_budget,
                job_estimated_time=job_estimated_time,
                job_posted_time=job_posted_time,
                job_page_link = job_page_link,
                job_detail = job_detail,
                job_skill = job_skill,
                job_div = job_div,
                proposals = job_proposals,
                location = job_country
                )
            textfile.write(page_line)
    page += 1


#google_r = requests.get(url)
#google_soup = BeautifulSoup(google_r.text, 'html.parser')

