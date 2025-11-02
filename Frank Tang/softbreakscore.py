#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv('../datasets/2025-sp.csv')



# In[11]:


def convert_to_24hour(time_str):
    hours = int(time_str[:2])
    minutes = int(time_str[3:5])
    period = time_str[-2:].upper()
    # Convert to 24-hour format
    if period == "PM" and hours != 12:
        hours += 12
    elif period == "AM" and hours == 12:
        hours = 0

    # Format the result as HH:MM
    return f"{hours:02d}:{minutes:02d}"


# In[ ]:


def get_crn_times(crns):
    if isinstance(crns, str):
        parts = [p.strip() for p in crns.replace(';', ',').split(',') if p.strip()]
        if len(parts) == 1 and ' ' in parts[0]:
            parts = [p for p in parts[0].split() if p.strip()]
        try:
            crn_list = [int(p) for p in parts]
        except ValueError:
            raise ValueError("CRN string must contain integers separated by commas or spaces.")
    elif isinstance(crns, (list, tuple, set)):
        crn_list = [int(x) for x in crns]
    else:
        crn_list = [int(crns)]

    results = []
    for crn in crn_list:
        row = df.loc[df['CRN'] == crn]
        if row.empty:
            results.append((crn, None, None, None))
        else:
            start = convert_to_24hour(row['Start Time'].iloc[0])
            end = convert_to_24hour(row['End Time'].iloc[0]) if 'End Time' in row else None
            days = row['Days of Week'].iloc[0]
            # convert NaN to None
            if pd.isna(start):
                start = None
            if pd.isna(end):
                end = None
            if pd.isna(days):
                days = None
            results.append((crn, start, end, days))
    return results


# In[19]:


def calculate_total_minutes(crns):
    total_minutes = 0
    for crn in crns:
        times = get_crn_times([crn])[0]  # Get time info for this CRN
        _, start, end, days = times

        if start and end and days:  # Only calculate if we have all time information
            # Convert times to minutes since midnight
            start_h, start_m = map(int, start.split(':'))
            end_h, end_m = map(int, end.split(':'))

            start_minutes = start_h * 60 + start_m
            end_minutes = end_h * 60 + end_m

            # Calculate duration for one session
            duration = end_minutes - start_minutes

            # Multiply by number of days per week
            days_count = len(days)

            # Add to total
            total_minutes += duration * days_count

    return total_minutes


# In[ ]:


def collect_soft_preference_intervals(intervals):
    result = []
    for interval in intervals:
        start, end, days = interval
        # Ensure time is in 24-hour format
        def to_24h(t):
            if len(t) == 5 and t[2] == ':':
                return t
            return convert_to_24hour(t)
        start_24 = to_24h(start)
        end_24 = to_24h(end)
        days_clean = ''.join([d for d in days if d in 'MTWRFSU'])
        result.append({'start': start_24, 'end': end_24, 'days': days_clean})
    return result


# In[38]:


def calculate_overlap_minutes(crns, soft_intervals):
    total_overlap = 0

    # Get course times for all CRNs
    course_times = []
    for crn in crns:
        _, start, end, days = get_crn_times([crn])[0]
        if start and end and days:
            course_times.append({'start': start, 'end': end, 'days': days})

    # Convert time string to minutes since midnight
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    # Calculate overlap between two time ranges
    def get_overlap_minutes(start1, end1, start2, end2):
        start1_min = time_to_minutes(start1)
        end1_min = time_to_minutes(end1)
        start2_min = time_to_minutes(start2)
        end2_min = time_to_minutes(end2)

        overlap_start = max(start1_min, start2_min)
        overlap_end = min(end1_min, end2_min)

        return max(0, overlap_end - overlap_start)

    # Check for common days between two day strings
    def has_common_days(days1, days2):
        return any(day in days2 for day in days1)

    # Process soft intervals
    preferred_times = collect_soft_preference_intervals(soft_intervals)

    # Calculate overlaps
    for course in course_times:
        for preferred in preferred_times:
            if has_common_days(course['days'], preferred['days']):
                # Count common days
                common_days = sum(1 for day in course['days'] if day in preferred['days'])

                # Calculate overlap for one day
                overlap_per_day = get_overlap_minutes(
                    course['start'], course['end'],
                    preferred['start'], preferred['end']
                )

                # Add to total (multiply by number of common days)
                total_overlap += overlap_per_day * common_days

    return total_overlap


# In[42]:


# Test case for calculate_overlap_minutes function
test_crns = [69781]  # CRN for AAS 100 AB (MW 2:00 PM - 3:20 PM)
test_soft_intervals = [('14:00', '15:00', 'M')]

overlap = calculate_overlap_minutes(test_crns, test_soft_intervals)
print(f"Overlap minutes for test case: {overlap}")


# In[43]:


def calculate_soft_break_score(crns, soft_intervals):
    total_minutes = calculate_total_minutes(crns)
    overlap_minutes = calculate_overlap_minutes(crns, soft_intervals)
    if total_minutes == 0:
        return None  # Avoid division by zero
    score = 1 - (overlap_minutes / total_minutes)
    return score


# In[56]:


# Test case for calculate_soft_break_score function
test_crns = [69781]  # Example CRN
test_soft_intervals = [('13:00', '15:10', 'M'),('14:00', '14:10', 'W')]

score = calculate_soft_break_score(test_crns, test_soft_intervals)
print(f"Soft break score for test case: {score}")

