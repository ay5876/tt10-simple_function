# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Clock (manual style). Use "unit" (not "units") to avoid warnings.
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset (same structure as the manual)
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # IMPORTANT FIX:
    # DO NOT do dut.ui_in[0].value = ...
    # Instead drive the whole bus, putting din on bit0.

    # din = 0
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 20)

    # reset pulse (optional, manual-style)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # din = 1
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 20)

    # din = 0
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)

    # din = 1
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 20)

    # din = 0
    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    # No asserts (manual says not required). :contentReference[oaicite:1]{index=1}
