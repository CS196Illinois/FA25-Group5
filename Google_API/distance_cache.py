"""
Distance Cache Manager for Google Distance Matrix API
This module handles caching of walking distances between buildings to minimize API usage
"""

import csv
import os
from typing import Optional, Dict, Tuple, List
import googlemaps

# Global cache dictionary
DISTANCE_CACHE: Dict[Tuple[str, str], float] = {}
CACHE_FILE = "building_distances_cache.csv"


def get_all_unique_buildings(csv_path: str) -> List[str]:
    """
    Extract all unique buildings from the course CSV file

    Args:
        csv_path: Path to the course CSV file

    Returns:
        Sorted list of unique building names with ", Urbana, IL" suffix
    """
    buildings = set()

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

        for idx, row in enumerate(rows[1:], start=1):  # Skip header
            try:
                building = row[17]  # Column 17 is Building
                start_time = row[13]  # Column 13 is Start Time

                # Skip online/arranged courses
                if start_time != "ARRANGED" and building.strip():
                    # Add ", Urbana, IL" suffix for consistency
                    full_building = building if ", IL" in building else building + ", Urbana, IL"
                    buildings.add(full_building)
            except:
                continue

    return sorted(list(buildings))


def get_walking_time_direct(gmaps: googlemaps.Client, origin: str, destination: str) -> Optional[float]:
    """
    Make a direct API call to get walking time between two locations

    Args:
        gmaps: Google Maps client
        origin: Starting location
        destination: Ending location

    Returns:
        Walking time in minutes, or None if error
    """
    try:
        response = gmaps.distance_matrix(
            origins=[origin],
            destinations=[destination],
            mode="walking",
            departure_time="now"
        )

        info = response['rows'][0]['elements'][0]
        if info['status'] == 'OK':
            seconds = info['duration']['value']
            minutes = seconds / 60
            return round(minutes, 2)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_distance_cache(
    csv_path: str,
    gmaps: googlemaps.Client,
    cache_file: str = CACHE_FILE
) -> None:
    """
    ONE-TIME FUNCTION: Generate all pairwise walking times and save to CSV

    This will make approximately (N * (N-1) / 2) API calls where N is number of unique buildings.
    For 109 buildings, this is about 5,886 API calls.

    Args:
        csv_path: Path to the course CSV file
        gmaps: Google Maps client with API key
        cache_file: Path to save the cache file
    """
    print("=" * 60)
    print("DISTANCE CACHE GENERATOR")
    print("=" * 60)

    print("\nExtracting unique buildings from course data...")
    buildings = get_all_unique_buildings(csv_path)

    num_buildings = len(buildings)
    total_calls = num_buildings * (num_buildings - 1) // 2

    print(f"\nFound {num_buildings} unique buildings:")
    for i, building in enumerate(buildings, 1):
        print(f"  {i}. {building}")

    print(f"\n{'=' * 60}")
    print(f"Total API calls needed: {total_calls}")
    print(f"Estimated cost: ${total_calls * 0.005:.2f} (at $0.005 per call)")
    print(f"Estimated time: {total_calls * 0.5 / 60:.1f} minutes (at 0.5 sec per call)")
    print(f"{'=' * 60}")

    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return

    print(f"\nGenerating distance cache and saving to '{cache_file}'...")
    print("This may take a while!\n")

    # Open CSV file for writing
    with open(cache_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['origin', 'destination', 'minutes'])

        call_count = 0
        errors = 0

        # Calculate distance for each unique pair
        for i, origin in enumerate(buildings):
            for j, destination in enumerate(buildings):
                if i >= j:  # Skip diagonal and duplicate pairs
                    continue

                call_count += 1

                # Progress indicator
                if call_count % 10 == 0 or call_count == 1:
                    print(f"Progress: [{call_count}/{total_calls}] ({call_count/total_calls*100:.1f}%)")

                # Make API call
                minutes = get_walking_time_direct(gmaps, origin, destination)

                if minutes is not None:
                    # Write both directions (A->B and B->A are the same)
                    writer.writerow([origin, destination, minutes])
                    writer.writerow([destination, origin, minutes])
                else:
                    errors += 1
                    print(f"  ⚠ ERROR: {origin} -> {destination}")
                    writer.writerow([origin, destination, 'ERROR'])
                    writer.writerow([destination, origin, 'ERROR'])

                # Flush every 10 calls to save progress
                if call_count % 10 == 0:
                    file.flush()

    print(f"\n{'=' * 60}")
    print("✓ Cache generation complete!")
    print(f"{'=' * 60}")
    print(f"Saved to: {cache_file}")
    print(f"Total API calls made: {call_count}")
    print(f"Successful: {call_count - errors}")
    print(f"Errors: {errors}")


