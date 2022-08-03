import csv
import random
import pandas as pd

def reviews(reviewers_file, reviewees_file, num_reviewers):
    try:
        if num_reviewers <= 0:
            return "Invalid number of reviewers"
    except:
        return "Invalid reviewers"

    # Compile the Reviewers data
    try:
        ers_df = pd.read_csv(reviewers_file, index_col="Reviewer")
    except:
        return "No Reviewer column in Reviewers table"

    # Make sure columns are correct
    headers = list(ers_df.columns)
    for header in ["Team"]:
        if header not in headers:
            return "No " + header + " column in Reviewers table"
    reviewers = list(ers_df.index.values)

    experience = True
    if "Experienced" not in headers:
        experience = False

    # Compile the Reviewees data
    try:
        ees_df = pd.read_csv(reviewees_file, index_col="Reviewee")
    except:
        return "No Reviewee column in Reviewees table"

    # Make sure columns are correct
    headers = list(ees_df.columns)
    for header in ["Team"]:
        if header not in headers:
            return "No " + header + " column in Reviewees table"
    reviewees = list(ees_df.index.values)

    # Create dictionary containing reviewer-to-reviewee matchings
    matchings = {}
    for reviewee in ees_df.index.values:
        matchings[reviewee] = []

    while True:
        for reviewer in reviewers:
            # Iterate through the reviewees in a random order
            random.shuffle(reviewees)
            for reviewee in reviewees:
                # Find the current reviewers for the reviewee
                chosen = matchings[reviewee]

                # Check if the reviewee is valid
                if ees_df.loc[reviewee, "Team"] != ers_df.loc[reviewer, "Team"] and len(chosen) < num_reviewers and reviewer not in chosen:
                    # Make sure nobody gets all inexperienced reviewers
                    if experience:
                        if num_reviewers > 1 and len(chosen) == num_reviewers - 1 and ers_df.loc[reviewer, "Experienced"] == "n":
                            no_experience = True
                            for assigned in chosen:
                                if ers_df.loc[assigned, "Experienced"] == "y":
                                    no_experience = False
                                    break
                            if no_experience:
                                continue
                    matchings[reviewee].append(reviewer)
                    break

        # Check if everyone has been reviewed the correct number of times
        all_reviewed = True
        for assigned in matchings.values():
            if len(assigned) < num_reviewers:
                all_reviewed = False
                break

        if all_reviewed:
            break

    # Return dictionary of information
    return {"matchings":matchings, "ers_df":ers_df, "ees_df":ees_df}

def test(num_reviewers, experience=False):
    # Open files
    if experience:
        reviewer_file = open("Reviews_-_Reviewers.csv", "r")
    else:
        reviewer_file = open("NoExperience.csv")
    reviewee_file = open("Reviews_-_Reviewees.csv", "r")

    # Execute function and store data
    info = reviews(reviewer_file, reviewee_file, num_reviewers)
    matchings = info["matchings"]
    ers_df = info["ers_df"]
    ees_df = info["ees_df"]

    correct_reviewers = True
    if experience:
        one_experienced = True
    different_team = True

    for reviewee in ees_df.index.values:
        assigned = matchings[reviewee]
        if len(assigned) != num_reviewers:
            correct_reviewers = False
            break

        if experience:
            no_experience = True
            for reviewer in assigned:
                if ers_df.loc[reviewer, "Experienced"] == "y":
                    no_experience = False
                    break
            if no_experience:
                one_experienced = False

        for reviewer in assigned:
            if ees_df.loc[reviewee, "Team"] == ers_df.loc[reviewer, "Team"]:
                different_team = False

    num_reviews = {}
    for reviewer in ers_df.index.values:
        count = 0
        for assigned in matchings.values():
            if reviewer in assigned:
                count += 1
        num_reviews[reviewer] = count

    print(num_reviewers, "experience", experience)
    print(correct_reviewers, "correct number of reviewers")
    if num_reviewers != 1 and experience:
        print(one_experienced, "one experienced")
    print(different_team, "different team")
    print(num_reviews)

for n in range(1, 4):
    test(n)
    test(n, True)