import csv
import random

def reviews(reviewers_file, reviewees_file):
    teams = {}

    # Compile the Reviewers data
    experienced = {}
    reviewers = []
    reader = csv.DictReader(reviewers_file)
    for row in reader:
        name = row["Reviewer"]
        teams[name] = row["Team"]
        experienced[name] = row["Experienced"]
        reviewers.append(name)

    # Compile the Reviewees data
    reviewees = []
    reader = csv.DictReader(reviewees_file)
    for row in reader:
        teams[row["Reviewee"]] = row["Team"]
        reviewees.append(row["Reviewee"])

    # Create dictionary containing reviewer-to-reviewee matchings
    matchings = {}
    for reviewee in reviewees:
        matchings[reviewee] = []

    # Repeat until all are reviewed
    while True:
        for reviewer in reviewers:
            # Iterate through the reviewees in a random order
            random.shuffle(reviewees)
            for reviewee in reviewees:
                # Find the current reviewers for the reviewee
                chosen = matchings[reviewee]

                # Check if the reviewee is valid
                if teams[reviewee] != teams[reviewer] and len(chosen) < 2 and reviewer not in chosen:
                    # Make sure nobody gets two inexperienced reviewers
                    if len(chosen) == 1 and experienced[reviewer] == "n" and experienced[chosen[0]] == "n":
                        continue
                    matchings[reviewee].append(reviewer)
                    break

        # Check if everyone has been reviewed twice
        all_reviewed = True
        for assigned in matchings.values():
            if len(assigned) < 2:
                all_reviewed = False
                break

        if all_reviewed:
            break

    return {"matchings":matchings, "reviewers":reviewers, "reviewees":reviewees, "experienced":experienced, "teams":teams}

def test():
    reviewer_file = open("Reviews_-_Reviewers.csv", "r")
    reviewee_file = open("Reviews_-_Reviewees.csv", "r")
    info = reviews(reviewer_file, reviewee_file)
    matchings = info["matchings"]

    two_reviewers = True
    one_experienced = True
    different_team = True

    for reviewee in info["reviewees"]:
        assigned = matchings[reviewee]
        if len(assigned) != 2:
            two_reviewers = False
            break

        experienced = info["experienced"]
        if experienced[assigned[0]] == "n" and experienced[assigned[1]] == "n":
            one_experienced = False

        teams = info["teams"]
        if teams[reviewee] == teams[assigned[0]] or teams[reviewee] == teams[assigned[1]]:
            different_team = False

    num_reviews = {}
    for reviewer in info["reviewers"]:
        count = 0
        for assigned in matchings.values():
            if reviewer in assigned:
                count += 1
        num_reviews[reviewer] = count

    print(two_reviewers, "two reviewers")
    print(one_experienced, "one experienced")
    print(different_team, "different team")
    print(num_reviews)

# test()