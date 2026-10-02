import math
input_width = output_width = 1024
rank, alpha = 32, 64
full = input_width * output_width
adapter = rank * (input_width + output_width)
print(full, adapter)  # 1048576 65536
print("standard scale:", alpha / rank)       # 2.0
print("rsLoRA scale:", alpha / math.sqrt(rank))  # about 11.31
