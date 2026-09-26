# Body mass index calculator 
# Give estimate of whether your body weight is in a healthy range for your height
def bmi_calculator(weight,height):
    bmi=weight/((height/100)**2) # formula of bmi ( Height in centimeter )
    return round(bmi,2)

# Basal metabolic rate calculator
# Gives how many calories your body burns at complete rest just to keep basic functions working
def bmr_calculator(gender,age,weight,height):
    if gender=="Male":
        bmr=(10*weight)+(6.25*height)-(5*age)+5 # formula of bmr for male
        return round(bmr,2)
    elif gender=="Female":
        bmr=(10*weight)+(6.25*height)-(5*age)-161 # formula of bmr for female
        return round(bmr,2)

# Total daily energy expenditure calculator
# Gives us approximately how many calories you burn in a whole day, including your normal activities
def tdee_calculator(bmr,activity):
    activity_factor={"Sendentary":1.20,
            "Lightly Active":1.375,
            "Moderately Active":1.55,
            "Very Active":1.725,
            "Extra Active":1.90} # Activity factor value is this [Already Fixed]
    tdee=bmr*activity_factor[activity] # formula of tdee
    return round(tdee,2)

# calory target ( maintain , increse or decrese )
def calorie_target(tdee,aim):
    if aim=="weight maintain": # if we want to maintain the calorie
        calorie=tdee # formula
    elif aim=="weight loss": # if we want to loose the calorie
        calorie=tdee-400 # formula
    elif aim=="weight gain": # if we want to gain the calorie
        calorie=tdee+300 # formula
    return round(calorie,2)

# # calling bmi calculator
# print(bmi_calculator(60,150)) # value - weight and height 

# # calling bmr calculator
# print(bmr_calculator("male",25,60,155)) # value - gender , age , weight and height

# # calling tdee calculator
# bmr_value=bmr_calculator("male",25,50,150) # value - gender , age , weight and height
# print(tdee_calculator(bmr_value,"Very Active")) # value - bmr_value and activity_factor [Choose it by yourself]

# # calling calorie target
# tdee_value=tdee_calculator(bmr_value,"Very Active") # value - bmr_vallue and activity_factor [Choose it by yourself]
# print(calorie_target(tdee_value,"weight loss")) # value - tdee_value and aim