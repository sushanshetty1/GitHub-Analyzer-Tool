from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Replace with your GitHub personal access token
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
API_URL = 'https://api.github.com'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def fetch_repo_data(owner, repo):
    url = f'{API_URL}/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return None  # Repository not found
    return response.json()


def fetch_contributors(owner, repo):
    url = f'{API_URL}/repos/{owner}/{repo}/contributors'
    response = requests.get(url, headers=headers)
    return response.json()


def fetch_recent_commits(owner, repo):
    url = f'{API_URL}/repos/{owner}/{repo}/commits'
    response = requests.get(url, headers=headers)
    return response.json()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        owner = request.form['owner']
        repo = request.form['repo']

        repo_data = fetch_repo_data(owner, repo)
        if repo_data is None:
            return render_template('index.html', error="Repository not found. Please check the details and try again.")

        contributors = fetch_contributors(owner, repo)
        commits = fetch_recent_commits(owner, repo)

        return render_template('results.html', repo_data=repo_data, contributors=contributors, commits=commits)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
