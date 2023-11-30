from abc import ABC, abstractmethod
from typing import List, Optional
import json
import csv
from pymongo import MongoClient, errors
from bson import ObjectId
import os
import CandidateModule
# FileParsingStrategy interface


class FileParsingPolicy:
    def determine_strategy(self, file_path: str) -> Optional[CandidateModule.FileParsingStrategy]:
        file_extension = file_path.split('.')[-1].lower()

        if file_extension == 'csv':
            return CSVFileParser()
        elif file_extension == 'json':
            return JSONFileParser()
        elif file_extension == 'txt':
            return TextFileParser()
        else:
            print(f"Unsupported file type: {file_extension}")
            return None

# Concrete strategy for CSV files
class CSVFileParser(CandidateModule.FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Assuming the CSV file has a header row
                header = next(csv_reader)
                for row in csv_reader:
                    candidate = CandidateModule.Candidate(
                        first_name=row[0],
                        last_name=row[1],
                        DOB=row[2],
                        party=row[3],
                        SOC=row[4],
                        position=row[5]
                    )
                    candidates.append(candidate)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return candidates

# Concrete strategy for JSON files
class JSONFileParser(CandidateModule.FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                json_data = file.read()
                # Assuming the JSON file contains an array of candidates
                candidates_data = json.loads(json_data)
                for candidate_data in candidates_data:
                    candidate = CandidateModule.Candidate(
                        first_name=candidate_data.get('first_name', ''),
                        last_name=candidate_data.get('last_name', ''),
                        DOB=candidate_data.get('DOB', ''),
                        party=candidate_data.get('party', ''),
                        SOC=candidate_data.get('SOC', ''),
                        position=candidate_data.get('position', '')
                    )
                    candidates.append(candidate)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_path}")
        return candidates

# Concrete strategy for text files
class TextFileParser(CandidateModule.FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        candidate = CandidateModule.Candidate(
                            first_name=data[0],
                            last_name=data[1],
                            DOB=data[2],
                            party=data[3],
                            SOC=data[4],
                            position=data[5]
                        )
                        candidates.append(candidate)
                    else:
                        print(f"Invalid data format in line: {line}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return candidates

# Concrete strategy for MongoDB writing
class MongoDBWriter(CandidateModule.FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        # Not currently implemented or planned to be implemented
        candidates = []
        return candidates

    def write_candidates_to_mongodb(self, candidates: List["Candidate"]):
        # This method is specifically for writing candidates to MongoDB without reading from a file
        self._write_to_mongodb(candidates)

    def _write_to_mongodb(self, candidates: List["Candidate"]):
        # Implement MongoDB writing logic here
        client = MongoClient(uri)
        db = client['candidates_db']
        collection = db['candidates']
        print("Sending Data to Database:")
        try:
            for candidate in candidates:
                data = {
                    "first_name": candidate.getFirstName(),
                    "last_name": candidate.getLastName(),
                    "DOB": candidate.getDOB(),
                    "party": candidate.getParty(),
                    "SOC": candidate.getSOC(),
                    "position": candidate.getPosition()
                }
                result = collection.insert_one(data)
                # Retrieve the generated MongoDB _id and store it in cand_ID
                print(result.inserted_id, " Remember this as your id")
        except errors.PyMongoError as e:
            print(f"Error writing to MongoDB: {e}")
        finally:

            client.close()



# Context class (Candidate) using the strategy


def CanidateUpdate():
    client = MongoClient(uri)
    db = client['candidates_db']
    collection = db['candidates']
    userCandidateID = input("Please enter your candidate ObjectID: ")
    userUpdateMenu = True
    try:
        while (userUpdateMenu):
            # gets current canididate with user input
            currentInfo = collection.find({"_id": ObjectId(userCandidateID)})

            # im sure theres probably a better way to get each individual information but
            # with my current mongoDB knowledge this will be the best i can do
            currentFName = currentInfo.distinct("first_name")
            currentLName = currentInfo.distinct("last_name")
            currentDOB = currentInfo.distinct("DOB")
            currentParty = currentInfo.distinct("party")
            currentSOC = currentInfo.distinct("SOC")
            currentPos = currentInfo.distinct("position")

            currentDict = {"First Name: ":currentFName, "Last Name: ":currentLName,
                           "DOB: ":currentDOB, "Party: ":currentParty, "SOC: ":currentSOC,
                           "POS: ":currentPos}
            submenuCounter = 0
            for x in currentDict.keys():
                submenuCounter = submenuCounter + 1
                print(str(submenuCounter) + ": " + x + str(currentDict[x]))
            print("7: Leave Update Menu \n")

            submenuChoice = input("Please select the number corresponding with the data you wish to update. ")
            if int(submenuChoice) == 7:
                userUpdateMenu = False
            else:
                updateMenuChoice(int(submenuChoice),userCandidateID)

        client.close()


    except:
        print("ID does not exist")
    return

def updateMenuChoice(choiceNum, currentID):
    client = MongoClient(uri)
    db = client['candidates_db']
    collection = db['candidates']
    if choiceNum == 1:
        changeInput = input("What do you want to change your first name to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"first_name":changeInput}})
    elif choiceNum == 2:
        changeInput = input("What do you want to change your last name to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"last_name":changeInput}})
    elif choiceNum == 3:
        changeInput = input("What do you want to change your date of birth to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"DOB":changeInput}})
    elif choiceNum == 4:
        changeInput = input("What do you want to change your party to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"party":changeInput}})
    elif choiceNum == 5:
        changeInput = input("What do you want to change your social security to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"SOC":changeInput}})
    elif choiceNum == 6:
        changeInput = input("What do you want to change your position to: ")
        collection.update_one({"_id":ObjectId(currentID)}, {"$set":{"position":changeInput}})
    client.close()


# ...

def deleteCandidate():
    client = MongoClient(uri)
    db = client['candidates_db']
    collection = db['candidates']
    userCandidateID = input("Please enter your candidate ObjectID: ")
    try:
        currentInfo = collection.find_one({"_id": ObjectId(userCandidateID)})
        if currentInfo:
            print("Are you sure you want to delete " + currentInfo.get("first_name", "") + " " + currentInfo.get("last_name", ""))
            choice = input("Please Put In The Number of Your Option\n"
                           "1.Yes\n"
                           "2.No\n")
            if choice == "1":
                collection.delete_one({"_id": ObjectId(userCandidateID)})
                print("Candidate deleted.")
            elif choice == "2":
                print("Deletion canceled.")
        else:
            print("ID Does Not Exist")
    except Exception as e:
        print(f"An error occurred: {e}")
    client.close()

    return




#initializes db at start of program
uri = "mongodb+srv://ClayBarr:GenericPassword@candidateregistration.yhgqzoi.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client['candidates_db']
collection = db['candidates']


def main():
    global inMenu
    inMenu = True
    while inMenu:
        print("Hello! Welcome to the Hotpatchers™ Candidate Registration System. (>^—^)>♡ \n" +
              "Please select one of the following options: \n" +
              "1. Register \n" +
              "2. View/Update information\n" +
              "3. Delete A Candidate's Information \n" +
              "4. Exit program")
        print("-----------------------")
        userChoice = input("Menu Decision Num: ")
        choiceNum = int(userChoice)

        if choiceNum == 1:
            file_name = input("Please input the exact file location for your candidate form: ")
            file_name = file_name.replace('"', '')
            print(file_name)
            assert os.path.isfile(file_name),f"File not found: {file_name}"
            csv_parser = CSVFileParser()
            json_parser = JSONFileParser()
            mongodb_writer = MongoDBWriter()
            txt_parser = TextFileParser()
            candidate = CandidateModule.Candidate(first_name="K", last_name="T", DOB="1990-01-01", party="Independent",
                                  SOC="123-45-6789", position="Senator")

            # Create an instance of the policy class
            parsing_policy = FileParsingPolicy()
            # Determine the strategy based on the file type
            strategy = parsing_policy.determine_strategy(file_name)

            if strategy:
                # Set the determined strategy for the candidate
                candidate.set_parser(strategy)

                # Parse the file using the determined strategy
                file_data = candidate.parse_file(file_name)
                candidate.set_parser(mongodb_writer)
                # Print the parsed data
                for candidate_data in file_data:
                    print(f"Parsed Data ({file_name}):", candidate_data.getFirstName(), candidate_data.getLastName(),
                          candidate_data.getDOB(), candidate_data.getParty(), candidate_data.getSOC(),
                          candidate_data.getPosition())

                mongodb_writer.write_candidates_to_mongodb(file_data)

            pause = input("Candidate registered, press enter to continue:")
        elif choiceNum == 2:
            CanidateUpdate()
            pause = input("Candidate updated, press enter to continue:")
        elif choiceNum == 3:
            deleteCandidate()
            pause = input("Candidate Deleted Press Enter to Continue")
        elif choiceNum == 4:
            inMenu = False
        else:
            pause = input("Invalid input, press enter to continue:")
        client.close()


if __name__ == "__main__":
    main()