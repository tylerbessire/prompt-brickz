"""
Let's test the new interactive Brickz Builder with Tyler's example
"""

import sys
import os
sys.path.append('/Users/tylerbessire/prompt-bricks-v2')

# Test the enhanced interactive interface
print("🧱 TESTING PROMPT BRICKS V2.0 INTERACTIVE INTERFACE")
print("="*60)

print("\n🎯 Tyler's Example: 'Hey brickz I choose 1 coding. I want to improve the codes stealth abilities and overall performance'\n")

# Simulate the interaction
from prompt_bricks.brickz_builder import BrickzBuilder

builder = BrickzBuilder()

# Step 1: Select coding workpath
print("Step 1: Select workpath")
builder.select_workpath("coding")

# Step 2: Show available bricks
print("\nStep 2: Available bricks for coding")
builder.show_available_bricks()

# Step 3: Add bricks based on Tyler's request
print("\nStep 3: Adding bricks for 'stealth abilities and performance'")
builder.add_bricks(
    style="defensive",        # For stealth/security
    goal="optimize_performance",  # For performance  
    scope="system",          # For overall improvements
    review="security_expert"  # For stealth expertise
)

# Step 4: Sample code
print("\nStep 4: Sample code that needs stealth and performance")
sample_code = '''
import requests
import time

def api_call(url, data):
    response = requests.get(url, params=data)
    return response.json()

def process_data():
    results = []
    for i in range(100):
        data = api_call("https://api.example.com/data", {"id": i})
        results.append(data)
        time.sleep(1)  # Avoid rate limiting
    return results
'''

builder.content = sample_code.strip()

# Step 5: Build the prompt
print("\nStep 5: Building optimized prompt...")
prompt = builder.build_prompt()

print("\n" + "="*80)
print("🎯 GENERATED PROMPT:")
print("="*80)
print(prompt)
print("="*80)

# Step 6: Test two-pass optimization
print("\nStep 6: Testing two-pass PSE optimization...")
optimized = builder.two_pass_optimize()

print("\n" + "="*80)
print("🚀 PSE-OPTIMIZED PROMPT:")
print("="*80)
print(optimized)
print("="*80)

print("\n✅ Interactive Brickz Builder test complete!")
print("Ready for Tyler's 'stealth and performance' use case! 🎯")
