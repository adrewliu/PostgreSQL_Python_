#! /usr/bin/env python

#  runElectionsApplication Solution

import datetime
import psycopg2
import sys


# usage()
# Print error messages to stderr
def usage():
    print("Usage:  python3 runElectionsApplication.py userid pwd", file=sys.stderr)
    sys.exit(-1)
# end usage

# The three Python functions that for Lab4 should appear below.
# Write those functions, as described in Lab4 Section 4 (and Section 5,
# which describes the Stored Function used by the third Python function).
#
# Write the tests of those function in main, as described in Section 6
# of Lab4.


 # printNumPartyCandidatesAndOfficeHolders (myConn, theParty):
 # party is an attribute in the CandidatesForOffice table, indicating the candidate for office’s
 # party in an election.  A candidate for office in an election runs in a particular party.
 # Every office holder must be a candidate for office (referential integrity), but some
 # candidates for office are office holders and some are not.  Any office holder was in a
 # particular party in the election in which they were candidates for office.
 #
 # The arguments for the printNumPartyCandidatesAndOfficeHolders Python function are the database
 # connection and a string argument, theParty, which is a party.  This Python function prints
 # out the number of candidates for office and the number of offfice holders who were in myParty
 # when they ran as candidates for office in an election.
 #
 # For more details, including error handling and return codes, see the Lab4 pdf.

def printNumPartyCandidatesAndOfficeHolders (myConn, theParty):
    # Python function to be supplied by students
    if theParty is None:
        return -1

    try:
        myCursor = myConn.cursor()
        myCursor.execute("SELECT count(*) FROM CandidatesForOffice WHERE party = %s", (theParty,))
        numPartyCandidates = myCursor.fetchone()[0]
        myCursor.execute("SELECT COUNT(*) FROM OfficeHolders o JOIN CandidatesForOffice c ON o.candidateID = c.candidateID AND o.officeID = c.officeID AND o.electionDate = c.electionDate WHERE c.party = %s", (theParty,))
        numOfficeHolders = myCursor.fetchone()[0]
        # printNumPartyCandidatesAndOfficeHolders = myCursor.rowcount
        # print("Number of office holders from party ", theParty, "is ", printNumPartyCandidatesAndOfficeHolders)
        print(f"Number of candidates from party {theParty} is {numPartyCandidates}.")
        print(f"Number of office holders from party {theParty} is {numOfficeHolders}.")
        return 0

    except psycopg2.Error as e:
        print("selection from CandidatesForOffice had error", e)
        return -1

    finally:
        myCursor.close()

# end printNumPartyCandidatesAndOfficeHolders


# increaseLowSalaries (myConn, theSalaryIncrease, theLimitValue):
# salary is an attribute of the ElectedOffices table.  We’re going to increase the salary by a
# certain amount (theSalaryIncrease) for all the elected offices who salary value is less than
# or equal some salary limit (theLimitValue).'
#
# Besides the database connection, the increaseLowSalaries Python function has two arguments,
# a float argument theSalaryIncrease and another float argument, theLimitValue.  For every
# elected office in the ElectedOffices table (if any) whose salary is less than or equal to
# theLimitValue, increaseLowSalaries should increase that salary value by theSalaryIncrease.
#
# For more details, including error handling, see the Lab4 pdf.

def increaseLowSalaries (myConn, theSalaryIncrease, theLimitValue):
#
#     # Python function to be supplied by students
#     # You'll need to figure out value to return.
    if theSalaryIncrease <= 0:
        return -1
    if theLimitValue <= 0:
        return -2

    try:
        myCursor = myConn.cursor()
        myCursor.execute("UPDATE ElectedOffices SET salary = salary + %s WHERE salary <= %s AND salary > 0", (theSalaryIncrease, theLimitValue))
        numOfUpdates = myCursor.rowcount
        print("Number of elected offices whose salaries under", theLimitValue, "were updated by", theSalaryIncrease, "is ", numOfUpdates)
    except psycopg2.Error as e:
        print("updating salary, had error", e)
        myCursor.close()
        myConn.close()
        sys.exit(-1)
    myCursor.close()
    return numOfUpdates
# end increaseLowSalaries


def improveSomeRatings (myConn, theParty, maxRatingImprovements):
    try:
        myCursor = myConn.cursor()
        sql = "SELECT improveSomeRatingsFunction(%s, %s)"
        myCursor.execute(sql, (theParty, maxRatingImprovements))
    except:
        print("Call of improveSomeRatingsFunction with arguments", theParty, maxRatingImprovements, "had error", file=sys.stderr)
        myCursor.close()
        myConn.close()
        sys.exit(-1)

    row = myCursor.fetchone()
    myCursor.close()
    return(row[0])
#end improveSomeRatings


def printRatingImprovements(myConn, theParty, maxRatingImprovements):
    improvements = improveSomeRatings(myConn, theParty, maxRatingImprovements)
    print(f"Number of ratings which improved for party '{theParty}' for maxRatingImprovements value '{maxRatingImprovements}' is: {improvements}")


def main():
    if len(sys.argv) != 3:
        usage()

    hostname = "cse182-db.lt.ucsc.edu"
    userID = sys.argv[1]
    pwd = sys.argv[2]

    # Try to make a connection to the database
    try:
        myConn = psycopg2.connect(host=hostname, user=userID, password=pwd)
    except:
        print("Connection to database failed", file=sys.stderr)
        sys.exit(-1)

    # We're making every SQL statement a transaction that commits.
    # Don't need to explicitly begin a transaction.
    # Could have multiple statement in a transaction, using myConn.commit when we want to commit.

    myConn.autocommit = True

    # There are other correct ways of writing all of these calls correctly in Python.

    # Perform tests of printNumPartyCandidatesAndOfficeHolders, as described in Section 6 of
    # Lab4.  That Python function handles printing when there is no error.
    # Print error outputs here. You may use a Python method to help you do the printing.

    printNumPartyCandidatesAndOfficeHolders(myConn, 'Silver')
    # Number of candidates from party Silver is 6.
    # Number of office holders from party Silver is 0.
    printNumPartyCandidatesAndOfficeHolders(myConn, 'Copper')
    # Number of candidates from party Copper is 12.
    # Number of office holders from party Copper is 7.

    # Perform tests of increaseLowSalaries, as described in Section 6 of Lab4.
    # Print their outputs (including error outputs) here, not in increaseLowSalaries.
    # You may use a Python method to help you do the printing.
    increaseLowSalaries(myConn, 6000, 125000)
    # Number of elected offices whose salaries under 125000 were updated by 6000 is  4
    increaseLowSalaries(myConn, 4000, 131000)
    # Number of elected offices whose salaries under 131000 were updated by 4000 is  4

    # Perform tests of improveSomeRatings, as described in Section 6 of Lab4,
    # Print their outputs (including error outputs) here, not in improveSomeRatings.
    # You may use a Python method to help you do the printing.
    printRatingImprovements(myConn, 'Copper', 6)
    # Rating improvements for party 'Copper': 4
    printRatingImprovements(myConn, 'Gold', 1)
    # Rating improvements for party 'Gold': 1
    printRatingImprovements(myConn, 'Silver', 1)
    # Rating improvements for party 'Silver': 0
    printRatingImprovements(myConn, 'Platinum', 0)
    # Rating improvements for party 'Platinum': 0
    printRatingImprovements(myConn, 'Copper', 6)
    # Rating improvements for party 'Copper': 3

    myConn.close()
    sys.exit(0)


# end

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# end
