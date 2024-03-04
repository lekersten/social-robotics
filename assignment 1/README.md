# Social Robotics 
## Assignment 1: Verbal Interaction
### Lauren Kersten (s3950905) and Yara Bikowski (s3989585)
#### University of Groningen, Groningen, NL

##

We have implemented a verbal interaction through the use of a pre-trained LLM and a social robot in which the goal is to create a human-like companion.

### Submitted Files

There are 3 files in the submission:
- **assignment1.py**: latest tested version - robot hears itself speak and thus converses with itself
- **assignment1_close_stream.py**: fixes issue mentioned above, but a bit buggy
- **assignment1_godel.py**: user interaction through the terminal to test implemented LLM

### Install Requirements
The requirements to run the code are in the requirements.txt file. 
When running the code for the first time, a HuggingFace model will be downloaded which will take some time.
Subsequent runs will reuse this download and thus be faster.

### Running Code 
```
python3 assignment1.py
```
! Make sure to change the realm before running the code!