import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

def _get_bit_from_binstr(binstr: str, bit_index: int) -> str:
    """
    binstr is MSB..LSB. bit_index=0 means LSB (rightmost char).
    Returns '0','1','x','z', etc.
    """
    return binstr[-1 - bit_index]

async def wait_until_01(dut, timeout_ns=500, step_ns=10):
    """
    Wait until uo_out bits become only 0/1 (no X/Z).
    Returns uo_out binstr.
    """
    waited = 0
    while waited <= timeout_ns:
        s = dut.uo_out.value.binstr.lower()
        # accept only if every bit is 0 or 1
        if all(c in "01" for c in s):
            return s
        await Timer(step_ns, unit="ns")
        waited += step_ns
    # timeout: return whatever we have for debugging
    return dut.uo_out.value.binstr.lower()

@cocotb.test()
async def test_all_combinations(dut):
    # Clock (safe for template / GL)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    # Init
    dut.ena.value = 1
    dut.rst_n.value = 1
    dut.uio_in.value = 0
    dut.ui_in.value = 0

    # IMPORTANT for gate-level: give it time to settle from X states
    await Timer(200, unit="ns")

    # Test all 8 combinations: ui_in[0]=A, [1]=B, [2]=C
    for i in range(8):
        dut.ui_in.value = i
        await Timer(50, unit="ns")  # initial settle

        A = (i >> 0) & 1
        B = (i >> 1) & 1
        C = (i >> 2) & 1

        Cn = 1 - C
        Fexp = (A & B) | Cn   # F = AB + C'
        Yexp = Cn             # Y = C'

        # Wait until outputs are 0/1 (no X/Z) before checking
        uo_str = await wait_until_01(dut, timeout_ns=500, step_ns=10)

        Fch = _get_bit_from_binstr(uo_str, 0)  # uo_out[0]
        Ych = _get_bit_from_binstr(uo_str, 1)  # uo_out[1]

        assert Fch in "01" and Ych in "01", \
            f"Still X/Z after wait at input {i:03b}: uo_out={uo_str}"

        Fgot = int(Fch)
        Ygot = int(Ych)

        assert Fgot == Fexp, f"Input {i:03b} (A={A},B={B},C={C}) F got={Fgot} exp={Fexp} uo_out={uo_str}"
        assert Ygot == Yexp, f"Input {i:03b} (A={A},B={B},C={C}) Y got={Ygot} exp={Yexp} uo_out={uo_str}"
