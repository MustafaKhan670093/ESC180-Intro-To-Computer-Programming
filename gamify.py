###############################################################################
#            gamify.py - Project 1 Submission - Mustafa Khan                  #
###############################################################################

def initialize():
    '''Initialize the global variables needed for the simulation.'''
    global cur_hedons, cur_health, cur_time
    global last_activity
    global bored_with_stars
    global memory
    global time_till_not_tired
    global cur_star_activity
    global num_stars
    global time_between_stars
    global star_time
    cur_hedons = 0
    cur_health = 0
    cur_star_activity = None
    bored_with_stars = False
    num_stars = 0
    last_activity = "resting" #The program begins with the user resting.
    cur_time = 0
    memory = [] #Used to save the state of the variables in the program
    time_till_not_tired = 0
    time_between_stars = 0
    star_time = []

def star_can_be_taken(activity):
    '''Determine if a star can be taken by the user for a given activity.'''
    global cur_star_activity
    global num_stars
    global bored_with_stars
    global star_time
    global last_activity
    if bored_with_stars == True:
        return False
    elif len(star_time) < 3 and cur_star_activity == activity:
        return True
    elif len(star_time) == 3 and cur_star_activity == activity and (star_time[-1]-star_time[0]) >= 120:
        return True
    elif len(star_time) == 3 and cur_star_activity == activity and (star_time[-1]-star_time[0]) < 120:
        bored_with_stars = True
        return False
    elif len(star_time) > 3 and cur_star_activity == activity:
        for i in range(len(star_time)):
            if i < len(star_time)-2:
                if star_time[i+2] - star_time[i] < 120:
                    bored_with_stars = True
                    return False
        if len(star_time) >= 6:
            star_time = star_time[3:]
        return True
    elif last_activity not in ["running", "textbooks"]:
        return False
    else:
        return False

def perform_activity(activity, duration):
    '''Simulate the user engaging in an activity.'''
    global cur_health
    global cur_hedons
    global cur_time
    global last_activity
    global cur_star_activity
    last_activity = activity
    if activity == "running":
        running(activity, duration)
        cur_time += duration
    elif activity == "resting":
        resting(activity, duration)
        cur_time += duration
    elif activity == "textbooks":
        textbooks(activity, duration)
        cur_time += duration
    else:
        cur_star_activity = None
        pass

def get_cur_hedons():
    '''Return the current number of hedons the user has.'''
    global cur_hedons
    return cur_hedons

def get_cur_health():
    '''Return the current number of health points the user has.'''
    global cur_health
    return cur_health

def offer_star(activity):
    '''Simulate the offering of a star to the user.'''
    global cur_star_activity
    global cur_time
    global num_stars
    global star_time
    if bored_with_stars == True:
        pass
    elif activity == "running" or activity == "textbooks":
        cur_star_activity = activity
        num_stars += 1
        star_time.append(cur_time)

def most_fun_activity_minute():
    '''
    Return the activity that will give the user
    the most number of hedons if undertaken for one minute
    '''
    global cur_hedons
    global cur_health
    global time_till_not_tired
    global last_activity
    global cur_star_activity
    global num_stars
    global bored_with_stars
    save_vars_to_memory()
    perform_activity("running", 1)
    running_hedons = get_cur_hedons()
    reset_memory()
    save_vars_to_memory()
    perform_activity("resting", 1)
    resting_hedons = get_cur_hedons()
    reset_memory()
    save_vars_to_memory()
    perform_activity("textbooks", 1)
    textbooks_hedons = get_cur_hedons()
    reset_memory()
    if running_hedons >= resting_hedons and running_hedons >= textbooks_hedons:
        return("running")
    elif resting_hedons >= running_hedons and resting_hedons >= textbooks_hedons:
        return("resting")
    elif textbooks_hedons >= running_hedons and textbooks_hedons >= resting_hedons:
        return("textbooks")

###############################################################################
#            Helper Functions For perform_activity() Function                 #
###############################################################################

