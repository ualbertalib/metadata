	from secret import password, client_id, client_secret

	git = Github(client_id, client_secret)
	org = git.get_organization('ualbertalib')
	repo = org.get_repo('metadata')
	pull = repo.create_pull(title="Daily Data Dictionary Update", head="data_dictionary_update", base="master", body="See commit message for yesterdays changes to the data dictionary profiles.")
	repo.issue(pull["number"]).edit(assignees=["zschoenb", "danydvd", "sfarnel", "johnhuck"], lables=['Jpuiter Data Dictionary'])