import csv
import random

teams = {}

# Compile the Reviewers data
experienced = {}
reviewers = []
with open("Reviews - Reviewers.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["Reviewer"]
        teams[name] = row["Team"]
        experienced[name] = row["Experienced"]
        reviewers.append(name)

# Compile the Reviewees data
reviewees = []
with open("Reviews - Reviewees.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        teams[row["Reviewee"]] = row["Team"]
        reviewees.append(row["Reviewee"])

# Create dictionary containing reviewer-to-reviewee matchings
reviewed = {}
for reviewee in reviewees:
    reviewed[reviewee] = []

# Repeat until all are reviewed
while True:
    for reviewer in reviewers:
        # Iterate through the reviewees in a random order
        random.shuffle(reviewees)
        for reviewee in reviewees:
            # Find the current reviewers for the reviewee
            chosen = reviewed[reviewee]

            # Check if the reviewee is valid
            if teams[reviewee] != teams[reviewer] and len(chosen) < 2 and reviewer not in chosen:
                # Make sure nobody gets two inexperienced reviewers
                if len(chosen) == 1 and experienced[reviewer] == "n" and experienced[chosen[0]] == "n":
                    continue
                reviewed[reviewee].append(reviewer)
                break

    # Check if everyone has been reviewed twice
    all_reviewed = True
    for assigned in reviewed.values():
        if len(assigned) < 2:
            all_reviewed = False
            break

    if all_reviewed:
        break

with open("output.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Reviewee", "Team", "Reviewer1", "Reviewer2"])
    for reviewee in reviewees:
        writer.writerow([reviewee, teams[reviewee], reviewed[reviewee][0], reviewed[reviewee][1]])

# two_reviewers = True
# one_experienced = True
# different_team = True

# for reviewee in reviewees:
#     assigned = reviewed[reviewee]
#     if len(assigned) != 2:
#         two_reviewers = False
#         break

#     if experienced[assigned[0]] == "n" and experienced[assigned[1]] == "n":
#         one_experienced = False

#     if teams[reviewee] == teams[assigned[0]] or teams[reviewee] == teams[assigned[1]]:
#         different_team = False

# reviews = {}
# for reviewer in reviewers:
#     count = 0
#     for assigned in reviewed.values():
#         if reviewer in assigned:
#             count += 1
#     reviews[reviewer] = count

# print(two_reviewers, "two reviewers")
# print(one_experienced, "one experienced")
# print(different_team, "different team")
# print(reviews)