import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def test_all_combinations(dut):
    dut._log.info("Starting test...")

    # Start the clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset
    dut._log.info("Resetting...")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    dut._log.info("Testing all combinations...")

    # Iterate through possible inputs (assuming 3 inputs A, B, C)
    for i in range(8):
        # Apply input as a whole byte to avoid packed array errors
        dut.ui_in.value = i
        
        # Wait for combinational logic to settle
        await Timer(1, units="ns")

        # Extract bits for verification logic
        A = (i >> 0) & 1
        B = (i >> 1) & 1
        C = (i >> 2) & 1

        # DEFINE YOUR EXPECTED OUTPUT 'F' HERE
        # Example: F = A & B | C (Change this to match your Verilog logic!)
        F = (A & B) | C 

        # Check the output (uo_out)
        # We check bit 0 of uo_out (assuming that's where your result is)
        actual_F = int(dut.uo_out.value) & 1
        
        assert actual_F == F, f"Failed at input {i}: expected {F}, got {actual_F}"
        
    dut._log.info("All tests passed!")
