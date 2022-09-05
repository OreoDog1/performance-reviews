# Google Performance Reviews
#### Video Demo:  <URL HERE>
#### Description:

I created this web app for Google when I learned that they needed a tool to automatically generate assignments for managers to review employees from other teams.

### The Input

The app provides step-by-step instructions to create two csv files using Google Sheets. One csv contains the reviewers and their teams, and the other contains the reviewees and their teams. The app provides the option to include another column in the reviewers file that contains whether the reviewer is experienced or not. There is one more input field that has the user choose the number of reviewers that review each reviewee.

### The Algorithm

The app will provide pairings as follows.

1. No reviewer will review someone from their own team.
2. Each reviewer will have to review roughly the same number of people.
3. If there is more than one reviewer per reviewee, and the experienced column is provided, no reviewee will get only inexperienced reviewers.

The app uses a randomizer to distribute the reviewers evenly.

### The Output

Once the user submits, they will see a table containing all of the assignments, as well as a button allowing them to download the data to their computer as a csv.