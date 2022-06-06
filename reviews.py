import csv
import random
import pandas as pd

def reviews(reviewers_file, reviewees_file, num_reviewers):
    # Compile the Reviewers data
    try:
        ers_df = pd.read_csv(reviewers_file, index_col="Reviewer")
    except:
        return "No Reviewer column in Reviewers table"

    # Make sure columns are correct
    headers = list(ers_df.columns)
    for header in ["Team", "Experienced"]:
        if header not in headers:
            return "No " + header + " column in Reviewers table"
    reviewers = list(ers_df.index.values)

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
                if ees_df.loc[reviewee, "Team"] != ers_df.loc[reviewer, "Team"] and len(chosen) < 2 and reviewer not in chosen:
                    # Make sure nobody gets all inexperienced reviewers
                    if len(chosen) == num_reviewers - 1 and ers_df.loc[reviewer, "Experienced"] == "n" and ers_df.loc[chosen[0], "Experienced"] == "n":
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

    return {"matchings":matchings, "ers_df":ers_df, "ees_df":ees_df}

def test():
    reviewer_file = open("Reviews_-_Reviewers.csv", "r")
    reviewee_file = open("Reviews_-_Reviewees.csv", "r")
    info = reviews(reviewer_file, reviewee_file, 2)
    matchings = info["matchings"]
    ers_df = info["ers_df"]
    ees_df = info["ees_df"]

    two_reviewers = True
    one_experienced = True
    different_team = True

    for reviewee in ees_df.index.values:
        assigned = matchings[reviewee]
        if len(assigned) != 2:
            two_reviewers = False
            break

        if ers_df.loc[assigned[0], "Experienced"] == "n" and ers_df.loc[assigned[1], "Experienced"] == "n":
            one_experienced = False

        team = ees_df.loc[reviewee, "Team"]
        if team == ers_df.loc[assigned[0], "Team"] or team == ers_df.loc[assigned[1], "Team"]:
            different_team = False

    num_reviews = {}
    for reviewer in ers_df.index.values:
        count = 0
        for assigned in matchings.values():
            if reviewer in assigned:
                count += 1
        num_reviews[reviewer] = count

    print(two_reviewers, "two reviewers")
    print(one_experienced, "one experienced")
    print(different_team, "different team")
    print(num_reviews)

test()