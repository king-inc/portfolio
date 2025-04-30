import itertools
import sqlite3

def handleBooking(data):
    split_data = data.split()
    data_size = len(split_data)
    print(split_data)
    cost, discount, err =calculateCost(split_data,data_size)
    if (data_size == 4 or data_size == 7 or data_size == 10) and err == 0:
        text = split_data[0]+" your tickets for the Robotics Festival are booked and cost "+str(cost)+". "+discount
    else:
        text = "Incorrect format"
    print(text)



def calculateCost(split_data,data_size):
    conn = sqlite3.connect("bookings.db")
    tick = 1
    cost = 0
    discount = "No discount given"
    err = 0
    while tick<data_size:
        try:
            ac = conn.execute("SELECT adult_cost FROM tickets WHERE type=?",(split_data[tick],))
            ac = [row for row in ac]
            cc = conn.execute("SELECT child_cost FROM tickets WHERE type=?",(split_data[tick],))
            cc = [row for row in cc]
            cost += (ac[0][0]*int(split_data[tick+1])) + (cc[0][0]*int(split_data[tick+2]))
            tick += 3
        except:
            err = 1
            break

    if cost>500:
        discount = "10% discount given"
        cost -= cost*(10/100)

    conn.close()
    return round(cost,2), discount, err
            
handleBooking("Increase VIP 3 2 Weekend 7 5")
