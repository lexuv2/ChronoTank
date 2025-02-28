import chronotank
import adapters.bin_with_args_perf as base_adapters

bin_path = "perf stat qemu-arm /home/lexu/Documents/RE/pingCTF-2025/pwn/tick-tock/private/main_arm"

adapter = base_adapters.BinWithArgsPerf(bin_path, "Found Flag")
ch = chronotank.ChronoTank(adapter,batch_size=64,max_flag_len=44)


res = []

for i, avg_time in ch.get_flag():
    res.append((i, avg_time))
    print(i, avg_time)
    # ch.update_plot()

