stage := "staging"

.PHONY: setup
setup:
	ansible-playbook setup.yml --limit $(stage) $(args)

.PHONY: deploy
deploy:
	ansible-playbook deploy.yml --limit $(stage) $(args)
