#!/bin/bash
# Example script to demonstrate GitHub Contributions Art

echo "=========================================="
echo "GitHub Contributions Art - Examples"
echo "=========================================="
echo ""

# Example 1: Simple text
echo "Example 1: Generating 'HI'"
python contributions_art.py "HI" ./example_hi

echo ""
echo "Example 2: Generating '2024'"
python contributions_art.py "2024" ./example_2024

echo ""
echo "Example 3: Generating 'CODE'"
python contributions_art.py "CODE" ./example_code

echo ""
echo "=========================================="
echo "Examples completed!"
echo "Check the generated repositories:"
echo "  - ./example_hi"
echo "  - ./example_2024"
echo "  - ./example_code"
echo "=========================================="