def running(activity, duration):
    '''Simulate the user running.'''
    global cur_health
    global cur_hedons
    global cur_star_activity
    global last_activity
    global time_till_not_tired
    if tired() == True and star_can_be_taken(activity) == True and cur_star_activity == "running":
        cur_health = cur_health + 3*duration if duration <= 180 else cur_health + 3*180 + (duration-180)*1
        cur_hedons = cur_hedons + -2*duration + 3*duration if duration <=10 else cur_hedons + -2*duration + 3*10
        cur_star_activity = None
    elif tired() == True and (star_can_be_taken(activity) == False or cur_star_activity != "running"):
        cur_health = cur_health + 3*duration if duration <= 180 else cur_health + 3*180 + (duration-180)*1
        cur_hedons = cur_hedons + -2*duration
        cur_star_activity = None
    elif tired() == False and star_can_be_taken(activity) == True and cur_star_activity == "running":
        cur_health = cur_health + 3*duration if duration <= 180 else cur_health + 3*180 + (duration-180)*1
        cur_hedons = cur_hedons + 2*duration + 3*duration if duration <=10 else cur_hedons + 2*10 + (duration-10)*-2 + 3*10
        cur_star_activity = None
    elif tired() == False and (star_can_be_taken(activity) == False or cur_star_activity != "running"):
        cur_health = cur_health + 3*duration if duration <= 180 else cur_health + 3*180 + (duration-180)*1
        cur_hedons = cur_hedons + 2*duration if duration <=10 else cur_hedons + 2*10 + (duration-10)*-2
        cur_star_activity = None
    time_till_not_tired = 120
    last_activity = "running"

def resting(activity, duration):
    '''Simulate the user resting.'''
    global last_activity
    global time_till_not_tired
    global cur_star_activity
    time_till_not_tired = time_till_not_tired - duration
    cur_star_activity = None
    last_activity = "resting"

def textbooks(activity, duration):
    '''Simulate the user carrying textbooks.'''
    global cur_health
    global cur_hedons
    global cur_star_activity
    global last_activity
    global time_till_not_tired
    if tired() == True and star_can_be_taken(activity) == True and cur_star_activity == "textbooks":
        cur_health = cur_health + 2*duration
        cur_hedons = cur_hedons + -2*duration + 3*duration if duration <=10 else cur_hedons + -2*duration + 3*10
        cur_star_activity = None
    elif tired() == True and (star_can_be_taken(activity) == False or cur_star_activity != "textbooks"):
        cur_health = cur_health + 2*duration
        cur_hedons = cur_hedons + -2*duration
        cur_star_activity = None
    elif tired() == False and star_can_be_taken(activity) == True and cur_star_activity == "textbooks":
        cur_health = cur_health + 2*duration
        if duration <= 10:
            cur_hedons = cur_hedons + 1*duration + 3*duration
        elif duration > 10 and duration <= 20:
            cur_hedons = cur_hedons + 1*duration + 3*10
        elif duration > 20:
            cur_hedons = cur_hedons + 1*20 + 3*10 + -1*(duration-20)
        cur_star_activity = None
    elif tired() == False and (star_can_be_taken(activity) == False or cur_star_activity != "textbooks"):
        cur_health = cur_health + 2*duration
        cur_hedons = cur_hedons + 1*duration if duration <= 20 else cur_hedons + 1*20 + -1*(duration-20)
        cur_star_activity = None
    time_till_not_tired = 120
    last_activity = "textbooks"


def tired():
    '''Return whether the user is tired or not.'''
    if time_till_not_tired <= 0:
        return False
    else:
        return True

###############################################################################
#         Helper Functions For most_fun_activity_minute() Function            #
###############################################################################

def save_vars_to_memory():
    '''
    Save the current state of the variables.
    Used in most_fun_activity_minute() function.
    '''
    global cur_hedons
    global cur_health
    global time_till_not_tired
    global last_activity
    global cur_star_activity
    global num_stars
    global bored_with_stars
    global memory
    global time_between_stars
    global star_time
    memory = [cur_hedons, cur_health, time_till_not_tired, last_activity,
              cur_star_activity, num_stars, bored_with_stars,
              time_between_stars, star_time]

