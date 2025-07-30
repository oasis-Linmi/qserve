import os
import subprocess

# 模型路径与对应 batch size
models = [
    ("/data04/huhuanqi/models/Llama-3-8B-QServe-g128", 256),
    ("/data04/huhuanqi/models/Llama-2-7B-QServe-g128", 190),
    ("/data04/huhuanqi/models/Mistral-7B-v0.1-QServe-g128", 256),
    ("/data04/huhuanqi/models/Llama-2-13B-QServe-g128", 128),
    ("/data04/huhuanqi/models/QServe-models-made-by-hq/QServeModel/qserve-llama-30b-g128/llama-30b-w4a8", 64),
    ("/data04/huhuanqi/models/Yi-34B-QServe-g128", 196),
    ("/data04/huhuanqi/models/QServe-models-made-by-hq/QServeModel/qserve-llama2-70b-g128/Llama-2-70b-hf-w4a8", 96),
    ("/data04/huhuanqi/models/Qwen-1.5-72B-QServe-g128", 32),
]

for model_path, batch_size in models:
    num_blocks = 25 * batch_size
    env = os.environ.copy()
    env["GLOBAL_BATCH_SIZE"] = str(batch_size)
    env["NUM_GPU_PAGE_BLOCKS"] = str(num_blocks)

    command = [
        "python", "qserve_benchmark.py",
        "--model", model_path,
        "--benchmarking",
        "--precision", "w4a8kv4",
        "--group-size", "128"
    ]

    print(f"\nRunning benchmark for model: {model_path}")
    print(f"Batch Size: {batch_size}, NUM_GPU_PAGE_BLOCKS: {num_blocks}")
    subprocess.run(command, env=env)
