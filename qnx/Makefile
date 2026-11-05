# CageCheck-on-QNX — packaging Makefile (QNX target side)
#
# CageCheck is Python, not C, so there is nothing to cross-compile.
# This Makefile PACKAGES the port for the QNX target: it stages the
# upstream app files (referenced, not vendored here — the submission
# repo holds the patches + this layer + build files only), the
# qnx_cage porting layer, and the QNX buildfile, then verifies the
# result. It runs ON the QNX target (QEMU image or Developer Desktop)
# or on the host for a dry-run check.
#
# Usage on the target:
#   make check     # sandbox tests (Linux) / import check (QNX)
#   make stage     # stage files under ./stage/cagecheck-qnx
#   make install   # install into /opt/cagecheck-qnx on the target
#
# VERIFY-ON-TARGET: install paths (/opt, python3 location) and the
# `python3` binary name on the QNX 8.0 Python port.

PYTHON ?= python3
PREFIX ?= /opt/cagecheck-qnx
STAGE  ?= ./stage/cagecheck-qnx
UPSTREAM ?= ../upstream/cagecheck

.PHONY: check stage install clean

check:
	$(PYTHON) -m unittest discover -s tests -v

stage:
	mkdir -p $(STAGE)/app $(STAGE)/qnx_cage $(STAGE)/runs
	cp $(UPSTREAM)/app/policy.py $(UPSTREAM)/app/cage.py $(UPSTREAM)/app/server.py \
	   $(UPSTREAM)/app/llm.py $(UPSTREAM)/app/receipts.py $(UPSTREAM)/app/index.html \
	   $(STAGE)/app/
	cp src/qnx_cage/*.py $(STAGE)/qnx_cage/
	cp qnx/cagecheck-qnx.build $(STAGE)/
	cp qnx/run-on-qnx.sh $(STAGE)/
	@echo "staged to $(STAGE) — apply patches/ to app/*.py before running"

install: stage
	mkdir -p $(PREFIX)
	cp -r $(STAGE)/* $(PREFIX)/
	chmod +x $(PREFIX)/run-on-qnx.sh
	@echo "installed to $(PREFIX)"

clean:
	rm -rf ./stage
