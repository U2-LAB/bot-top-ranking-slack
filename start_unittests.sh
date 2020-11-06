#!/bin/bash
coverage run -m unittest discover -s tests/unittest
coverage report -m
