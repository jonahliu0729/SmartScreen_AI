#!/bin/bash

# Navigate to your project folder
cd /Users/jonahliu/SmartScreen_AI || exit

# Install dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Run the Streamlit app
streamlit run SmartScreen_AI_Demo_optimized.py

# Keep terminal open if Streamlit stops (optional)
echo "Streamlit app stopped. Press Enter to exit."
read