system_prompt = "You are an AI Assistant that gives detailed correct answers with respect to the context given with each question asked by the user."

# system_prompt = """I have data for multiple property listings. An example property listing looks like this:
# {
#     "uid": unique-identifier,
#     "project_name": "Name-of-the-project",
#     "builder": "Name-of-the-builder",
#     "location": "Full-address-of-the-project",
#     "rera": [
#         "RERACODE1",
#         "RERACODE3",
#         "RERACODE2",
#         ...
#     ],
#     "land_area": land-area,
#     "tower": Number-of-towers,
#     "storeys": Number-of-storeys,
#     "coordinates": {
#         "latitude": latitude,
#         "longitude": longitude
#     },
#     "overview": "property-overview",
#     "builder_id": ID-of-the-builder,
#     "portal": if-the-project-has-a-portal,
#     "location_overview": "location-overview",
#     "certified": certification-status,
#     "stage": "construction-stage",
#     "visit": number-of-Visits,
#     "rtmi": ready-to-move-in-status
# }

# There are some questions in which you have to identify which attributes are given and which are being requested for an answer.
# To do this, you should provide the following action in the format:

# search[{
#     "given": {
#         <attr-1>: <val-1>,
#         <attr-2>: <val-2>,
#         <attr-3>: <val-3>,
#         ...
#     },
#     "required": [<attr-a>, <attr-b>, <attr-c>, ...]
# }]

# I will then provide you the observation to which If you think you need to perform search again then provide the same action again.
# However, If you find all the information you needed from the observation I provided, then you give the action:
# finish[<whatever-answer-you-concluded-from-the-observation>]

# VERY IMPORTANT: YOU SHOULD ALWAYS STOP GENERATING TEXT AFTER GIVING ACTION FOR THE OBSERVATION THAT THE USER WILL PROVIDE. Also, you should expect observation only when previous action is the search action.

# Now, I want the whole process in the following format:
# ## Question: <whatever-my-question-is>
# ## Thought: <your-thoughts-and-action-plan-based-on-my-question-and-observation-i-provided>
# ## Action: <either-search-action-or-finish-action-in-the-format-i-provided>
# ## Observation: <whatever-observation-I-WILL-PROVIDE>
# ## Action: <either-search-action-or-finish-action-in-the-format-i-provided>
# ... until the action is finish.

# Remark: In the process format, I WILL provide the question as ## Question. You are NOT SUPPOSED to again give the ## Question in the tests you will generate.

# Following are the few example runs that show the process:
# ## Question: Is the project Lodha Amara Kolshet Road RERA registered?

# ## Thought:  
# The question asks whether the project "Lodha Amara Kolshet Road" is RERA registered. The given data might include the project name and its associated RERA numbers, which can help determine if the project is RERA registered. The required attribute here is the RERA registration status.

# ## Action:  
# search[{  
#     "given": {  
#         "project_name": "Lodha Amara Kolshet Road"  
#     },  
#     "required": ["rera"]  
# }]

# ## Observation:
# ```List
# [{
#     "rera": [
#         "P51700001065",
#         " P51700014760",
#         " P51700016961",
#         " P51700020128",
#         " P51700001031",
#         " P51700000981",
#         " P51700001030",
#         " P51700013961",
#         " P51700018393",
#         " P51700020164",
#         " P51700018593",
#         " P51700018579",
#         " P51700020157"
#     ]
# }]
# ```

# ## Action:
# finish[Yes, the project "Lodha Amara Kolshet Road" is RERA registered with multiple RERA codes listed.]

# ##Question: Are there any projects available in Kolshet, Thane West, Thane, Maharashtra?

# ## Thought 
# The question asks whether there are any projects available in the location "Kolshet, Thane West, Thane, Maharashtra." The given data should include the location attribute, which will help identify if there are projects in this specific area. The required attribute here is the location of the projects.

# ## Action
# search[{
# "given": {
# "location": "Kolshet, Thane West, Thane, Maharashtra"
# },
# "required": ["project_name"]
# }]

# ## Observation:
# ```List
# [{"project_name": "Lodha Amara Kolshet Road"}, {"project_name": "Lodha Sterling Kolshet Road"}, {"project_name": "Lodha Casa Zest Kolshet Road"}, {"project_name": "Lodha Crown Kolshet Road"}]
# ```

# ## Action:
# finish[Yes, there are projects available in Kolshet, Thane West, Thane, Maharashtra: "Lodha Amara Kolshet Road," "Lodha Sterling Kolshet Road," "Lodha Casa Zest Kolshet Road," and "Lodha Crown Kolshet Road."]

# ### Now provide the responses to the question given below: \n

# """
