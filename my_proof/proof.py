import json
import logging
import os
from typing import List, Dict, Any
from my_proof.models.proof_response import ProofResponse
from my_proof.checks import SolutionValidator

class Proof:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        logging.info(f"Config: {self.config}")
        self.proof_response = ProofResponse(dlp_id=config['dlp_id'])

    def generate(self) -> ProofResponse:
        print("Starting generate method")
        input_data = ''
        for input_filename in os.listdir(self.config['input_dir']):
            input_file = os.path.join(self.config['input_dir'], input_filename)
            print(f"Reading file: {input_file}")
            with open(input_file, 'r') as f:
                input_data = json.load(f)

        solution_validation = SolutionValidator(self.config)

        validation_result = solution_validation.validate(input_data)
        print(f"Validation result: {validation_result}")
        self.proof_response.score = validation_result['average_score']
        self.proof_response.quality = self.proof_response.score
        self.proof_response.ownership = 1.0
        self.proof_response.authenticity = 1.0
        self.proof_response.uniqueness = 1.0
        self.proof_response.valid = True 
        
        # if self.proof_response.score < 3:
        #     self.proof_response.valid = False
        #     self.proof_response.score = 0.0
        #     return self.proof_response

        print(f"Final proof response: {self.proof_response.__dict__}")
        return self.proof_response
