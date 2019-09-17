#!/bin/python3
import pytest
import requests

assert "Hello World" in requests.get("http://localhost").content