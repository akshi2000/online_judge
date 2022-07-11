from online_judge.celery import app
from .models import *
import time


@app.task(name="compile_and_run", bind=True, max_retries=3)
def compile_and_run(self, submissionId):
    pass


@app.task(name="test", bind=True, max_retries=3)
def test(self):
    time.sleep(5)
