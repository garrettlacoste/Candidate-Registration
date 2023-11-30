from abc import ABC, abstractmethod
from typing import List, Optional
import json
import csv
from pymongo import MongoClient, errors
from bson import ObjectId
import os

class FileParsingStrategy(ABC):
    @abstractmethod
    def parse_file(self, file_path: str) -> List["Candidate"]:
        pass

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