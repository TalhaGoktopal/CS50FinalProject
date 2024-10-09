import requests
from bs4 import BeautifulSoup

jobDicts = []
def scrape():
    #Scrapes UCAS website
    url = "https://www.ucas.com/explore/search/apprenticeships?query=&refinementList%5BLevel.Nation%5D%5B0%5D=England&refinementList%5BLevel.ApprenticeshipType%5D%5B0%5D=Degree%20Apprenticeship&refinementList%5BIndustry%5D%5B0%5D=Information%20and%20communication%20technology&refinementList%5BVacancyType%5D%5B0%5D=Apprenticeship"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = (soup.find("div", class_ = "content-grid")).find_all("article", class_ = "v5-card elevation-low link-container")
    for job in job_list:
        title = (job.find("a", class_ = "link-container__link")).text
        
        link = (job.find("a")).get("href")
        
        salaryTag = job.find(lambda tag: tag.name == "dt" and "Salary" in tag.text)
        salary = (salaryTag.parent).find("dd").text[:6]

        deadlineTag = job.find(lambda tag: tag.name == "dt" and "Apply by | Start date" in tag.text)
        deadline = (deadlineTag.parent).find("dd").text[:10]  

        company = (job.find("p", class_ = "apprenticeship-display__employer")).text

        location = (job.find("p", class_ = "apprenticeship-display__location icon icon--info-location")).text
        
        jobDicts.append({"title": title , "salary": salary , "link": link, "deadline": deadline, "company": company, "location": location})
    
    #Scrapes GOV website
    url = "https://www.findapprenticeship.service.gov.uk/apprenticeships?routeIds=7&sort=DistanceAsc&levelIds=6"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.find_all("li", class_ = "das-search-results__list-item govuk-!-padding-top-6")
    for job in job_list:
        title = (job.find("a", class_ = "das-search-results__link")).text
        
        link = url + (job.find("a", class_ = "das-search-results__link")).get("href")
        
        salaryTag = job.find(lambda tag: tag.name == "dt" and "Salary" in tag.text)
        salary = salaryTag.find("p", class_ = "govuk-body").text[:6]
        
        deadlineTag = job.find(lambda tag: tag.name == "dt" and "Apply by | Start date" in tag.text)
        deadline = (deadlineTag.parent).find("dd").text[:10]  

        jobDicts.append({"title": title , "salary": salary , "link": link, "deadline": deadline})
    
    return jobDicts
