
def generate_schedule(course_list, CRN_list, hard_breaks, soft_preferences):
    """
    generate and rank schedules
    return top 10 schedules
    """

    # generate all valid schedules based on hard preferences
    valid_schedules = hardfilter(hard_breaks, course_list, CRN_list)
    

    # ccore each schedule based on soft preferences
    scored_schedules = score_schedules(soft_preferences)

    #return top 10
    top_schedules = sorted(scored_schedules, key=lambda x: x['score'], reverse=True)[:10]

    return top_schedules


# def generate_valid_schedules(course_list, CRN_list, hard_breaks):
#     """
#     Hard preferences
#     coure lists, CRN, hard breaks
#     """
#     # put my algo to generate schedules here
#     valid_schedules = []

#     #here call hardfilter


#     valid_schedules.append(example_schedule)

#     return valid_schedules


def score_schedules(schedules, soft_prefs):
    """
    1. Soft preferences (importtance of 1-5 of how much the user cares about the below two)
    rate my professor score(1-5 of how much they care
    professor excellence and oustanding rating(1-5 of how much they care

    2. class difficulty(importtance of 1-5 of how much the user cares about the below two)
    professor average GPA ((1-5 of how much they care
    class average GPA ((1-5 of how much they care
    minimum acceptable GPA (A+ to F)

    3. Locations(importtance of 1-5 of how much the user cares about the below two)
     maximum late minues(0-30minutes)
    location selected as center(out of the optioins we provided on the website)
    promixity to center point(in km)

     Expected soft_prefs structure:
  {
      "professor_importance": int (1-5),
      "difficulty_importance": int (1-5),
      "location_importance": int (1-5),
      "rmp_score_weight": int (1-5),
      "professor_excellence_weight": int (1-5),
      "professor_gpa_weight": int (1-5),
      "class_gpa_weight": int (1-5),
      "min_acceptable_gpa": str ("A+" to "F"),
      "max_late_minutes": int (0-30),
      "center_location": str,
      "max_proximity_km": float
  }
    """
    scored = []

    for schedule in schedules:
        # NEED UPDATES HERE 
        professor_score = calculate_professor_score(schedule, soft_prefs)
        difficulty_score = calculate_difficulty_score(schedule, soft_prefs)
        # location_score = calculate_location_score(schedule, soft_prefs)

        #weights from soft preferences 

        # Calculate final weighted score 

        
        final_score = (
            professor_score * professor_weight +
            difficulty_score * difficulty_weight +
            location_score * location_weight
        )


        schedule['score'] = final_score
        schedule['breakdown'] = {
            'professor_score': professor_score,
            'difficulty_score': difficulty_score,
            'location_score': location_score
        }

        scored.append(schedule)

    return scored

