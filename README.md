# linkedin-crawler
LinkedIn Crawler is a Python-based tool designed to assist job seekers in gathering publicly available information from LinkedIn profiles. This tool is strictly intended for personal use by individuals looking to streamline their job search process by analyzing professional connections, skill sets, and other relevant data.

## Preview
https://github.com/user-attachments/assets/11ad8094-78d4-4ceb-aec3-916e061f2ad4



## ⚠️ Precautions and Disclaimer
Responsibility Notice:
The use of this tool is entirely at your own discretion and responsibility. This project and its contributors are not responsible for how the tool is used. Misusing LinkedIn Crawler to spam individuals, send unsolicited messages, or violate LinkedIn’s Terms of Service is strictly prohibited and may result in penalties, including account suspension.

Intended Purpose:
This tool is exclusively for individual job seekers. It is not intended for companies or recruiters to send unsolicited messages or cold emails. Use this responsibly and within ethical and legal boundaries.

# 🚀 Installation
## Clone the Repository
```
git clone https://github.com/danniely/linkedin-crawler.git

cd linkedin-crawler
```

## Install Dependencies
```
pip install -r requirements.txt
```

## Set your Linkedin login credentials
```
LINKEDIN_EMAIL=your_email
LINKEDIN_PASSWORD=your_password
```

# 📖 How to Use
## configuration
Set your name, company and job title to match your preference.
```
# example
BASE_SEARCH_URL = ""
MY_FIRST_NAME = "Donlad"
MY_LAST_NAME = "Trump"
MY_SCHOOL = "University of Illinois"
MY_MAJOR = "Computer Science"
COMPANY_NAME = "Microsoft"
JOB_URL = "https://example-job-posting.com"
JOB_TITLE = "software engineer"
```

For BASE_SEARCH_URL, you must go to linkedin, filter your search, then copy the address of that URL into `BASE_SEARCH_URL`.

Example.
```
BASE_SEARCH_URL="linkedin.com/search/results/people/?currentCompany=%5B"1035"%5D&keywords=uiuc&origin=GLOBAL_SEARCH_HEADER&sid=Ks%40"
```
<img width="1298" alt="스크린샷 2025-02-13 17 58 14" src="https://github.com/user-attachments/assets/97c761c5-2b9a-4641-9b8a-428f2001ac57" />


## Run
```
python3 linkedin_crawler.py
```

Happy job searching!

# ❗ Important Notes
This tool is a utility to support personal job searches and must not be abused for mass communication or spamming.
Respect LinkedIn’s rate limits to avoid account restrictions.
For further customization, you can modify the code according to your specific needs.
Disclaimer: Always follow LinkedIn’s Terms of Service and use this tool responsibly. Misuse of this tool may result in consequences beyond the control of its developers.
