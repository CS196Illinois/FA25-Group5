"""
Modified versions of your functions that use the distance cache

Copy these into your notebook to replace the existing functions
"""

import numpy as np
import pandas as pd
from distance_cache import load_distance_cache, get_walking_time_cached


# Load the cache at the start (do this once in your notebook)
# load_distance_cache()


def get_walking_time(origin, destination):
    """
    MODIFIED: Now uses cache instead of making API calls

    This function now checks the cache first. If the distance is cached,
    it returns instantly with NO API call. If not cached, it returns None.
    """
    # Ensure locations have proper suffix
    if ", IL" not in origin:
        origin = origin + ", Urbana, IL"
    if ", IL" not in destination:
        destination = destination + ", Urbana, IL"

    # Get from cache (no gmaps parameter = no fallback API calls)
    minutes = get_walking_time_cached(origin, destination, gmaps=None)

    return minutes


def compute_travel_satisfaction_score(df, schedule_indices, max_acceptable_travel_minutes, generate_detailed_schedule):
    """
    MODIFIED: Uses cached walking times instead of making API calls

    This is your existing function with minimal changes - it now uses the cached
    get_walking_time() function instead of making API calls.

    Parameters:
        df: Your course dataframe
        schedule_indices: List of row indices
        max_acceptable_travel_minutes: Maximum acceptable walking time
        generate_detailed_schedule: Function to generate timespace
    """
    satisfactory = 0
    considered = 0
    timespace = generate_detailed_schedule(schedule_indices)

    # Loop through each day
    for day in range(5):
        current = 0
        # Skip empty slots at start of day
        while current < 90 and timespace[day][current] == 0:
            current += 1

        while current < 90:
            # Skip through current class
            while current < 90 and timespace[day][current] != 0:
                current += 1
            start = current  # Start of break

            # Skip through break between classes
            while current < 90 and timespace[day][current] == 0:
                current += 1
            end = current  # End of break (start of next class)

            if current == 90:
                break  # Reached end of day

            break_minutes = (end - start) * 10

            # Only consider back-to-back classes (break < 30 minutes)
            if break_minutes < 30:
                # Make sure to add "Urbana, IL" to building names
                origin_building = df.loc[timespace[day][start - 1], 'Building']
                destination_building = df.loc[timespace[day][end], 'Building']

                # Add location suffix if not already present
                if ", IL" not in origin_building:
                    origin_building += ", Urbana, IL"
                if ", IL" not in destination_building:
                    destination_building += ", Urbana, IL"

                # Get from cache (NO API CALL!)
                travel_minutes = get_walking_time(origin_building, destination_building)

                if travel_minutes is None:
                    print(f"Warning: Distance not in cache: {origin_building} -> {destination_building}")
                    # Skip this pair - don't count it in the score
                    continue

                considered += 1
                # Check if actual walking time is within user's acceptable range
                if travel_minutes <= max_acceptable_travel_minutes:
                    satisfactory += 1

    # Calculate and return percentage
    if considered == 0:
        return None
    else:
        return satisfactory / considered * 100


# ===== INSTRUCTIONS FOR YOUR NOTEBOOK =====
"""
To use the cache in your notebook:

1. Add this cell at the top (after imports):
   ```
   from distance_cache import load_distance_cache, get_walking_time_cached

   # Load the cache (do this once)
   print("Loading distance cache...")
   if load_distance_cache():
       print("Cache loaded successfully!")
   else:
       print("ERROR: Cache not found. Run cache_usage_example.py first!")
   ```

2. Replace your get_walking_time() function with:
   ```
   def get_walking_time(origin, destination):
       if ", IL" not in origin:
           origin = origin + ", Urbana, IL"
       if ", IL" not in destination:
           destination = destination + ", Urbana, IL"

       return get_walking_time_cached(origin, destination, gmaps=None)
   ```

3. Your compute_travel_satisfaction_score() function will now automatically
   use the cache through the modified get_walking_time()!

4. No changes needed to your other functions!

That's it! Now all your distance lookups use the cache with ZERO API calls.
"""
