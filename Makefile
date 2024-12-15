HSPICE = hspice

EXAMPLE_SP = $(wildcard example/*.sp)
EXAMPLE_LIS = $(EXAMPLE_SP:.sp=.lis)
EXAMPLE_ST0 = $(EXAMPLE_SP:.sp=.st0)
EXAMPLE_SW0 = $(EXAMPLE_SP:.sp=.sw0)

all: example


%.lis: %.sp
	$(HSPICE) -i $< -o $@


example: $(EXAMPLE_LIS)


clean:
	rm -f $(EXAMPLE_LIS)
	rm -f $(EXAMPLE_ST0)
	rm -f $(EXAMPLE_SW0)
	@echo "Clean all generated files."


.PHONY: all clean example