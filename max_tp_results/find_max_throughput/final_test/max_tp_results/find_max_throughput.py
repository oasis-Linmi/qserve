import os
import re

def extract_max_throughput_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    throughputs = re.findall(r"Round 2 Throughput:\s+([0-9.]+)\s+tokens\s+/\s+second", content)
    throughputs = [float(tp) for tp in throughputs]

    if throughputs:
        return max(throughputs)
    else:
        return None

def summarize_throughputs(folder_path, output_file):
    with open(output_file, 'w') as out_f:
        out_f.write("文件名\t最大Throughput (tokens/s)\n")
        out_f.write("="*40 + "\n")

        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                max_tp = extract_max_throughput_from_file(file_path)

                if max_tp is not None:
                    out_f.write(f"{filename}\t{max_tp}\n")
                else:
                    out_f.write(f"{filename}\t未找到Throughput\n")

    print(f"汇总完成，结果保存在：{output_file}")

# 使用示例：将下面路径改为你实际的文件夹路径
folder = "/data03/huhuanqi/projects/qserve/max_bs_results/find_max_throughput/final_test/max_tp_results"
output_summary = "throughput_summary.txt"

summarize_throughputs(folder, output_summary)
