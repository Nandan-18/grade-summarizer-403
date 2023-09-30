#!/usr/bin/env bash

# Load environment variables from .env file
if [[ -f .env ]]; then
    source .env
else
    echo "Error: .env file not found."
    exit 1
fi

# Check if COURSE is set to CMPUT 403
if [[ "$COURSE" == "403" ]]; then
    # Check if SEMINAR and PROJECT are set
    if [[ -z "$SEMINAR" || -z "$PROJECT" ]]; then
        echo "Error: SEMINAR and PROJECT must be set in .env file when COURSE=403."
        exit 1
    fi

    # Pass SEMINAR and PROJECT as arguments
    python3 main.py "$USERNAME" "$PASSWORD" "cmput$COURSE.txt" "$SEMINAR" "$PROJECT" > result.txt
else
    # Pass only the required arguments (without SEMINAR and PROJECT)
    python3 main.py "$USERNAME" "$PASSWORD" "cmput$COURSE.txt" > result.txt
fi