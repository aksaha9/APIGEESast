#!/bin/bash
JAVA_DIR=$1
OUTPUT=$2
CX_TOKEN=$CX_TOKEN  # Set as env var

# Assuming CxFlow or CxCLI installed
cx scan create --project-name "ApigeeJava" --source $JAVA_DIR --format sarif -o $OUTPUT