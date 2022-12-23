from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ray
from ray import serve
from typing import Any, Union, Dict
from src.deployments import azure_deployment,detectron_deployment
from ray.serve.drivers import DAGDriver
from ray.serve.deployment_graph import InputNode
import logging
import sys
from ray.serve.http_adapters import json_request,image_to_ndarray



logging.basicConfig(
    format="{asctime} {name} {levelname:4s}: {message}",
    style="{",
    stream=sys.stdout,
    level=logging.INFO,
)

log = logging.getLogger()
log.info("Starting server")

# # disable logging from modules
for name in logging.Logger.manager.loggerDict.keys():
    if (
        ("sklearn" in name)
        or ("torch" in name)
        or ("s3transfer" in name)
        or ("boto3" in name)
        or ("botocore" in name)
        or ("nose" in name)
        or ("multipart" in name)
        or ("urllib3" in name)
        or ("msrest" in name)
        or ("uvicorn" in name)
    ):
        logging.getLogger(name).setLevel(logging.CRITICAL)

MODEL_VERSION = "1.2"


@serve.deployment()
class HealthDeployment():
    async def forward(self) -> str:
        return "Server is healthy"

@serve.deployment
async def read_file(input):
    print("Input is --> {}".format(input))
    form = await input.form()
    print("form is --> {}".format(form))
    contents = await form['img'].read()
    return contents

@serve.deployment
def aggregate(ocr_resp,detectron_output):
    return {
        "ocr":ocr_resp,
        "detectron":detectron_output
    }

health_deployment = HealthDeployment.bind()

with InputNode() as input_file:
    print(f"input file is :: {input_file}")
    health_response = health_deployment.forward.bind()
    dag = aggregate.bind(azure_deployment.forward.bind(input_file),detectron_deployment.forward.bind(input_file))


serve_dag = DAGDriver.options(num_replicas=1).bind({
    "/process":dag,
    "/health": health_response
})



