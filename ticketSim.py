import sys
import os
import random

def main(argv):
    if(len(argv) != 2):
        print("Invalid args!\nticketSim.py [# hours to simulate]")
        exit()

    numHours = int(argv[1])

    simulate(User(1), NUM_SERVICES, TICKET_LENGTH_MINUTES, REQUEST_LAMBDA, numHours*60)

    #for i in range(0,NUM_USERS):
    #    HELLO = 1


class User:
    tickets = {}

    def __init__(self, userID):
        self.userID = userID

    def requestService(self, serviceID, ticketDuration):
        if(serviceID in self.tickets):
            #do nothing
            print("Already have ticket for service " + str(serviceID))
        else:
            #add ticket
            self.tickets[serviceID] = Ticket(serviceID, ticketDuration)
            print("Added a new ticket for service "  + str(serviceID) + " with duration " + str(ticketDuration))

    def decrementTickets(self, amount):
        for serviceID,ticket in self.tickets.copy().items():
            if(self.tickets[serviceID].decrementTicket(amount)):
                #ticket expired
                print("Ticket expired for service " + str(ticket.getServiceID()))
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

    while(currentMinute < duration):
        if(serviceRequested):
            user.decrementTickets(minutesToRequest)
            user.requestService(serviceToRequest, ticketDuration)

        minutesToRequest = int(random.expovariate(requestLambda))
        serviceToRequest = random.randint(1,numServices)
        currentMinute += minutesToRequest
        #currentMinute += 1
        serviceRequested = True
        print("Time: " + str(currentMinute))
        #print("User " + str(user.userID) + " requests service " + str(serviceToRequest) + " at time " + str(currentMinute))

    
# constants and python main thing

NUM_SERVICES = 10
NUM_USERS = 100
TICKET_LENGTH_MINUTES = 1
REQUEST_LAMBDA = 0.25

if __name__ == "__main__":
    main(sys.argv)