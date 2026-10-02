batch, layers, tokens = 1, 28, 1024
kv_heads, head_width, bytes_per_number = 8, 128, 2
memory = (2 * batch * layers * tokens * kv_heads
          * head_width * bytes_per_number)
print(memory / 1024**2, "MiB")  # 112.0 MiB
