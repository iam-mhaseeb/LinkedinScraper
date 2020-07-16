# LinkedinScraper
LinkedinScrapper scrapes user profiles from Linkedin decently without getting you in trouble in 2020.

## Installation

Installation is simplest with pip:
1. Clone the repository
2. Create a virtual enviorment & activate it
3. Run `pip install -r requirements.txt` to install dependencies
4. Go to config.json 
   1. Add or change query in `USER_QUERIES` using Google dorks
   2. Add Linkedin `username` or `email` in `LINUSERNAME`
   3. Add `password` in `LINPWD`
5. Run `python linked_scraper.py user` to start scraping

### Scraped data goes into `scrapped_data.json` file

## Sample data is in [sample file](https://github.com/iam-mhaseeb/LinkedinScraper/blob/master/scrapped_data.json)

```
[
    {
        "URL": "https://pk.linkedin.com/in/saifurrehman",
        "name": "Saif-ur- Rehman",
        "query": "site:linkedin.com/in/ AND \"software engineer\" AND \"lahore\"",
        "job_title": "Senior Software Developer at Programmers Force",
        "degree": [
            {
                "school_name": "University of the Punjab, Lahore",
                "degree_name": "Degree NameBachelor of Information and Technology",
                "dates": "Dates attended or expected graduation2010\u20132014"
            },
            {
                "school_name": "Govt Central ModelSchool Lower Mall",
                "degree_name": "Degree NameSecondary School Certificate",
                "dates": "Dates attended or expected graduation2002\u20132007"
            }
        ],
        "experience": [
            {
                "job_title": "Senior Software Developer",
                "company_name": "Programmers Force",
                "dates": "Dates EmployedMay 2017 \u2013 Present",
                "duration": "3 yrs 3 mos",
                "location": "LocationLahore, Pakistan"
            },
            {
                "job_title": "Software Developer",
                "company_name": "Devtron Genesis",
                "dates": "Dates EmployedJul 2016 \u2013 May 2017",
                "duration": "11 mos",
                "location": "LocationLahore, Pakistan"
            },
            {
                "job_title": "Game Developer",
                "company_name": "Cyber Village Studios",
                "dates": "Dates EmployedMar 2016 \u2013 Jun 2016",
                "duration": "4 mos",
                "location": "LocationLahore, Pakistan"
            }
        ],
        "location": "Lahore, Pakistan",
        "languages": [],
        "skills": [
            "Node.js",
            "Vue.js",
            "Laravel",
            "Software Engineering",
            "Project Management",
            "ISM Code",
            "Web Development",
            "Java",
            "CodeIgniter",
            "JavaScript",
            "JSON",
            "jQuery",
            "Bootstrap",
            "PHP",
            "MySQL",
            "Git",
            "JSP",
            "C#",
            "Drupal",
            "HTML5",
            "C++",
            "UML",
            "Eclipse",
            "Microsoft Office",
            "Apache",
            "Cascading Style Sheets (CSS)",
            "NetBeans",
            "HTML",
            "Windows",
            "XML",
            "Photoshop",
            "SQL",
            "Microsoft Excel",
            "Unity3D",
            "PhpMyAdmin",
            "AJAX",
            "Problem Solving",
            "Symfony Framework",
            "Smart Draw",
            "Sublime Text",
            "Use Case Diagrams",
            "PHP Applications",
            "Electron",
            "Electron App",
            "electrin.js"
        ],
        "contact_info": {
            "phone_number": "",
            "email": "mailto:saifurrehman.developer@gmail.com",
            "linkedin": "https://www.linkedin.com/in/saifurrehman",
            "twitter": "https://twitter.com/Saif_Ur__Rehman",
            "websites": "",
            "birthday": ""
        }
    }
]
```
    

## TODO

1. Minimize time required for scraping
2. Clean data with more accuracy
3. Introduce job scraper


## Authors

* **Muhammad Haseeb** - *Initial work* - [Muhammad Haseeb](https://github.com/iam-mhaseeb)
