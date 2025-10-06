import m5
from m5.objects import *
import argparse

# Define a custom FU Pool to easily modify latencies
class MyFUPool(MinorFUPool):
    def __init__(self, opLat, issueLat):
        super().__init__()
        
        # This is a simplified pool. A real one would have more units.
        self.IntALU = MinorIntALU()
        self.IntMultDiv = MinorIntMultDiv()
        self.MemRead = MinorMemRead()
        self.MemWrite = MinorMemWrite()
        
        # Define the custom Float/SIMD unit
        self.FloatSimdFU = MinorFloatSimdFU()
        self.FloatSimdFU.opLat = opLat
        self.FloatSimdFU.issueLat = issueLat

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='Run a multi-threaded workload on MinorCPU.')
parser.add_argument("--num-cpus", type=int, default=1, help="Number of CPU cores")
parser.add_argument("--opLat", type=int, default=4, help="Operation latency for FloatSimdFU")
parser.add_argument("--issueLat", type=int, default=4, help="Issue latency for FloatSimdFU")
parser.add_argument("--cmd", type=str, required=True, help="The workload to run")
args = parser.parse_args()

# --- System Setup ---
system = System()
system.clk_domain = SrcClockDomain(clock='3GHz', voltage_domain=VoltageDomain())
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('2GB')]

# Create a list of CPUs
fu_pool = MyFUPool(opLat=args.opLat, issueLat=args.issueLat)
system.cpu = [MinorCPU(cpu_id=i, fuPool=fu_pool) for i in range(args.num_cpus)]

# Create a memory bus and connect caches
system.membus = SystemXBar()
for i in range(args.num_cpus):
    system.cpu[i].icache = Cache(size='32kB', assoc=2)
    system.cpu[i].dcache = Cache(size='32kB', assoc=2)
    system.cpu[i].icache.connectCPU(system.cpu[i])
    system.cpu[i].dcache.connectCPU(system.cpu[i])
    system.cpu[i].icache.connectBus(system.membus)
    system.cpu[i].dcache.connectBus(system.membus)
    system.cpu[i].createInterruptController()

# Memory Controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

# --- Workload Setup ---
process = Process()
process.cmd = [args.cmd]
for cpu in system.cpu:
    cpu.workload = process
    cpu.createThreads()

# --- Simulation ---
root = Root(full_system=False, system=system)
m5.instantiate()

print("**** REAL SIMULATION ****")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")
