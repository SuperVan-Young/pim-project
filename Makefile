HSPICE = hspice

EXAMPLE_SP = $(wildcard example/*.sp)
EXAMPLE_LIS = $(EXAMPLE_SP:.sp=.lis)
EXAMPLE_ST0 = $(EXAMPLE_SP:.sp=.st0)
EXAMPLE_SW0 = $(EXAMPLE_SP:.sp=.sw0)

CONFIG_JSON = $(wildcard config/*.json)
CONFIG_RPT  = $(CONFIG_JSON:.json=.rpt)

all: 
	make example
	make gen_config
	make experiment


%.lis: %.sp
	$(HSPICE) -i $< -o $@


example: $(EXAMPLE_LIS)


calibrate:
	python pim.py --run_dir ./run/calibrate_config_a --cell_type A --debug
	python pim.py --run_dir ./run/calibrate_config_b --cell_type B --debug

gen_config:
	python gen_config.py

%.rpt: %.json
	python pim.py --run_dir ./run/$* --extra_args $< | tee $@


experiment: $(CONFIG_RPT)

clean:
	rm -f $(EXAMPLE_LIS)
	rm -f $(EXAMPLE_ST0)
	rm -f $(EXAMPLE_SW0)
	rm -rf ./run
	rm -rf ./config
	@echo "Clean all generated files."


.PHONY: all clean example calibrate experiment gen_config