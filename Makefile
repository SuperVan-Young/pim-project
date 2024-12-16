HSPICE = hspice

EXAMPLE_SP = $(wildcard example/*.sp)
EXAMPLE_LIS = $(EXAMPLE_SP:.sp=.lis)
EXAMPLE_ST0 = $(EXAMPLE_SP:.sp=.st0)
EXAMPLE_SW0 = $(EXAMPLE_SP:.sp=.sw0)

all: example


%.lis: %.sp
	$(HSPICE) -i $< -o $@


example: $(EXAMPLE_LIS)


calibrate:
	python pim.py --run_dir ./run/calibrate_config_a --cell_type A
	python pim.py --run_dir ./run/calibrate_config_b --cell_type B

clean:
	rm -f $(EXAMPLE_LIS)
	rm -f $(EXAMPLE_ST0)
	rm -f $(EXAMPLE_SW0)
	rm -rf ./run
	@echo "Clean all generated files."


.PHONY: all clean example calibrate