def reset_memory():
    '''
    Reset the global variables to its previous values.
    Works in conjunction with save_vars_to_memory() function.
    '''
    global cur_hedons
    global cur_health
    global time_till_not_tired
    global last_activity
    global cur_star_activity
    global num_stars
    global bored_with_stars
    global memory
    cur_hedons = memory[0]
    cur_health = memory[1]
    time_till_not_tired = memory[2]
    last_activity = memory[3]
    cur_star_activity = memory[4]
    num_stars = memory[5]
    bored_with_stars = memory[6]
    time_between_stars = memory[7]
    star_time = memory[8]
    memory = []

###############################################################################
#                                   Tests                                     #
###############################################################################

if __name__ == '__main__':

    print("Running When NOT tired and with NO star (Part 1: below and above 10 mins)")
    initialize()
    perform_activity("running", 9)
    print(get_cur_health())           # 27 = 3*9
    print(get_cur_hedons())           # 18 = 2*9
    perform_activity("resting", 120)
    perform_activity("running", 10)
    print(get_cur_health())           # 57 = 27 + 3*10
    print(get_cur_hedons())           # 38 = 18 + 2*10
    perform_activity("resting", 120)
    perform_activity("running", 11)
    print(get_cur_health())           # 90 = 27 + 30 + 3*11
    print(get_cur_hedons())           # 56 = 18 + 20 + 2*10 + -2*1

    print("Running When NOT tired and with NO star (Part 2: below and above 180 mins)")
    initialize()
    perform_activity("running", 180)
    print(get_cur_health())           # 540 = 3*180
    print(get_cur_hedons())           # -320 = 2*10 + 170*-2
    perform_activity("resting", 120)
    perform_activity("running", 181)
    print(get_cur_health())           # 1081 = 540 + 3*180 + 1*1
    print(get_cur_hedons())           # -642 = -320 + 2*10 + 171*-2

    print("Running When NOT tired and WITH a star (below and above 180 mins)")
    initialize()
    offer_star("running")
    perform_activity("running", 9)
    print(get_cur_health())           # 27 = 3*9
    print(get_cur_hedons())           # 45 = 2*9 + 3*9
    perform_activity("resting", 60)
    print("Time till not tired: " + str(time_till_not_tired))
    perform_activity("resting", 60)
    offer_star("running")
    print("Time till not tired: " + str(time_till_not_tired))
    perform_activity("running", 181)
    print(get_cur_health())           # 568 = 27 + 3*180 + 1*1
    print(get_cur_hedons())           # -247 = 45 + 2*10 + 171*-2 + 3*10

    print("Running When TIRED and with NO star (same for below/above 10/180 mins")
    initialize()
    perform_activity("running", 9)
    print(get_cur_health())           # 27 = 3*9
    print(get_cur_hedons())           # 18 = 2*9
    perform_activity("running", 10)
    print(get_cur_health())           # 57 = 27 + 3*10
    print(get_cur_hedons())           # -2 = 18 + -2*10
    perform_activity("running", 11)
    print(get_cur_health())           # 90 = 27 + 30 + 3*11
    print(get_cur_hedons())           # -24 = -2 + -2*11

    print("Running When TIRED and WITH a star")
    initialize()
    offer_star("running")
    perform_activity("running", 9)
    print(get_cur_health())           # 27 = 3*9
    print(get_cur_hedons())           # 45 = 2*9 + 3*9
    offer_star("running")
    perform_activity("running", 181)
    print(get_cur_health())           # 568 = 27 + 3*180 + 1*1
    print(get_cur_hedons())           # -287 = 45 + -2*181 + 3*10

    print("Textbooks When NOT tired and with NO star (Part 1: below and above 20 mins)")
    initialize()
    perform_activity("textbooks", 19)
    print(get_cur_health())           # 38 = 2*19
    print(get_cur_hedons())           # 19 = 1*19
    perform_activity("resting", 120)
    perform_activity("textbooks", 20)
    print(get_cur_health())           # 78 = 38 + 2*20
    print(get_cur_hedons())           # 39 = 19 + 1*20
    perform_activity("resting", 120)
    perform_activity("textbooks", 21)
    print(get_cur_health())           # 120 = 78 + 2*21
    print(get_cur_hedons())           # 58 = 39 + 1*20 + -1*1


    print("Textbooks When NOT tired and with NO star (Part 2: below and above 180 mins)")
    initialize()
    perform_activity("textbooks", 180)
    print(get_cur_health())           # 360 = 2*180
    print(get_cur_hedons())           # -140 = 1*20 + 160*-1
    perform_activity("resting", 120)
    perform_activity("textbooks", 181)
    print(get_cur_health())           # 722 = 360 + 2*181
    print(get_cur_hedons())           # -281 = -140 + 1*20 + 161*-1

    print("Textbooks When NOT tired and WITH a star")
    initialize()
    offer_star("textbooks")
    perform_activity("textbooks", 9)
    print(get_cur_health())           # 18 = 2*9
    print(get_cur_hedons())           # 36 = 1*9 + 3*9
    perform_activity("resting", 60)
    perform_activity("resting", 60)
    offer_star("textbooks")
    perform_activity("textbooks", 181)
    print(get_cur_health())           # 380 = 18 + 2*181
    print(get_cur_hedons())           # -75 = 36 + 1*20 + 161*-1 + 3*10

    print("Textbooks When TIRED and with NO star")
    initialize()
    perform_activity("textbooks", 9)
    print(get_cur_health())           # 18 = 2*9
    print(get_cur_hedons())           # 9 = 1*9
    perform_activity("textbooks", 10)
    print(get_cur_health())           # 38 = 18 + 2*10
    print(get_cur_hedons())           # -11 = 9 + -2*10
    perform_activity("textbooks", 11)
    print(get_cur_health())           # 60 = 38 + 2*11
    print(get_cur_hedons())           # -33 = -11 + -2*11

    print("Textbooks When TIRED and WITH a star")
    initialize()
    offer_star("textbooks")
    perform_activity("textbooks", 9)
    print(get_cur_health())           # 18 = 2*9
    print(get_cur_hedons())           # 36 = 1*9 + 3*9
    offer_star("textbooks")
    perform_activity("textbooks", 181)
    print(get_cur_health())           # 380 = 18 + 2*181
    print(get_cur_hedons())           # -296 = 36 + -2*181 + 3*10


    print("Star Tests UNDER 120 mins")
    initialize()
    print(star_can_be_taken("running")) #False
    offer_star("running")
    print(star_can_be_taken("running")) #True. Correct
    offer_star("running")
    print(star_can_be_taken("running")) #True. Coorect
    offer_star("running")
    print(star_can_be_taken("running")) #False. Correct.
    print("User is bored with stars: " + str(bored_with_stars))
    offer_star("running")
    print(star_can_be_taken("running"))  #False
    print("User is bored with stars: " + str(bored_with_stars))
    initialize()
    offer_star("running")
    print(star_can_be_taken("running")) #True. Correct
    offer_star("running")
    print(star_can_be_taken("textbooks")) #False. Correct
    initialize()
    offer_star("jogging")
    print(star_can_be_taken("textbooks")) #False. Correct

    print("Star Tests OVER 120 mins")
    initialize()
    offer_star("running")
    print(star_can_be_taken("running")) #True
    perform_activity("resting", 60)
    offer_star("running")
    print(star_can_be_taken("running")) #True
    perform_activity("resting", 60)
    offer_star("running")
    print(star_can_be_taken("running")) #True

    print("Star OFFERED but NOT taken")
    initialize()
    offer_star("running")
    perform_activity("textbook", 10)
    print(star_can_be_taken("running")) #False
    offer_star("textbooks")
    perform_activity("resting", 120)
    print(star_can_be_taken("textbooks")) #False


    print("Star and Fun Activity Tests")
    initialize()
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    offer_star("textbooks")
    print(most_fun_activity_minute())  # running

    initialize()
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    offer_star("textbooks")
    perform_activity("running", 30)
    print(most_fun_activity_minute())  # resting

    initialize()
    offer_star("textbooks")
    perform_activity("running", 101)
    print(get_cur_health()) # 303
    print(get_cur_hedons()) # -162
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    perform_activity("textbooks", 20)
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks

    initialize()
    offer_star("resting")
    offer_star("textbooks")
    perform_activity("running", 101)
    print(get_cur_health()) # 303
    print(get_cur_hedons()) # -162
    perform_activity("textbooks", 20)
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks
    perform_activity("textbooks", 20)
    offer_star("textbooks")
    print(most_fun_activity_minute())  # textbooks