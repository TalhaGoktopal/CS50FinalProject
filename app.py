from flask import Flask, render_template, request, redirect
from scraper import scrape
from datetime import datetime
import sqlite3
import math

#Establish connection and cursor
connection = sqlite3.connect("apprenticeship_listings.db",check_same_thread=False)
cursor = connection.cursor()

#Creates the emails table
cursor.execute(""" CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT, priority TEXT, numberOfListings TEXT) """)

#Creates the app
app = Flask(__name__)

scraped_apprenticeships = scrape()
sortedApprenticeships = []

#THIS IS GOING TO BE THE MAIN SCREEN
@app.route("/", methods=["GET", "POST"])
def main():
    # Number of jobs per page
    jobs_per_page = 5
    
    # Get the current page number and sorting preferences from query parameters
    page = request.args.get('page', 1, type=int)
    orderBy = request.args.get('orderBy', 'salary')
    orderType = request.args.get('orderType', 'ascending')

    # Default sorting: if no POST request, or if GET request with query parameters
    if request.method == "POST":
        # If sorting preferences submitted via form
        orderBy = request.form.get("orderBy")
        orderType = request.form.get("orderType")
    
    # Sort based on the user's choice
    if orderBy == "salary" and orderType == "ascending":
        sortedApprenticeships = sorted(scraped_apprenticeships, key=lambda x: x['salary'])
    elif orderBy == "salary" and orderType == "descending":
        sortedApprenticeships = sorted(scraped_apprenticeships, key=lambda x: x['salary'], reverse=True)
    elif orderBy == "deadline" and orderType == "ascending":
        sortedApprenticeships = sorted(scraped_apprenticeships, key=lambda x: datetime.strptime(x['deadline'], '%d/%m/%Y'))
    elif orderBy == "deadline" and orderType == "descending":
        sortedApprenticeships = sorted(scraped_apprenticeships, key=lambda x: datetime.strptime(x['deadline'], '%d/%m/%Y'), reverse=True)
    
    # Slice the jobs list to display only jobs for the current page
    start = (page - 1) * jobs_per_page
    end = start + jobs_per_page
    paginated_jobs = sortedApprenticeships[start:end]

    # Calculate total number of pages
    total_pages = math.ceil(len(scraped_apprenticeships) / jobs_per_page)

    return render_template('main2.html', jobDicts=paginated_jobs, page=page, total_pages=total_pages, orderBy=orderBy, orderType=orderType)

@app.route("/register", methods = ["GET", "POST"])
def register():
    numListings = ""
    emailPriority = ""
    emailSaved = False

    if request.method == "POST":
        emailAddress = request.form.get("Email")
        if emailAddress != request.form.get("confirmEmail"):
            pass #Render teh eror function telling the user the email dont match
        
        numListings = request.form.get("numberOfListings")
        emailPriority = request.form.get("priority")

        #Check if email is already saved
        cursor.execute("""SELECT email FROM emails WHERE email = ?""", (emailAddress,))
        savedEmails = cursor.fetchall()

        for savedEmail in savedEmails:
            if emailAddress in savedEmail:
                emailSaved = True
        
        
        if emailSaved == True:
            #If it is updates its preferences
            cursor.execute("""UPDATE emails SET priority = ?, numberOfListings = ?  WHERE email == ?""", (emailPriority, numListings, emailAddress))    

        #Else create a new entry with preferences
        else:
            cursor.execute("""INSERT INTO emails (email, priority, numberOfListings) VALUES (?, ?, ?)""", (emailAddress,emailPriority, numListings ))
    
        connection.commit()
        return redirect("/")
    return render_template("register.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', debug=True)