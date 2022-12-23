from ray import serve
import os
import time
import logging
import numpy as np
import cv2
import traceback
import json

log = logging.getLogger(__name__)

@serve.deployment()
class DetectronDeployment:
    def __init__(self):
        pass


    async def forward(self,uploaded_file):
        start_time = time.time()
        resp = {
            "detection values":[1,2,3,4,5]
        }
        log.info("Time taken to analyze image :: {}".format(time.time() - start_time))
        return resp


detectron_deployment = DetectronDeployment.bind()
