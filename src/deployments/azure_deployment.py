from ray import serve
import os
import time
import logging


log = logging.getLogger(__name__)

@serve.deployment()
class AzureDeployment:
    def __init__(self):

        pass

    def forward(self,uploaded_file):
        start_time = time.time()
        time.sleep(0.2)
        resp = {
                "status": "success",
                "status_code": 200,
                "result": {
                    "extracted_data": {
                        "aadhaarNumber": "random number",
                        "dob": " random dob",
                        "gender": "Male",
                        "name": "Random name",
                        "fatherName": "NA",
                        "address": "NA",
                        "docType": "random data"
                    },
                    "image_quality": {
                        "blur": 0,
                        "res": 0.05
                    }
                },
                "version": "1.2"
            }
        log.info("Time taken to analyze image :: {}".format(time.time() - start_time))
        return resp

azure_deployment = AzureDeployment.bind()
