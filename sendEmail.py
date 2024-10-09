from redmail import EmailSender, gmail
import requests
from scraper import scrape
import sqlite3
from datetime import datetime

# Set up email details
gmail.username = 'mtgoktopal@gmail.com'  
gmail.password = ''  #Removed for safety


# Scrape the data
scraped_jobs = scrape()

#Fetch all the mail adresses from the database
connection = sqlite3.connect("apprenticeship_listings.db",check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""SELECT * FROM emails""")
Emails = cursor.fetchall()


for email in Emails:
    sortedJobs = []
    #Orders the listings based on the user's choice
    if email[2] == "greatest salary" :
        sortedJobs = sorted(scraped_jobs, key=lambda x: x['salary'], reverse=True)
    
    elif email[2] == "earliest deadline":
        scraped_jobs.sort(key = lambda x: datetime.strptime(x['deadline'], '%d/%m/%Y'))
        sortedJobs = scraped_jobs

    # Get the number of listings from email[3]
    num_listings = int(email[3])

    # Build the HTML body manually
    html_body = f"""
    <head>
        <title>Weekly Apprenticeship Listings</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .card {{
                margin-bottom: 20px;
                border: none;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .card-body {{
                padding: 20px;
            }}
            .card-title {{
                color: #007bff;
                font-size: 1.25rem;
                font-weight: bold;
            }}
            .card-subtitle {{
                margin-bottom: 10px;
                font-size: 1rem;
                color: #6c757d;
            }}
            .card-text {{
                font-size: 0.95rem;
                color: #495057;
            }}
            .btn {{
                margin-top: 10px;
                padding: 10px 20px;
                font-size: 1rem;
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                text-decoration: none;
            }}
            .btn:hover {{
                background-color: #0056b3;
                color: white;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.875rem;
                color: #6c757d;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Weekly Apprenticeship Listings</h2>
                <p>Here are the top {num_listings} apprenticeship listings based on your preferences!</p>
            </div>
    """

    # Add job listings dynamically
    for i in range(0, num_listings):
        html_body += f"""
            <div class="card">
                <div class="card-body">
                    <h4 class="card-title">{sortedJobs[i]["title"]}</h4>
                    <h5 class="card-subtitle mb-2 text-muted">Employer: {sortedJobs[i]["company"]} - Location: {sortedJobs[i]["location"]}</h5>
                    <p class="card-text">Salary: {sortedJobs[i]["salary"]} <br>Deadline: {sortedJobs[i]["deadline"]}</p>
                    <a href="{sortedJobs[i]['link']}" class="btn">Apply Now</a>
                </div>
            </div>
        """

    # Close the HTML body
    html_body += """
            <div class="footer">
                <p>You are receiving this email because you signed up for weekly apprenticeship listings.</p>
                <p>Want to update your preferences? <a href="unsubscribe-link">Click here to unsubscribe</a>.</p>
            </div>
        </div>
    </body>
    """


    # Send the email
    gmail.send(
        subject="Apprenticeship Listings",
        receivers=[email[1]],
        html=html_body
    )
