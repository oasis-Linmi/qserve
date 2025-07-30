#!/bin/bash

# 模型路径列表
# MODEL_PATHS=(
#   # "/data03/huhuanqi/projects/qserve/models/Llama-2-7B-QServe"
#   # "/data03/huhuanqi/projects/qserve/models/Llama-2-13B-QServe"
#   # "/data03/huhuanqi/projects/qserve/models/Llama-2-7B-QServe-g128"
#   # "/data03/huhuanqi/projects/qserve/models/Llama-2-13B-QServe-g128"
#   # "/data03/huhuanqi/projects/qserve/models/Llama-3-8B-QServe-g128"
#   # "/data03/huhuanqi/projects/qserve/models/Mistral-7B-v0.1-QServe-g128"
#   # "/data03/huhuanqi/projects/qserve/models/Yi-34B-QServe-g128"
# )
# export CUDA_VISIBLE_DEVICES=6
# # 全局设置
# PRECISION="w4a8kv4"
# GROUP_SIZE=128
# export GLOBAL_BATCH_SIZE=64
# # 循环遍历每个模型路径
# for MODEL_PATH in "${MODEL_PATHS[@]}"; do
#   echo "Testing model: $MODEL_PATH"
  
#   # 执行基准测试
#   python qserve_benchmark.py \
#     --model "$MODEL_PATH" \
#     --benchmarking \
#     --precision "$PRECISION" \
#     --group-size "$GROUP_SIZE" \

  
#   # 检查命令是否成功
#   if [ $? -ne 0 ]; then
#     echo "Benchmarking failed for model: $MODEL_PATH"
#     exit 1
#   fi
  
#   echo "Benchmarking completed for model: $MODEL_PATH"
# done

# echo "All models have been tested successfully."

import os
import subprocess

# 模型路径列表（根据需要取消注释或添加）
model_paths = [
    # "/data03/huhuanqi/projects/qserve/models/Llama-2-7B-QServe",
    # "/data03/huhuanqi/projects/qserve/models/Llama-2-13B-QServe",
    "/data04/huhuanqi/models/Llama-2-7B-QServe-g128",
    "/data04/huhuanqi/models/Llama-2-13B-QServe-g128",
    "/data04/huhuanqi/models/Llama-3-8B-QServe-g128",
    "/data04/huhuanqi/models/Mistral-7B-v0.1-QServe-g128",
    "/data04/huhuanqi/models/Yi-34B-QServe-g128",
    "/data04/huhuanqi/models/QServe-models-made-by-hq/QServeModel/qserve-llama-30b-g128/llama-30b-w4a8",
    "/data04/huhuanqi/models/QServe-models-made-by-hq/QServeModel/qserve-llama2-70b-g128/Llama-2-70b-hf-w4a8"
]

# 全局设置
precision = "w4a8kv4"
group_size = 128
# batch_sizes = [1, 2, 4, 8, 16, 32, 64]
# batch_sizes = [256]
# batch_sizes = [_ for _ in range(0, 257, 4)]
# max_batch_size_base = [188, 148, 144, 144, 100, 76, 72]
max_batch_size_upper = [190, 151, 146, 146, 102, 77, 73]
# batch_sizes[0] = 1
# 设置CUDA设备为7号GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "7"
# os.environ["NUM_GPU_PAGE_BLOCKS"] = "1600"

# 遍历每个模型路径
for model_index, model_path in enumerate(model_paths):
    print(f"Testing model: {model_path}")
    
    
    output_filename = model_path.replace("/", "_").lstrip("_") + "_find_max_tp.txt"
    test_batch_size_upper = max_batch_size_upper[model_index]
    test_batch_sizes = [_ for _ in range(4, test_batch_size_upper + 10, 4)]
    with open(output_filename, "a") as f:
        for batch in test_batch_sizes:
            # 构建命令（假设 qserve_benchmark.py 接受 --batch-size 参数）
            os.environ["GLOBAL_BATCH_SIZE"] = str(batch)
            os.environ["NUM_GPU_PAGE_BLOCKS"] = str(batch * 25)
            command = (
                f"python /data03/huhuanqi/projects/qserve/qserve_benchmark.py "
                f"--model \"{model_path}\" "
                f"--benchmarking "
                f"--precision {precision} "
                f"--group-size {group_size} "
            )
            f.write(f"Running command: {command}\n")
            print(f"Running: {command}")
            
            # 执行命令并捕获输出
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 将输出写入文件
            f.write(result.stdout.decode())
            f.write(result.stderr.decode())
            f.write("\n" + "="*50 + "\n")
            
            # 如果命令执行失败，写入错误信息（可根据需求决定是否终止脚本）
            if result.returncode != 0:
                f.write(f"Benchmarking failed for model: {model_path} with batch size {batch}\n")
                print(f"Benchmarking failed for model: {model_path} with batch size {batch}")
                break
                # 如有需要可以选择退出：exit(1)
    
    print(f"Benchmarking completed for model: {model_path}. Output saved in {output_filename}")

print("All models have been tested successfully.")
