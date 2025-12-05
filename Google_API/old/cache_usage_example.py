"""
Example: How to use the distance caching system

STEP 1: Run this script ONCE to generate the cache (costs API calls)
STEP 2: Use the cached distances in your notebook (no more API calls!)
"""

import googlemaps
from distance_cache import (
    generate_distance_cache,
    load_distance_cache,
    get_walking_time_cached,
    get_cache_stats
)

# Your API key
API_KEY = "AIzaSyDKfrpFNE6saT16tngJPH4MQTAgQNk6zN8"
gmaps = googlemaps.Client(key=API_KEY)

# Path to your course CSV
CSV_PATH = "1101-modified+RMP-2025-sp.csv"


def step1_generate_cache():
    """
    STEP 1: Generate the cache (run this ONCE)

    This will:
    - Extract all unique buildings from your 109 courses
    - Calculate walking time between every pair
    - Save results to 'building_distances_cache.csv'

    For 109 courses, this will make approximately 5,886 API calls
    Cost: ~$29.43 (at $0.005 per call)
    Time: ~50 minutes
    """
    print("STEP 1: Generating distance cache\n")
    generate_distance_cache(CSV_PATH, gmaps)


def step2_use_cache():
    """
    STEP 2: Use the cache (run this every time you need distances)

    After generating the cache once, you can use it unlimited times
    with NO additional API calls!
    """
    print("STEP 2: Using the cache\n")

    # Load the cache into memory
    if not load_distance_cache():
        print("Error: Cache not found. Run step1_generate_cache() first!")
        return

    # Now you can get walking times instantly from the cache
    print("\nExample lookups:")

    origin = "Siebel Center for Computer Science, Urbana, IL"
    destination = "Grainger Engineering Library, Urbana, IL"

    minutes = get_walking_time_cached(origin, destination)
    print(f"{origin}")
    print(f"  -> {destination}")
    print(f"  = {minutes} minutes\n")

    # Another example
    origin2 = "Illini Union, Urbana, IL"
    destination2 = "English Building, Urbana, IL"

    minutes2 = get_walking_time_cached(origin2, destination2)
    print(f"{origin2}")
    print(f"  -> {destination2}")
    print(f"  = {minutes2} minutes")


def check_cache_status():
    """Check if cache exists and show statistics"""
    print("=" * 60)
    print("CACHE STATUS")
    print("=" * 60)

    stats = get_cache_stats()

    if stats["exists"]:
        print("✓ Cache file exists")
        print(f"  Unique building pairs: {stats['unique_pairs']}")
        print(f"  Total entries: {stats['total_entries']}")
        print(f"  Errors: {stats['errors']}")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        print("\nYou can use the cache! No more API calls needed.")
    else:
        print("✗ Cache file does not exist")
        print("\nRun step1_generate_cache() to create it.")

    print("=" * 60)


if __name__ == "__main__":
    # First, check if cache exists
    check_cache_status()

    print("\n")
    print("=" * 60)
    print("WHAT TO DO:")
    print("=" * 60)
    print()

    # Check if cache exists
    stats = get_cache_stats()

    if not stats["exists"]:
        print("1. Run step1_generate_cache() to generate the cache (ONE TIME ONLY)")
        print("   This will cost API calls but you only need to do it once!")
        print()
        print("2. Then you can use get_walking_time_cached() unlimited times")
        print("   with NO additional API calls")
        print()
        print("To generate cache, uncomment and run:")
        print(">>> step1_generate_cache()")
    else:
        print("✓ Cache already exists!")
        print()
        print("You can now use get_walking_time_cached() in your notebook")
        print("Example:")
        print(">>> from distance_cache import load_distance_cache, get_walking_time_cached")
        print(">>> load_distance_cache()")
        print(">>> minutes = get_walking_time_cached('Building A, Urbana, IL', 'Building B, Urbana, IL')")
        print()
        print("To see example usage:")
        print(">>> step2_use_cache()")
