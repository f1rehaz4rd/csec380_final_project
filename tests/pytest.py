#!/bin/python3
import pytest
import requests

assert requests.get("localhost").status_code == 200