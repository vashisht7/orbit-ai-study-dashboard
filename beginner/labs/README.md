# Small, inspectable AI experiments

Begin with lesson_01.py and follow the reader in order. Lessons 01-29 use Python's standard library only. Run, for example, `python3 lesson_06.py`. Predict the result first, change one value, and explain what changed.

The examples use synthetic data and mocked actions. They do not contact model services, create reminders, change NoteEchoes or establish production quality.

## Optional transformer

Open chapter 30 after chapters 2-12. Create an isolated environment and install PyTorch and NumPy, then run:

    python tiny_decoder.py --steps 40
    python tiny_decoder.py --steps 40 --lr 0.001

The default run was verified with Python 3.12.14 and PyTorch 2.8.0 on CPU. It has 14,962 trainable parameters. In the recorded default run, training loss fell from 3.0724 to 1.4512 over 40 steps, and the causal-invariance check passed. Numerical results can vary across versions and platforms. The repeated synthetic corpus is not an independent evaluation dataset, and generated text is intentionally not production quality.

Try --width, --heads, --layers, --context, --steps, --lr and --seed. Change one at a time. Width must be divisible by heads in this implementation. Run --help for defaults.

## Reading progress

Use the browser's Mark practiced button only after you have predicted, run and changed an example. Progress is stored in that browser; it does not sync between devices.
