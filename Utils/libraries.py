from flask import Flask, render_template, url_for, request
import transformers
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from bs4 import BeautifulSoup
import requests

