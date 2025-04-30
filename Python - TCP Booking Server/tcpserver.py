import socketserver
import sqlite3


def handleBooking(data, tag):
    '''handleBooking takes data and tag as input.
        It returns cost and booking information as an array
        tag zero represents tickets table and 
        tag one represents activity table'''
    data = str(data, "utf-8")                                           #turn data from bytes to string
    split_data = data.split()                                           #split data into words and keep as an array
    data_size = len(split_data)                                         #get split_data size
    cost, discount, err =calculateCost(split_data,data_size,tag)        #run calculateCost and get cost discount and error 
    if (data_size == 4 or data_size == 7 or data_size == 10) and err == 0 and tag == 0:             #check if data_size is valid and no error and tag is zero
        text = "\n" + split_data[0]+" your tickets for the Robotics Festival are booked and cost "+str(cost)+". "+discount          #create booking information text
    elif (data_size == 4 or data_size == 7 or data_size == 10) and err == 0 and tag == 1:           #check if data_size is valid and no error and tag is one
        text = "\nYour activities for the Robotics Festival are booked and cost "+str(cost)+"."     #create booking information text
    else:
        text = "Incorrect format"                                       #create text as error

    arr = [bytes(text + "\n", "utf-8"),bytes(str(cost),"utf-8")]        #create array of booking information and cost
    return arr                                                          #return arr
    

def calculateCost(split_data,data_size,tag):
    '''calculateCost takes an array of booking request
        it's size and the tag indicating whether it's for tickets or activity table.
        tag zero represents tickets table and 
        tag one represents activity table'''
    
    conn = sqlite3.connect("bookings.db")                   #connect to bookings database
    tick = 1                                                #set tick to 1
    cost = 0                                                #set cost to 0
    discount = "No discount given"
    err = 0                                                 #set err to 0
    
    while tick<data_size:                                   #while tick is less than data size
        if tag == 0:                                        #if tickets section
            try:
                ac = conn.execute("SELECT adult_cost FROM tickets WHERE type=?",(split_data[tick],))    #select the adult cost of ticket bought
                ac = [row for row in ac]
                cc = conn.execute("SELECT child_cost FROM tickets WHERE type=?",(split_data[tick],))    #select the child cost of ticket bought
                cc = [row for row in cc]
                cost += (ac[0][0]*int(split_data[tick+1])) + (cc[0][0]*int(split_data[tick+2]))         #multiply the costs by the quantity and add them to cost
                tick += 3                                                                               #add 3 to tick
            except:
                err = 1                                     #if error set err to be 1
                break
        elif tag == 1:
            try:
                ac = conn.execute("SELECT adult_cost FROM activity WHERE type=?",(split_data[tick],))   #select the adult cost of activity bought
                ac = [row for row in ac]
                cc = conn.execute("SELECT child_cost FROM activity WHERE type=?",(split_data[tick],))   #select the child cost of activity bought
                cc = [row for row in cc]
                cost += (ac[0][0]*int(split_data[tick+1])) + (cc[0][0]*int(split_data[tick+2]))         #multiply the costs by the quantity and add them to cost
                tick += 3                                                                               #add 3 to tick
            except:
                err = 1                                     #if error set err to be 1
                break
        
    if cost>500 and tag == 0:                               #if cost is greater than 500 and tag is 0 representing tickets section
        discount = "10% discount given"                     #change discount value
        cost -= cost*(10/100)                               #subtract discount from cost

    conn.close()                                            #close connection
    return round(cost,2), discount, err                     #return cost, discount and err
    

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        tag = int(chr(self.data[-1]))                           #take tag from the end of the booking request text
        self.data = self.data[0:-1]                             #strip tag from booking request
        print(self.data)
        new_data = handleBooking(self.data,tag)                 #run handleBooking to get booking information and cost
        self.request.sendall(new_data[0])                       #send booking information
        self.request.sendall(new_data[1])                       #send cost

    
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
