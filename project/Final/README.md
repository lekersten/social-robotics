# Social Robotics 
## Final Project
### Lauren Kersten (s3950905) and Yara Bikowski (s3989585)
#### University of Groningen, Groningen, NL

##

Two different functionalities have been implemented. 
These are a stretching routine and a functionality with activity lists that can be used to answer questions and suggest activities.

### Submitted Files

There are 6 files in the submission:
- **project_main.py**: this is the file that can be run to test all functionalities together
- **exercise_process.py**: the file containing only the stretching routine functionality
- **exercises.py**: the separate exercises that are done during the stretching routine
- **database_functions.py**: the functions that can be used to access and update the activity list database
- **suggest_activity.py**: the file containing only the suggestion functionality for the activity lists
- **answer_question.py**: the file containing only the question answering functionality for the activity lists

### Install Requirements
The requirements to run the code are in the ```requirements.txt``` file. 
When running the code for the first time, a HuggingFace model will be downloaded which will take some time.
Subsequent runs will reuse this download and thus be faster.

### Running Code 
```
python3 project_main.py
```

Depending on when the code is used, it will be a good idea to uncomment the code:
```
# global date
# date = "2024-03-28"
```
This is present at the start of the **project_main.py** file. 
Uncommenting this code will ensure that there are lists in the activity list database which can be used to answer questions.
Otherwise, the current date is used which might fall outside of the end date of the activities.

**Make sure to change the realm before running the code!**
