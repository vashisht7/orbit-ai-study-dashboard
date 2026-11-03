# Train your first tiny language model

This workshop trains a real, small decoder Transformer using PyTorch on a CPU. It learns to predict the next **character**, not a production BPE token. The included short stories are original teaching fixtures. Expect fragments and memorization, not a capable assistant. Use your own permitted UTF-8 text for a more meaningful experiment.

## Write it yourself in a notebook

Open `Write_Your_Transformer.ipynb` for unfinished implementation cells, explanations, shape checks, two controlled training runs, loss plots, generation, and model export. Use `Transformer_Reference.ipynb` only after trying each exercise. Both include the teaching text and work in local JupyterLab, VS Code with the Python/Jupyter extensions, or Colab.

After activating your Python environment:

```sh
python -m pip install -r requirements-notebook.txt
python -m jupyterlab Write_Your_Transformer.ipynb
```

In Colab, upload the notebook and run its setup instructions. GPU access is optional and not required by this starter. Keep downloads of your work before the session ends.

The dashboard's **Inside the model** page animates computed attention, residual connections, and feed-forward neuron calculations. Its live next-word training experiment is a small bigram model implemented in JavaScript. The full PyTorch Transformer runs in your notebook or Python terminal, not in the static dashboard. No extra animation plugin is required.

The notebook saves `notebook_weights.pt` for inference and exports `notebook-run/metrics.json` for the dashboard. Its weights file is not compatible with `train.py --resume`; the script below separately saves its complete training checkpoint.

## Run the reference script

Download and extract the workshop ZIP from the dashboard. Open a terminal in the extracted folder.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python train.py --steps 200 --out run
```

On Windows, activate with `.venv\Scripts\activate` and use `python` instead of `python3` if needed.

No API key or GPU is needed. Installing PyTorch needs internet access. Runtime depends on your computer. The browser diagrams illustrate the calculations; actual Transformer training happens when you run this Python script.

## What the code does

1. **Text → IDs.** Read text, reserve its final 10% for validation, and build a character vocabulary from the training region. Unknown validation characters map to ID 0.
2. **IDs → vectors.** Token embeddings represent characters; position embeddings distinguish their locations. These are learned parameters.
3. **Vectors → context.** Queries and keys produce scores, scaled by the square root of the head width. Mask future positions, apply softmax, and use those weights to mix value vectors.
4. **Context → logits.** Residual attention and feed-forward blocks refine vectors. The output layer produces one score per vocabulary character at every position.
5. **Logits → loss.** Targets are the input shifted by one character. Cross-entropy penalizes assigning low probability to the actual next character.
6. **Loss → updates.** Clear old gradients, backpropagate, clip gradients, then use AdamW to update weights. `loss.backward()` computes gradients; `optimizer.step()` changes weights.
7. **Evaluate and save.** Compare fixed held-out windows periodically. Save parameters, optimizer state, random state, configuration, corpus fingerprint, and metrics.
8. **Generate.** Use the last position's scores, divide by temperature, sample one character, append it, and repeat. Generation does not update the model weights.

With defaults, the input shape is `[8,64]`; embeddings are `[8,64,64]`; logits are `[8,64,vocabulary_size]`. Width 64 splits into four heads of width 16. Each block has a causal mask: an earlier position cannot use a future character.

## See and resume your results

`run/metrics.json` contains measured losses. Import it into the dashboard's training workshop to plot your actual run. `run/sample.txt` contains generated text. `run/checkpoint.pt` lets you continue:

```sh
python train.py --steps 200 --resume run/checkpoint.pt --out run
```

Steps are **additional** steps. Resume uses the same text, architecture, batch size, and learning rate. Load only checkpoints you created yourself: this educational checkpoint format uses Python pickle.

## Try a controlled experiment

```sh
python train.py --steps 200 --lr 0.001 --out slower
python train.py --text my-stories.txt --steps 1000 --out my-model
```

Compare runs with the same corpus, split, seed, and number of updates when studying learning rate. For a changed corpus, those losses are not directly comparable. Keep an independent final test set if you tune repeatedly on validation.

Ask: does training loss fall while validation loss rises? Is generated text copied? Does the model produce coherent new sentences? The supplied corpus is tiny and related throughout. A contiguous split prevents overlapping training windows across the boundary, but does not eliminate duplicates or source leakage. For serious evaluation, split by independent source/document and inspect near duplicates.

## What comes next

First explain and modify this implementation. Then follow https://github.com/FareedKhan-dev/train-llm-from-scratch for larger natural-text training, modern architecture, and post-training. This workshop covers pretraining and generation; SFT and preference training remain a separate next stage.
