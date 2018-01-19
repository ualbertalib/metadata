from secret import password, client_id, client_secret
from github import Github

git = Github('metadata-bot', password)
org = git.get_organization('ualbertalib')
repo = org.get_repo('metadata')
pull = repo.create_pull(title="Daily Data Dictionary Update", head="data_dictionary_update", base="master", body="See commit message for yesterdays changes to the data dictionary profiles.")
repo.get_issue(pull.number).edit(assignees=["danydvd", "sfarnel", "johnhuck"], labels=['Jupiter Data Dictionary'])
