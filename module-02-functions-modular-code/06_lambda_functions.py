#Celsius to Fahrenheit Converter Lambda Function
celcius = 0
print((lambda celsius: (celsius * 9/5) + 32)(celcius))  # 32.0

# Passing new numbers directly
print((lambda celsius: (celsius * 9/5) + 32)(100))      # 212.0
print((lambda celsius: (celsius * 9/5) + 32)(37))       # 98.6


#LLM response ranker
responses = [
    {"model": "claude-3-5", "tokens": 320, "quality_score": 0.94},
    {"model": "gpt-4o",     "tokens": 415, "quality_score": 0.91},
    {"model": "gemini-pro", "tokens": 280, "quality_score": 0.87},
]

sorted_resp = sorted(responses, key = lambda x: x["quality_score"], reverse = True)

for response in sorted_resp:
    print(response)
