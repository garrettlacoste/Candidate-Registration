from pymongo import MongoClient
import CandidateModule
from typing import List, Optional
from pymongo import MongoClient, errors
from main import uri


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
