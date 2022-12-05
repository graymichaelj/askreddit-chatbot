from transformers import AutoTokenizer, AutoModelWithLMHead
from torch.utils.data import RandomSampler
from transformers import (
    AdamW,
    Adafactor,
    T5ForConditionalGeneration,
    T5Tokenizer,
    T5Config,
    get_linear_schedule_with_warmup
)
from pathlib import Path
import string
from nlp import load_metric
from pytorch_lightning.loggers import WandbLogger
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
import torch
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
from flask import Flask, render_template, request
import argparse
import glob
import os
import json
import time
import logging
import random
import re
from itertools import chain
from string import punctuation
import nltk
nltk.download('punkt')

tokenizer = T5Tokenizer.from_pretrained("model")
# config = T5Config.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained(
    'model')
model.eval()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    res = getResponse(msg, model)


def getResponse(msg, model):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    preprocess_text = msg.strip().replace("\n", "")
    tokenized_text = tokenizer.encode(
        preprocess_text, return_tensors="pt").to(device)
    model = model.to(device)

    outs = model.generate(
        tokenized_text,
        max_length=100,
        num_beams=2,
        early_stopping=True
    )
    resp = [tokenizer.decode(ids) for ids in outs]

    return resp


if __name__ == '__main__':
    app.run()
