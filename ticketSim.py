import sys
import os
import random

def main(argv):
    if(len(argv) != 2):
        print("Invalid args!\nticketSim.py [# hours to simulate]")
        exit()

    numHours = int(argv[1])

    if(numHours <= 0):
        print("Invalid args!\nHours must be a positive integer!\nticketSim.py [# hours to simulate]")
        exit()

    ticketsGranted = 0

    for i in range(0,NUM_USERS):
        ticketsGranted += simulate(User(1), NUM_SERVICES, TICKET_LENGTH_MINUTES, REQUEST_LAMBDA, numHours*60)

    print("Total tickets granted: " + str(ticketsGranted))
    print("Average tickets per day: " + format(((ticketsGranted/numHours)*24),'.2f'))
    print("Average tickets per user: " + format((ticketsGranted/NUM_USERS), '.2f'))


class User:
    tickets = {}

    def __init__(self, userID):
        self.userID = userID

    def requestService(self, serviceID, ticketDuration):
        ticketGranted = True
        if(serviceID in self.tickets):
            #do nothing
            #print("Already have ticket for service " + str(serviceID))
            ticketGranted = False
        else:
            #add ticket
            self.tickets[serviceID] = Ticket(serviceID, ticketDuration)
            #print("Added a new ticket for service "  + str(serviceID) + " with duration " + str(ticketDuration))

        return ticketGranted

    def decrementTickets(self, amount):
        for serviceID,ticket in self.tickets.copy().items():
            if(self.tickets[serviceID].decrementTicket(amount)):
                #ticket expired
                #print("Ticket expired for service " + str(ticket.getServiceID()))
                del self.tickets[serviceID]


class Ticket:
    def __init__(self, serviceID, duration):
        self.serviceID = serviceID
        self.duration = duration

    # decrements ticket duration by [amount] minutes
    # if amount reaches zero, return true
    def decrementTicket(self, amount):
        self.duration -= amount
        return (self.duration <= 0)

    def getServiceID(self):
        return self.serviceID
    

def simulate(user, numServices, ticketDuration, requestLambda, duration):
    currentMinute = 0
    serviceRequested = False
    minutesToRequest = 0
    serviceToRequest = 0
    ticketsGranted = 0

    while(currentMinute < duration):
        if(serviceRequested):
            user.decrementTickets(minutesToRequest)
            if(user.requestService(serviceToRequest, ticketDuration)):
                ticketsGranted += 1

        minutesToRequest = int(random.expovariate(requestLambda))
        serviceToRequest = random.randint(1,numServices)
        currentMinute += minutesToRequest
        serviceRequested = True
        #print("Time: " + str(currentMinute))
        
        
    return ticketsGranted

    
# constants and python main thing

NUM_SERVICES = 10
NUM_USERS = 100
TICKET_LENGTH_MINUTES = 30
REQUEST_LAMBDA = 0.25

if __name__ == "__main__":
    main(sys.argv)