import pytest


@pytest.mark.api
def test_user_exists(github_api):
    user = github_api.get_user('defunkt')
    assert user['login'] == 'defunkt'


@pytest.mark.api
def test_user_not_exists(github_api):
    r = github_api.get_user('butenkosergii')
    assert r['message'] == 'Not Found'


@pytest.mark.api
def test_repo_can_be_found(github_api):
    r = github_api.search_repo('become-qa-auto')
    assert r['total_count'] == 58
    assert 'become-qa-auto' in r['items'] [0] ['name']


@pytest.mark.api
def test_repo_cannot_be_found(github_api):
    r = github_api.search_repo('sergiibutenko_repo_non_exist')
    assert r['total_count'] == 0 



@pytest.mark.api
def test_repo_with_single_char_be_found(github_api):
    r = github_api.search_repo('s')
    assert r['total_count'] != 0 


@pytest.mark.api
def test_emojis(github_api):
    emojis = github_api.get_emojis()
    assert 'smile' in emojis 


@pytest.mark.api
def test_commits(github_api):
    commits = github_api.get_commits('octocat', 'Hello-World')
    assert len(commits) > 0
    assert 'commit' in commits[0]
    assert 'message' in commits[0]['commit']
    assert 'author' in commits[0]['commit']


@pytest.mark.api
def test_specific_commit(github_api):
    commits = github_api.get_commits('octocat', 'Hello-World')
    commit_messages = [commit['commit']['message'] for commit in commits]
    assert 'first commit' in commit_messages


@pytest.mark.api
def test_no_commits_in_repo(github_api):
    commits = github_api.get_commits('nonexistent_user', 'nonexistent_repo')
    assert len(commits) == 0 or 'message' in commits
    if 'message' in commits:
        assert commits['message'] == 'Not Found'