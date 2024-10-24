start:
	@timestamp=$$(date +%Y_%m_%d_%H_%M); \
	python3 fetchHimawari9h24.py 1>> "run_logs/$$timestamp.stdout" 2>> "run_logs/$$timestamp.stderr"
