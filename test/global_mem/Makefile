SIM ?= icarus
TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(PWD)/../../src/spi/memory.v
VERILOG_SOURCES += $(PWD)/../../src/spi/spi_rx.v
VERILOG_SOURCES += $(PWD)/../../src/spi/packer.v

COCOTB_TOPLEVEL = GLOBAL_MEMORY
COCOTB_TEST_MODULES = test
# export PYTHONPATH := $(PWD)/..:$(PYTHONPATH)
include $(shell cocotb-config --makefiles)/Makefile.sim