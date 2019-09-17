#!/bin/python3
import pytest
import requests

assert requests.get("localhost:1337").status_code == 200