# GitHub Profile Card Generator

This Python script allows you to generate a GitHub profile card using the GitHub API.

![preview](/preview.png)<br><br>


## Prerequisites

-   Python 3.x
-   `requests` library (install via `pip install requests`)

## Usage

1.  Clone this repository to your local machine:
    
    ```
    git clone https://github.com/kenybapin/github-profile-card-generator.git
    ```
    
2.  Navigate to the project directory:
    
    ```
    cd github-profile-card-generator
    ```
    
3.  Run the script with Python:
    
    ```
    python3 main.py
    Enter the GitHub username: 
    ```
    Enter the github username. This will generate an HTML file with a GitHub profile card.

## Note
There is no authentication system here; the use of the GitHub API is of course free but comes with limitations...
Each execution of the script consumes about 10 API calls.
Be mindful of the GitHub API rate limit, which allows 60 calls per hour.
If you exceed this call limit, you must wait for one hour, then the number of calls will reset to 60.
