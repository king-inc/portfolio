import socket
import sys
import sqlite3
from pathlib import Path        #for path checking



def main():
    
    print("Welcome to Robotic Festival Booking System")
    if not(Path("bookings.db").exists()):   #check if the booking database exists
        createDB()                          #if it does not exist then run createDB function
    
    #ticket section
    printDB(0)                              #run printDB with a tag of zero indicating ticket section
    print("The booking format is below:")   #print booking format 
    print("[Name] [Type of Ticket] [Quantity of Adult’s tickets] [Quantity of Children’s Tickets] \n[Type of Ticket] [Quantity of Adult’s tickets] [Quantity of Children’s Tickets] \n[Type of Ticket n] [Quantity of Adult’s tickets] [Quantity of Children’s Tickets]")
    ticket_cost = server(0)                 #run the server function with a tag of zero indcating ticket section and return ticket cost

    #activity section
    print("You can now book additional activities for the Robotic Festival")
    printDB(1)                              #run printDB with a tag of one indicating activity section
    print("The booking format is below:")   #print booking format
    print("[Name] [Type of Activity] [Quantity of Adult’s Tickets for activity] [Quantity of Children’s Tickets for activity] \n[Type of Activity] [Quantity of Adult’s Tickets for activity] [Quantity of Children’s Tickets for activity] \n[Type of Activity] [Quantity of Adult’s Tickets for activity] [Quantity of Children’s Tickets for activity]")
    activity_cost = server(1)               #run the server function with a tag of one indcating activity section and return activity cost
    print("Your total is " + str(ticket_cost+activity_cost)) #print total cost
    
def createDB():
    '''createDB creates the booking database and
        it's tables'''
   #https://www.geeksforgeeks.org/sql-using-python/
    conn = sqlite3.connect("bookings.db")        #connect to database
    cur = conn.cursor()
    cur.execute("CREATE TABLE tickets (type TEXT,adult_cost INT,child_cost REAL);")     #create table tickets
    cur.execute("INSERT INTO tickets VALUES('Saturday',25,20),('VIP',50,25),('Sunday',10,7.5),('Weekend',30,22);")      #insert values into tickets 
    cur.execute("CREATE TABLE activity (type TEXT,adult_cost INT,child_cost REAL);")    #create table activity
    cur.execute("INSERT INTO activity VALUES('Baking',8,5),('Dancing Class',15,10),('Craft',10,7.5),('Disco',15,11);")  #insert values into activity
    conn.commit()           #commit to database
    conn.close()            #close the connection

def printDB(tag):
    '''printDB prints the values in a table depending on the tag'''
    #https://www.tutorialspoint.com/sqlite/sqlite_python.htm
    conn = sqlite3.connect("bookings.db")                                                               #connect to database
    if tag == 0:                                                                                        #tag zero represents tickets table
        cursor = conn.execute("SELECT type,adult_cost,child_cost FROM tickets")                         #select tickets table from database
        
        for row in cursor:
            print("Ticket: ", row[0], "\nAdult Cost: ", row[1], "\nChild Cost: ", row[2], "\n \n")      #print ticket details
    elif tag == 1:                                                                                      #tag one represents activity table
        cursor =  conn.execute("SELECT type,adult_cost,child_cost FROM activity")                       #select activity table from database
        
        for row in cursor:
            print("Activity: ", row[0], "\nAdult Cost: ", row[1], "\nChild Cost: ", row[2], "\n \n")    #print activity details

    conn.close()                                                                                        #close connection

def server(tag):
    '''server connects to the tcpserver to calculate cost
        with tag indicating what cost is being calculated.
        tag zero represents tickets table and 
        tag one represents activity table'''
    cost = 0                                                                #initialise cost as zero     
    while cost == 0:                                                        #while cost is zero
        data = input("What are you booking? ")                              #request user booking 
        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            sock.connect((HOST, PORT))
            sock.sendall(bytes(data + "\n"+str(tag), "utf-8"))              #send to tcpserver with tag appended

            # Receive data from the server 
            text = str(sock.recv(1024), "utf-8")                            #receive booking information
            cost = float(sock.recv(1024))                                   #receive cost
            print(text)                                                     #print booking information
    return cost                                                             #return cost
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    main()