def load_distance_cache(cache_file: str = CACHE_FILE) -> bool:
    """
    Load the distance cache from CSV file into memory

    Args:
        cache_file: Path to the cache file

    Returns:
        True if successfully loaded, False otherwise
    """
    global DISTANCE_CACHE
    DISTANCE_CACHE = {}

    if not os.path.exists(cache_file):
        print(f"⚠ Warning: Cache file '{cache_file}' not found!")
        print(f"Run generate_distance_cache() first to create it.")
        return False

    with open(cache_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            origin = row['origin']
            destination = row['destination']
            minutes = row['minutes']

            # Store in cache (use tuple as key)
            if minutes != 'ERROR':
                DISTANCE_CACHE[(origin, destination)] = float(minutes)

    print(f"✓ Loaded {len(DISTANCE_CACHE)} distance pairs from cache")
    return True


def get_walking_time_cached(
    origin: str,
    destination: str,
    gmaps: Optional[googlemaps.Client] = None
) -> Optional[float]:
    """
    Get walking time between two locations, using cache if available

    Args:
        origin: Starting location
        destination: Ending location
        gmaps: Google Maps client (only needed if cache miss and fallback desired)

    Returns:
        Walking time in minutes, or None if not found
    """
    # Normalize location strings (add suffix if missing)
    if ", IL" not in origin:
        origin = origin + ", Urbana, IL"
    if ", IL" not in destination:
        destination = destination + ", Urbana, IL"

    # Check cache first
    cache_key = (origin, destination)
    if cache_key in DISTANCE_CACHE:
        return DISTANCE_CACHE[cache_key]

    # If not in cache and gmaps client provided, make API call
    if gmaps is not None:
        print(f"⚠ Cache miss: {origin} -> {destination}")
        print(f"  Making API call...")
        minutes = get_walking_time_direct(gmaps, origin, destination)

        # Store in cache for future use
        if minutes is not None:
            DISTANCE_CACHE[cache_key] = minutes
            DISTANCE_CACHE[(destination, origin)] = minutes  # Symmetric

        return minutes

    # Not in cache and no fallback available
    print(f"⚠ Not found in cache: {origin} -> {destination}")
    return None


def get_cache_stats(cache_file: str = CACHE_FILE) -> Dict:
    """
    Get statistics about the cache file

    Returns:
        Dictionary with cache statistics
    """
    if not os.path.exists(cache_file):
        return {"exists": False}

    total = 0
    errors = 0

    with open(cache_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total += 1
            if row['minutes'] == 'ERROR':
                errors += 1

    # Divide by 2 because each pair is stored twice (A->B and B->A)
    unique_pairs = total // 2

    return {
        "exists": True,
        "total_entries": total,
        "unique_pairs": unique_pairs,
        "errors": errors,
        "success_rate": (total - errors) / total * 100 if total > 0 else 0
    }


if __name__ == "__main__":
    # Example usage
    print("Distance Cache Manager")
    print("=" * 60)
1
    stats = get_cache_stats()
    if stats["exists"]:
        print(f"Cache file exists: {CACHE_FILE}")
        print(f"Unique building pairs: {stats['unique_pairs']}")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Errors: {stats['errors']}")
        print(f"Success rate: {stats['success_rate']:.1f}%")
    else:
        print(f"No cache file found at: {CACHE_FILE}")
        print("Run generate_distance_cache() to create it")
