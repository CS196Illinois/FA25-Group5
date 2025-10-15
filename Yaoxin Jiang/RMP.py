import requests
import re
import json

def getRMP(professor_full_name: str) -> float:
  url = "https://www.ratemyprofessors.com/search/professors/1112?q=" + professor_full_name
  
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }
  
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    return None

  match = re.search(r'window\.__RELAY_STORE__ = (.*?);', response.text)
  if not match:
    print("Could not find professor data on the page.")
    return None

  try:
    data = json.loads(match.group(1))
  except json.JSONDecodeError:
    print("Failed to parse JSON data.")
    return None

  for key, value in data.items():
    if isinstance(value, dict) and value.get('__typename') == 'Teacher':
      first_name = value.get('firstName', '')
      last_name = value.get('lastName', '')
      
      if f"{first_name} {last_name}".lower() == professor_full_name.lower():
        avg_rating = value.get('avgRating')
        if avg_rating is not None:
          # Return the float value directly
          return avg_rating
          
  return None

# Example of how to use the function
print(getRMP("Dunfield, Nathan"))

def getRMPfuzzy(professor_full_name: str) -> float:
  url = "https://www.ratemyprofessors.com/search/professors/1112?q=" + professor_full_name
  
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }
  
  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    return None

  match = re.search(r'window\.__RELAY_STORE__ = (.*?);', response.text)
  if not match:
    print("Could not find professor data on the page.")
    return None

  try:
    data = json.loads(match.group(1))
  except json.JSONDecodeError:
    print("Failed to parse JSON data.")
    return None

  for key, value in data.items():
    if isinstance(value, dict) and value.get('__typename') == 'Teacher':
      avg_rating = value.get('avgRating')
      if avg_rating is not None:
          # Return the float value directly
        return avg_rating
          
  return None

# Example of how to use the function
print(getRMPfuzzy("Nathan D"))