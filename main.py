import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

def job_id():
    target_url='https://www.linkedin.com/jobs/search/?currentJobId=3619426742&geoId=102713980&keywords=data%20analyst&location=India&refresh=true&sortBy=R&position=22&pageNum=0&start={}'
    number_of_loops=math.ceil(1/2)
    
    companies = []  # List to store the job details
    
    for i in range(0, math.ceil(1/10)):
        res = requests.get(target_url.format(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")

        for x in range(0, len(alljobs_on_this_page)):
            base_card = alljobs_on_this_page[x].find("div", {"class": "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card"})

            if base_card is not None:
                jobid = base_card.get('data-entity-urn')
                if jobid is not None:
                    jobid = jobid.split(":")[3]
                    companies.append({"jobid": jobid})

    target_url = 'https://in.linkedin.com/jobs/view/data-analyst-at-cowrks-{}?trk=public_jobs_topcard-title'
    
    for j in range(0, len(companies)):
        resp = requests.get(target_url.format(companies[j]["jobid"]))
        soup1 = BeautifulSoup(resp.text, 'html.parser')
        #print((target_url.format(companies[j]["jobid"])))

        # company_name
        try:
            company_name = soup1.find("div", {"class": "top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})
            company_name = company_name.find('a', class_='topcard__org-name-link topcard__flavor--black-link')
            company_name = company_name.get_text(strip=True)
            companies[j]["company_name"] = company_name
        except:
            companies[j]["company_name"] = None
        
        #company_location
        try:
            company_location = soup1.find("div", {"class": "top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})
            company_location = company_location.find('span', class_='topcard__flavor topcard__flavor--bullet')
            company_location = company_location.get_text(strip=True)
            companies[j]["company_location"] = company_location
        except:
            companies[j]["company_location"] = None
        
        #job_posted_date
        try:
            job_posted_date = soup1.find("div", {"class": "top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})
            job_posted_date = job_posted_date.find('span', class_='posted-time-ago__text topcard__flavor--metadata')
            job_posted_date = job_posted_date.get_text(strip=True)
            companies[j]["job_posted_date"] = job_posted_date
        except:
            companies[j]["job_posted_date"] = None
    
        #job_role
        try:
            job_role = soup1.find("div", {"class": "top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})
            job_role = job_role.find('h1', class_='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title')
            job_role = job_role.get_text(strip=True)
            companies[j]["job_role"] = job_role
            #print(job_role)
        except:
            companies[j]["job_role"] = None
            
        #company linkedin profile
        try:
            linkedin_profile = soup1.find("div", {"class": "top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full"})
            linkedin_profile = linkedin_profile.find('a', class_='topcard__org-name-link topcard__flavor--black-link')
            linkedin_profile = linkedin_profile.get('href')
            companies[j]["linkedin_profile"] = linkedin_profile
            #print(linkedin_profile)
        except:
            companies[j]["linkedin_profile"] = None


        # requirement and skills
        #ul_element = soup1.find("div", {"class": "description__text description__text--rich"}).get_text(strip=True)
        '''above single line code will retrive the requirements in paragaraph'''
        try:
            skills = soup1.find("div", {"class": "description__text description__text--rich"})#.get_text(strip=True)
            skills = skills.find_all('li')
            skills = [li.text for li in skills]
            separated_text = [item.split() for item in skills]
            #print(separated_text)
            companies[j]["skills"] = separated_text
        except:
            companies[j]["skills"] = None
    
    print("done")
    
    df = pd.DataFrame(companies)
    df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')
   
job_id()  # Call the main function 