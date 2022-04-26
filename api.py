import requests
import json
import fastapi

# function to get specific information about user
def get_github_user_data(user_data):
	data_to_remove = []
	for data in user_data:
		if data not in ['login', 'name', 'bio']:
			data_to_remove.append(data)

	# deleting unnecesarry informations
	for data in data_to_remove:
		del user_data[data]

	user_data['repo_languages'] = {}
	return user_data


# function to get specific informations about all repositories
def get_github_user_repos(url, authentication):
	user_repos = requests.get(url, auth=authentication)

	if not user_repos.ok:
		return None

	user_repos = user_repos.json()

	# deleting unnecesarry informations
	for repo in user_repos:
		data_to_remove = []
		for repo_data in repo:
			if repo_data not in ['name', 'languages_url']:
				data_to_remove.append(repo_data)
		for data in data_to_remove:
			del repo[data]

	# adding languages information for every repository
	for repo in user_repos:
		repo_languages = requests.get(repo['languages_url'], auth=authentication)

		if not repo_languages.ok:
			return None

		repo_languages = repo_languages.json()

		del repo['languages_url']
		repo['languages'] = repo_languages
	
	return user_repos

	
# function to return information about user
def github_user_data(username, authentication):
	url = f"https://api.github.com/users/{username}"
	user_data = requests.get(url, auth=authentication)

	if not user_data.ok:
		return None

	user_data = user_data.json()

	user_repos = get_github_user_repos(user_data['repos_url'], authentication)

	if user_repos == None:
		return None

	user_data = get_github_user_data(user_data)

	# counting summary size for every language
	for repo in user_repos:
		for lang in repo['languages']:
			if lang not in user_data['repo_languages']:
				user_data['repo_languages'][lang] = 0
			user_data['repo_languages'][lang] += int(repo['languages'][lang])

	answer = {}
	answer['user'] = user_data
	answer['repos'] = user_repos

	return answer



app = fastapi.FastAPI()

@app.get("/check_user")
def home(username : str):
	github_auth = ('','')
	with open('auth.json') as auth_file:
		data = json.load(auth_file)
		if('username' in data and 'token' in data):
			github_auth = (data['username'], data['token'])

	print(github_auth)

	answer = github_user_data(username, github_auth)
	if answer == None:
		answer = "User not found or request limit exceeded"
	return answer
