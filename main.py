# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Candidate:
    def __init__(self, first_name, last_name, DOB, party, SOC):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.party = party
        self.SOC = SOC

    def getFirstName(self):
        return self.first_name
    def getLastName(self):
        return self.last_name
    def getDOB(self):
        return self.DOB
    def getParty(self):
        return self.party
    def getSOC(self):
        return self.SOC

'''def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.'''



def registerCandidate():

    newFirstName = input("Enter your first name: ")
    newLastName = input("Enter your last name: ")
    newDOB = input("Enter your Date of Birth: ")
    newPolParty = input("Enter your political party: ")
    newSOC = input("Enter your Social Security: ")

    newCandidate = Candidate(newFirstName,newLastName,newDOB,newPolParty,newSOC)
    return newCandidate

def updateCandidate():
    print("Under Construction")
    return

def printCandidates(candidateList):
    for x in range(0,len(candidateList)):
        print("Candidate: " + str(x + 1) + "\n " +
              "------------------------")
        print("Name: " + candidateList[x].getFirstName() + " " + candidateList[x].getLastName())
        print("DOB: " + candidateList[x].getDOB())
        print("Political Party: " + candidateList[x].getParty())
        print("SOC: " + candidateList[x].getSOC() + "\n ")

#code is ran through main.
def main():
    global inMenu
    inMenu = True
    # a dictionary to hold all valid candidates
    candidateList = []
    while(inMenu):
        print("hello welcome to the hotpatchers™ candidate registration system (>^—^)>♡ \n" +
              "Please select one of the following options \n" +
              "1. Register \n" +
              "2. Update information\n" +
              "3. Print candidate list \n" +
              "4. Exit program")
        print("-----------------------")

        userChoice = input("Menu Decision Num: ")
        choiceNum = int(userChoice)

        if choiceNum == 1:
            candidateList.append(registerCandidate())
            pause = input("Candidate registered, press enter to continue:")
        elif choiceNum == 2:
            updateCandidate()
            pause = input("Candidate updated, press enter to continue:")
        elif choiceNum == 3:
            printCandidates(candidateList)
            pause = input("list printed, press enter to continue:")
        elif choiceNum == 4:
            inMenu = False
        else:
            pause = input("invalid input, press enter to continue:")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

