default:
	python3 setup.py
	$(MAKE) sea_2

sea_2:
	timestamp=$$(date +%Y_%m_%d_%H_%M); \
	python3 fetchHimawariSEA_2PH.py

clean:
	find run_logs/fetchHimawariSEA_2PH -type f -name '*.stderr' -empty -delete
	find run_logs/fetchHimawariSEA_ALL -type f -name '*.stderr' -empty -delete
