import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

def fetch_job_details(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        company_name = soup.find("div", class_="top-card-layout__entity-info").find('a', class_='topcard__org-name-link topcard__flavor--black-link').get_text(strip=True)
        company_location = soup.find("div", class_="top-card-layout__entity-info").find('span', class_='topcard__flavor topcard__flavor--bullet').get_text(strip=True)
        job_posted_date = soup.find("div", class_="top-card-layout__entity-info").find('span', class_='posted-time-ago__text topcard__flavor--metadata').get_text(strip=True)
        job_role = soup.find("div", class_="top-card-layout__entity-info").find('h1', class_='top-card-layout__title').get_text(strip=True)
        linkedin_profile = soup.find("div", class_="top-card-layout__entity-info").find('a', class_='topcard__org-name-link topcard__flavor--black-link').get('href')

        skills = soup.find("div", class_="description__text description__text--rich").find_all('li')
        skills = [li.text.strip() for li in skills]

        return {
            "company_name": company_name,
            "company_location": company_location,
            "job_posted_date": job_posted_date,
            "job_role": job_role,
            "linkedin_profile": linkedin_profile,
            "skills": skills
        }
    except:
        return None


def job_id():
    target_url='https://www.linkedin.com/jobs/search/?currentJobId=3619426742&geoId=102713980&keywords=data%20analyst&location=India&refresh=true&sortBy=R&position=22&pageNum=0&start={}'
    companies = []  # List to store the job details

    for i in range(0, math.ceil(1/2)):
        res = requests.get(target_url.format(i))
        soup = BeautifulSoup(res.text, 'html.parser')
        alljobs_on_this_page = soup.find_all("li")

        for job_element in alljobs_on_this_page:
            base_card = job_element.find("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

            if base_card is not None:
                jobid = base_card.get('data-entity-urn')
                if jobid is not None:
                    jobid = jobid.split(":")[3]
                    companies.append({"jobid": jobid})

    target_url = 'https://in.linkedin.com/jobs/view/data-analyst-at-cowrks-{}?trk=public_jobs_topcard-title'

    job_detail_urls = [target_url.format(company["jobid"]) for company in companies]
    job_details = []

    with requests.Session() as session:
        for url in job_detail_urls:
            job_detail = fetch_job_details(url)
            if job_detail is not None:
                job_details.append(job_detail)

    df = pd.DataFrame(job_details)
    df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')

    print("done")


job_id()  # Call the main function
