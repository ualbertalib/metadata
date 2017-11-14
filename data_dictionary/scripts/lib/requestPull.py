from secret import password, client_id, client_secret
<<<<<<< HEAD
from github import Github
=======
import PyGithub as Github
>>>>>>> 07a046970e6d86fc27e7221260c5405a0be9b4b8

git = Github('zschoenb', password)
org = git.get_organization('ualbertalib')
repo = org.get_repo('metadata')
pull = repo.create_pull(title="Daily Data Dictionary Update", head="data_dictionary_update", base="master", body="See commit message for yesterdays changes to the data dictionary profiles.")
repo.issue(pull["number"]).edit(assignees=["zschoenb", "danydvd", "sfarnel", "johnhuck"], lables=['Jupiter Data Dictionary'])