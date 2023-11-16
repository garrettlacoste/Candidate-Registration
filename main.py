from abc import ABC, abstractmethod
from typing import List, Optional
import json
import csv
from pymongo import MongoClient, errors
import os

# FileParsingStrategy interface
class FileParsingStrategy(ABC):
    @abstractmethod
    def parse_file(self, file_path: str) -> List["Candidate"]:
        pass

class FileParsingPolicy:
    def determine_strategy(self, file_path: str) -> Optional[FileParsingStrategy]:
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
class CSVFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                # Assuming the CSV file has a header row
                header = next(csv_reader)
                for row in csv_reader:
                    candidate = Candidate(
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
class JSONFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                json_data = file.read()
                # Assuming the JSON file contains an array of candidates
                candidates_data = json.loads(json_data)
                for candidate_data in candidates_data:
                    candidate = Candidate(
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
class TextFileParser(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        candidates = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    if len(data) == 6:
                        candidate = Candidate(
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
class MongoDBWriter(FileParsingStrategy):
    def parse_file(self, file_path: str) -> List["Candidate"]:
        # Not currently implemented or planned to be implemented
        candidates = []
        return candidates

    def write_candidates_to_mongodb(self, candidates: List["Candidate"]):
        # This method is specifically for writing candidates to MongoDB without reading from a file
        self._write_to_mongodb(candidates)

    def _write_to_mongodb(self, candidates: List["Candidate"]):
        # Implement MongoDB writing logic here
        print("Sending Data to Database:")
        uri = "mongodb+srv://ClayBarr:GenericPassword@candidateregistration.yhgqzoi.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        client = MongoClient(uri)
        try:
            db = client['candidates_db']
            collection = db['candidates']
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
class Candidate:
    def __init__(self, first_name, last_name, DOB, party, SOC, position):
        self.first_name = first_name
        self.last_name = last_name
        self.DOB = DOB
        self.party = party
        self.SOC = SOC
        self.position = position
        self.parser = None  # Added attribute to store the current strategy

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

    def getPosition(self):
        return self.position

    def set_parser(self, parser: FileParsingStrategy):
        self.parser = parser  # Set the current strategy

    def parse_file(self, file_path: str) -> List["Candidate"]:
        if self.parser is not None:
            return self.parser.parse_file(file_path)
        else:
            print("Error: No parser set. Please use set_parser to set a parsing strategy.")
            return []

def main():
    global inMenu
    inMenu = True
    while inMenu:
        print("Hello! Welcome to the Hotpatchers™ Candidate Registration System. (>^—^)>♡ \n" +
              "Please select one of the following options: \n" +
              "1. Register \n" +
              "2. View/Update information\n" +
              "3. Print candidate list \n" +
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
            candidate = Candidate(first_name="John", last_name="Doe", DOB="1990-01-01", party="Independent",
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
            # not implemented
            pause = input("Candidate updated, press enter to continue:")
        elif choiceNum == 3:
            # not implemented
            pause = input("List printed, press enter to continue:")
        elif choiceNum == 4:
            inMenu = False
        else:
            pause = input("Invalid input, press enter to continue:")

if __name__ == "__main__":
    main()
