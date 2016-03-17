"""StudentDatabase.py
CSC 109.02 Mid-term Project
Author      : Catherine Grillo
Created     : 11/01/2015
Last Updated: 11/05/2015
Due         : 11/06/2015
"""
import sqlite3 as sq

#create and connect to a database students.db
db = sq.connect('students.db')

#set a cursor in the database
cursor = db.cursor()

#make a table student1 in database students with 7 fields
cursor.execute('''CREATE TABLE IF NOT EXISTS student1(id INTEGER PRIMARY KEY, studentID TEXT, fname TEXT, lname TEXT, gradYear TEXT, email TEXT,
size TEXT)''')
db.commit()

#function displays main menu options
def displayMenu():
    print('\n')
    print("MAIN MENU")
    print("*********")
    print("1. Display all student entries")
    print("2. Display t-shirt sizes")
    print("3. Add new student entry")
    print("4. Modify student entries")
    print("5. Delete student entry")
    print("Enter 'q' to quit\n")

#function displays modification menu for option 4 from amin menu
def displayMenu2():
    print('\n')
    print("Modification Menu")
    print("*********")
    print("1. First name")
    print("2. Last name")
    print("3. Graduation year")
    print("4. Email address")
    print("5. T-shirt size")
    print("Enter 'q' to quit\n")

#function displays all entries in the table
def displayAll():
    cursor.execute("SELECT * FROM student1")
    allEntries = cursor.fetchall()
    #prints each student entry in a seperate row
    for entry in allEntries:
        print(entry+'\n')

#function prints who has a certain tshirt size and how many have that size.
def displaySize(x):
    cursor.execute("SELECT * FROM student1")
    rows = cursor.fetchall()
    sNames = []
    #loop through the student entries
    for row in rows:
        #change entry from tuple to list
        row=list(row)
        #if the student's tshirt size is the one being counted, add their name to the list sNames
        if row[6] == x:
            sNames.append(row[2]+" "+row[3])
    #count the number of students in list sNames
    num = len(sNames)
    #print the number of students counted, the size being loked at, and the names of the students.
    if x == 'N/A':
        print(num, "Student(s) did not give a t-shirt size.")
    else:
        print(num, "Student(s) are size", x.upper())
    for sname in sNames:
        print("     "+sname)


#Main Program

#code used to input several starting entries
    #stEntries = [('1234', 'Catherine', 'Grillo', '2018', 'catherinegrillo@live.com', 'Medium'),
    #            ('1357', 'Bruce', 'Wayne', '1980', 'notbatman@hotmail.com', 'Extra Large')]
    #cursor.executemany('''INSERT INTO student1(studentID, fname, lname, gradYear, email, size) VALUES(?,?,?,?,?,?)''',stEntries)

#loop through program as long as user wants
while True:
    #commit any previous updates/changes to the database
    db.commit()
    #user interface
    displayMenu()
    answer = input("Please enter a selection: ")

    if answer == 'q' or answer == 'Q':
        break

    elif answer == '1':
        displayAll()

    #display all size counts and names
    elif answer == '2':
        displaySize('s')
        displaySize('m')
        displaySize('l')
        displaySize('xl')
        displaySize('xxl')
        displaySize('N/A')
        print("\n")

    #new student entry
    elif answer == '3':
        #get student info from user
        id = input("Student ID number (or enter to quit): ")
        if id == '':
            break
        fname = input("First name: ")
        lname = input("Last name: ")
        gradYear = input("(Expected) Graduation year: ")
        email = input("Email address: ")
        size = input("T-shirt size (s,m,l,xl,xxl) (if not given, enter 'N/A'): ")

        #insert student info into table
        cursor.execute('''INSERT INTO student1(studentID, fname, lname, gradYear, email, size) VALUES(?,?,?,?,?,?)''',
                       (id, fname, lname, gradYear, email, size))
        #notify user that the new entry is complete
        print("Student entered into database.\n")

    #modify an entry
    elif answer == '4':
        #loops through mdification as long as user wants to
        while True:
            db.commit()
            #print all entries and as user to input keyID to be modified
            displayAll()
            answer2 = input("Please enter the keyID of the student to be modified or 'q' to quit: ")


            if answer2 == 'q' or answer2 == 'Q':
                break

            else:
                #print field mod options and get user selection
                displayMenu2()
                answer3 = input("Please enter the field number you wish to modify: ")
                if answer3 == 'q' or answer == 'Q':
                    break

                #update the selected field with new input from user
                elif answer3 == '1':
                    finame = input("New first name: ")
                    cursor.execute("UPDATE student1 SET fname=? WHERE id=?", (finame, answer2))

                elif answer3 == '2':
                    laname = input("New last name: ")
                    cursor.execute("UPDATE student1 SET lname=? WHERE id=?", (laname, answer2))

                elif answer3 == '3':
                    graduYear = input("New (expected) graduation year: ")
                    cursor.execute("UPDATE student1 SET gradYear=? WHERE id=?", (graduYear, answer2))

                elif answer3 == '4':
                    emails = input("New email address: ")
                    cursor.execute("UPDATE student1 SET email=? WHERE id=?", (emails, answer2))

                elif answer3 == '5':
                    sizes = input("New t-shirt size (s,m,l,xl,xxl) (if not given, enter 'N/A'): ")
                    cursor.execute("UPDATE student1 SET size=? WHERE id=?", (sizes, answer2))

                #in case of imporper input to answer3, reloop
                else:
                    print("Error. Please try again.")

    #delete existing entry
    elif answer == '5':
        displayAll()
        deleteID = input("Please enter the key ID of the student to be deleted: ")

        #create string with sqlite3 code to delete an entry
        sqlString="DELETE FROM student1 where id="+deleteID
        #execute sqlite3 code
        cursor.execute(sqlString)
        #notify user of deletion
        print("Student "+deleteID+" deleted from database.")

    #in case of imporper input to answer, reloop
    else:
        print("Error. Please try again.")

#close database
db.close()
