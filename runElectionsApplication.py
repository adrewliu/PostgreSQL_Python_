import datetime
import psycopg2
import sys


def usage():
    print("Usage:  python3 runElectionsApplication.py userid pwd", file=sys.stderr)
    sys.exit(-1)


'''
party is an attribute in the CandidatesForOffice table, indicating the candidate for office’s
party in an election. A candidate for office in an election runs in a particular party.
Every office holder must be a candidate for office, but some candidates for office are office
holders and some are not. Any office holder was in a particular party in the election in which
they were candidates for office. The argument, myConn, is the database connection and the argument,
theParty, is a string which is a party. This Python function prints out the number of candidates for
office and the number of office holders who were in myParty when they ran as candidates for office
in an election.
'''
def printNumPartyCandidatesAndOfficeHolders (myConn, theParty):
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


'''
salary is an attribute of the ElectedOffices table. This function increases the salary by a
certain amount (theSalaryIncrease) for all the elected offices who salary value is less than
or equal some salary limit (theLimitValue).
Besides the database connection, the increaseLowSalaries function has two arguments,
a float argument theSalaryIncrease and another float argument, theLimitValue. For every
elected office in the ElectedOffices table (if any) whose salary is less than or equal to
theLimitValue, increaseLowSalaries should increase that salary value by theSalaryIncrease.
'''
def increaseLowSalaries (myConn, theSalaryIncrease, theLimitValue):
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


'''
rating is an attribute of the OfficeHolders table. This function invokes the stored function
 improveSomeRatingsFunction and improves the ratings for office holders that satisfy the 
 conditions defined in improveSomeRatingsFunction. The argument, maxRatingImprovements, sets
 a limit to the number of ratings that could be improved for the party, which is a string 
 argument (theParty).
 '''
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


'''
This function prints the results of the improveSomeRatings function and takes in the same 
arguments.
'''
def printRatingImprovements(myConn, theParty, maxRatingImprovements):
    improvements = improveSomeRatings(myConn, theParty, maxRatingImprovements)
    if improvements < 0:
        print(f"An error has occurred for party '{theParty}'  numbers of ratings improved for maxRatingImprovements value '{maxRatingImprovements}' is: 0\n")
        return -1
    print(f"Number of ratings which improved for party '{theParty}' for maxRatingImprovements value '{maxRatingImprovements}' is: {improvements}")


def main():
    if len(sys.argv) != 3:
        usage()

    hostname = "cse182-db.lt.ucsc.edu"
    userID = sys.argv[1]
    pwd = sys.argv[2]

    #connection to the database
    try:
        myConn = psycopg2.connect(host=hostname, user=userID, password=pwd)
    except:
        print("Connection to database failed", file=sys.stderr)
        sys.exit(-1)

    myConn.autocommit = True

    # Tests for each of the functions.

    printNumPartyCandidatesAndOfficeHolders(myConn, 'Silver')
    # Number of candidates from party Silver is 6.
    # Number of office holders from party Silver is 0.
    printNumPartyCandidatesAndOfficeHolders(myConn, 'Copper')
    # Number of candidates from party Copper is 12.
    # Number of office holders from party Copper is 7.

    increaseLowSalaries(myConn, 6000, 125000)
    # Number of elected offices whose salaries under 125000 were updated by 6000 is  4
    increaseLowSalaries(myConn, 4000, 131000)
    # Number of elected offices whose salaries under 131000 were updated by 4000 is  4

    printRatingImprovements(myConn, 'Copper', 6)
    # Number of ratings which improved for party 'Copper' for maxRatingImprovements value '6' is: 4
    printRatingImprovements(myConn, 'Gold', 1)
    # Number of ratings which improved for party 'Gold' for maxRatingImprovements value '1' is: 1
    printRatingImprovements(myConn, 'Silver', 1)
    # Number of ratings which improved for party 'Silver' for maxRatingImprovements value '1' is: 0
    printRatingImprovements(myConn, 'Platinum', 0)
    # Number of ratings which improved for party 'Platinum' for maxRatingImprovements value '0' is: 0
    printRatingImprovements(myConn, 'Copper', 6)
    # Number of ratings which improved for party 'Copper' for maxRatingImprovements value '6' is: 3

    myConn.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
