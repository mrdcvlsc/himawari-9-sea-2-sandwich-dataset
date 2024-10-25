default:
	python3 setup.py
	$(MAKE) sea_2
	$(MAKE) sea_all

sea_2:
	@timestamp=$$(date +%Y_%m_%d_%H_%M); \
	python3 fetchHimawariSEA_2PH.py 1>> "run_logs/fetchHimawariSEA_2PH/$$timestamp.stdout" 2>> "run_logs/fetchHimawariSEA_2PH/$$timestamp.stderr"

sea_all:
	@timestamp=$$(date +%Y_%m_%d_%H_%M); \
	python3 fetchHimawariSEA_ALL.py 1>> "run_logs/fetchHimawariSEA_ALL/$$timestamp.stdout" 2>> "run_logs/fetchHimawariSEA_ALL/$$timestamp.stderr"

clean:
	find run_logs/fetchHimawariSEA_2PH -type f -name '*.stderr' -empty -delete
	find run_logs/fetchHimawariSEA_ALL -type f -name '*.stderr' -empty -delete
