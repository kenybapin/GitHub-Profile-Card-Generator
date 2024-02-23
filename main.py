import json
import requests
from jinja2 import Template

def get_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url)
    if response.status_code == 200:
        limit_info = response.json()
        return limit_info
    else:
        print("Error occurred:", response.status_code)
        return None

def get_user_and_repo_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data, data["repos_url"]
    else:
        print(f"Error occurred when fetching user and repo data for {username}:", response.status_code)
        return None, None

def get_repo_languages(repos_data):
    languages = {}
    for repo in repos_data:
        repo_languages_url = repo["languages_url"]
        languages_response = requests.get(repo_languages_url)
        repo_languages = languages_response.json()
        for lang, bytes in repo_languages.items():
            languages[lang] = languages.get(lang, 0) + bytes
    return languages

def create_html_page(combined_result):
    template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="initial-scale=1, width=device-width" />
    <title>GitHub User Information</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="card">
        <h1>{{ user_info.name }} ({{ user_info.login }})</h1>
        <div class="image-crop">
    			<img id="avatar" src="{{ user_info.avatar_url }}" alt="Profile Picture">
        </div>

        <div id="bio">
            <p>{{ user_info.bio }}</p>
    	    <div id="location"><p>🌍 Location: {{ user_info.location }}</p></div>
    	</div>

        <ul>
            {% for lang, bytes in repo_languages.items() %}
                <li>{{ lang }}</li>
            {% endfor %}
        </ul>

        <hr class="hr-1">

        <div id="stats">
    	    <div class="col">
    	    	<p class="stat">{{ user_info.public_repos }}</p>
    	    	<p class="label">Public repos</p>
    	    </div>
    	    <div class="col">
    	    	<p class="stat">{{ user_info.followers }}</p>
    	    	<p class="label">Followers</p>
    	    </div>
    	    <div class="col">
    	    	<p class="stat">{{ user_info.following }}</p>
    	    	<p class="label">Following</p>
    	    </div>
    	</div>

        <div id="buttons">
    			<button><a href="https://github.com/{{ user_info.login }}">Follow</a></button>
    			<button id="msg"><a href="mailto:example">Contact</button>
    	</div>
    </div>
</body>
</html>
""")

    html_content = template.render(combined_result)
    with open("github_results.html", "w") as f:
        f.write(html_content)
    print("HTML results generated in github_results.html")


def main():
    rate_limit_info = get_rate_limit()
    if rate_limit_info:
        print("Rate limit:", rate_limit_info["rate"]["limit"])
        print("Remaining calls:", rate_limit_info["rate"]["remaining"])
        remaining_calls = rate_limit_info["rate"]["remaining"]
        if remaining_calls == 0:
            print(f"You have exhausted your rate limit. Please wait until the rate limit resets.")
            sys.exit(1)  # Exit with error code 1

    username = input("Enter the GitHub username: ")
    
    user_data, repos_url = get_user_and_repo_data(username)
    if user_data and repos_url:
        repos_data = requests.get(repos_url).json()  # Reuse user_data's repos_url
        repo_languages = get_repo_languages(repos_data)

        combined_result = {
            "repo_languages": repo_languages,
            "user_info": user_data,  # Extract user info from user_data
        }
        create_html_page(combined_result)
        json_result = json.dumps(combined_result, indent=2)
        print(json_result)
    else:
        print("Failed to retrieve user and repo data.")

if __name__ == "__main__":
    main()
