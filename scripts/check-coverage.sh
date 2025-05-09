#!/bin/bash

# Generated by chatgpt: https://chatgpt.com/share/67cf5f81-5500-8006-894a-7f8403fcc0f5

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <coverage_report_file>"
    exit 1
fi

coverage_file="$1"

if [ ! -f "$coverage_file" ]; then
    echo "Error: File '$coverage_file' not found!"
    exit 1
fi

total_coverage=$(grep -E 'TOTAL' "$coverage_file" | awk '{print $NF}' | tr -d '%')

if [ -z "$total_coverage" ]; then
    echo "Error: Could not extract total coverage. Check the report format."
    exit 1
fi

if [ "$total_coverage" -ge 80 ]; then
	echo "Coverage is sufficient: ${total_coverage}% >= 80% (PASS)"
    exit 0
else
	echo "Coverage is too low: ${total_coverage}% < 80% (FAIL)"
    exit 1
fi

