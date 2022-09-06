# Performance Reviews
#### Video Demo:  <URL HERE>

I created this web app for a company when I learned that they needed a tool to automatically generate assignments for managers to review employees from other teams.

## How It Works

#### Input

The app provides step-by-step instructions to create two csv files using Google Sheets. One csv contains the reviewers and their teams, and the other contains the reviewees and their teams. The app provides the option to include another column in the reviewers file that contains whether the reviewer is experienced or not. There is one more input field that has the user choose the number of reviewers that review each reviewee.

#### Algorithm

The app will provide pairings as follows.

1. No reviewer will review someone from their own team.
2. Each reviewer will have to review roughly the same number of people.
3. If there is more than one reviewer per reviewee, and the experienced column is provided, no reviewee will get only inexperienced reviewers.

The app uses a randomizer to distribute the reviewers evenly.

#### Output

Once the user submits, they will see a table containing all of the assignments, as well as a button allowing them to download the data to their computer as a csv.

#### Error Handling

Whenever an invalid input is entered, the app will redirect to the home page and display a message explaining the error at the top of the screen.

## Python Files

#### app.py

I am using a Flask application, so this is the central file that handles the input and sends it to different parts of the project. It also handles the errors and turns them into error messages. I intentionally left most of the actual algorithm to reviews.py and focused app.py on redirecting.

#### reviews.py

This is where the bulk of the project is. It contains the algorithm that takes the csv files and turns it into the assignments. While I was originally using multiple dictionaries to contain the data, I switched to using two pandas dataframes, which work much more cleanly. Also in this file is a detailed testing function that ensures that the algorithm works. This helped greatly during the proccess as it was an easy way to make sure the code was working correctly after a change was made.

## HTML Files

#### layout.html

This layout file allows for the use of Bootstrap and my style sheet and allows error-handling in all of the HTML files. While it is a little strange to have a layout file with just two other HTML files, I think it helps the main files look cleaner and more readable.

#### index.html

This is the homepage of the application which contains the instructions to create the csv files as well as the input fields.

#### reviewers.html

Once the form is submitted in index.html, app.py uses reviews.py to create the assignments, then sends the output here. This is where the user can see the assignments and download them in the top right corner.

## \static

THe static folder contains a number of screenshots as well as a stylesheet to help pretty up the app.