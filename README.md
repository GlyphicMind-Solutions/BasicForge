# ⭐ BasicForge — Basic Code Forge
- Created By: David Kistner (Unconditional Love)  
- GlyphicMind Solutions LLC

## Overview
BasicForge is a standalone Forge‑Suite tool designed to generate, refactor, analyze, and manage BASIC code using an AI‑assisted workflow.
It supports both Modern BASIC (SUB/FUNCTION, no line numbers) and Classic BASIC (line‑numbered, GOTO/GOSUB) with Auto‑Detect Mode built directly into the GUI. BasicForge follows the same tabbed IDE layout and workflow conventions as PythonForge, GoForge, RustForge, KotlinForge, JavaForge, and the rest of the Forge ecosystem.

- BasicForge supports:
1. Modern BASIC (structured, SUB/FUNCTION)
2. Classic BASIC (line‑numbered, GOTO/GOSUB)
3. Auto‑detect BASIC mode
4. Multi‑file output using REM FILE: markers
5. Deep Analysis v2 (chunk → summarize → meta‑summarize → reconstruct)
6. Full GUI workflow with topic, corrections, raw output, extracted code, master code, and logs
7. Pending/saved file management with brand‑tag injection
8. Model‑family‑aware prompt building (GPT, Mistral, Qwen, DeepSeek, Phi, Llama)
GoForge is part of the GlyphicMind Solutions Forge Suite, alongside PythonForge, JavaScriptForge, CSharpForge, CppForge, JavaForge, and RustForge.

---

## 🚀 Features

### Dual BASIC Mode Support
BasicForge supports three modes:
1. Auto Detect — analyzes the code and chooses the correct style
2. Modern BASIC — SUB/FUNCTION, structured flow, no line numbers
3. Classic BASIC — line numbers, GOTO/GOSUB, retro style
Mode selection is available via three radio buttons in the GUI.

### 🔥 Local‑First LLM Execution
JavaForge loads `.gguf` models defined in:
```
models/manifest.yaml

```

Supports:
- GPT‑OSS  
- Mistral  
- Llama  
- Qwen  
- DeepSeek  
- Phi  
- Any LocalAI‑compatible `.gguf` model  


### 🧠 Deep Analysis v2
JavaForge includes the upgraded Deep Analysis engine:

- Splits large codebases into chunks  
- Summarizes each chunk  
- Produces a meta‑summary  
- Reconstructs/refactors the entire project  
- Logs every step in the Deep Analysis Log tab  


### 🧩 Multi‑File Output
GoForge automatically detects and writes multiple files when the model outputs:
```
REM FILE: Main.bas
REM FILE: Utils.bas
REM FILE: Program1.bas
```

### 🖥️ Full GUI (PyQt5)

- Tabbed IDE layout:
   1. Topic / Corrections
   2. Raw LLM Output
   3. Extracted Code
   4. Master Code
   5. Deep Analysis Log

- Global controls:
   1. Generate
   2. Re‑run with Corrections
   3. Deep Analysis
   4. Open File
   5. Save File
   6. Forge → Pending
   7. Clear Session


### 🗂️ Storage System

BasicForge organizes output into:

```
storage/
    pending/   ← forged files awaiting review
    saved/     ← user‑saved files
    logs/      ← forge.log + deep analysis logs
```

---

## ⭐ Installation

1. Create a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Add your .gguf models
Place them in:
```
models/
```
Then update:
```
models/manifest.yaml
```


## ⭐ Running BasicForge

In your terminal, or Command Prompt type in your directory:
```
python3 basicforge.py
```


### ⭐ Model Manifest Example
```
models:
  mistral_default:
    path: ./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf <--- you can change this to the directory of your model
    n_ctx: 32768
    template: mistral
```


---

# ⭐ Part of the GlyphicMind Forge Suite

BasicForge is one of many Forge tools:

1. ✅️ PythonForge

2. ✅️ JavaScriptForge

3. ✅️ CSharpForge

4. ✅️ CppForge

5. ✅️ JavaForge

6. ✅️ RustForge

7. ✅️ GoForge

8. ✅️ KotlinForge

9. ✅️ BasicForge

8. HTML/CSS Forge (coming soon)

9. SQLForge (coming soon)

--All tools follow the same architecture, branding, and workflow.

---

### ⭐License

This project is part of the GlyphicMind Solutions ecosystem.
All rights reserved.
