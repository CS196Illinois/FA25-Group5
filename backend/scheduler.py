
def generate_schedule(courses, preferences):
    """
    generate and rank schedules
    return top 10 schedules
    """
    # extract preferences
    hard_prefs = preferences.get("hard_preferences", {})
    soft_prefs = preferences.get("soft_preferences", {})

    # generate all valid schedules based on hard preferences
    valid_schedules = generate_valid_schedules(courses, hard_prefs)

    # ccore each schedule based on soft preferences
    scored_schedules = score_schedules(valid_schedules, soft_prefs)

    #return top 10
    top_schedules = sorted(scored_schedules, key=lambda x: x['score'], reverse=True)[:10]

    return top_schedules


def generate_valid_schedules(courses, hard_prefs):
    """
    Hard preferences
    coure lists, CRN, hard breaks
    """
    # put my algo to generate schedules here
    valid_schedules = []

    # Example structure of what you should return:


    valid_schedules.append(example_schedule)

    return valid_schedules


def score_schedules(schedules, soft_prefs):
    """
    1. Soft preferences (importtance of 1-5 of how much the user cares about the below two)
    rate my professor score 
    professor excellence and oustanding rating

    2. class difficulty(importtance of 1-5 of how much the user cares about the below two)
    professor average GPA (1-5)
    class average GPA (1-5)
    minimum acceptable GPA (A+ to F)

    3. Locations(importtance of 1-5 of how much the user cares about the below two)
     maximum late minues(0-30minutes)
    location selected as center(out of the optioins we provided on the website)
    promixity to center point(in km)
    """
    scored = []

    for schedule in schedules:
        # Calculate score for each category
        professor_score = calculate_professor_score(schedule, soft_prefs)
        difficulty_score = calculate_difficulty_score(schedule, soft_prefs)
        location_score = calculate_location_score(schedule, soft_prefs)

        # Weight each score by user's importance rating (1-5)
        professor_weight = soft_prefs.get("professor_importance", 3)
        difficulty_weight = soft_prefs.get("difficulty_importance", 3)
        location_weight = soft_prefs.get("location_importance", 3)

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



#Subs with the ones alr written in the softbreak code
#remember if receive -1 then ignore that part to prevent our function from breaking
# def calculate_professor_score(schedule, soft_prefs):



# def calculate_difficulty_score(schedule, soft_prefs):



# def calculate_location_score(schedule, soft_prefs):
