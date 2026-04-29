# /BasicForge/prompt/prompt_builder.py
# BasicForge Prompt Builder (model-family aware)
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import re



# ==========================================
# PROMPT BUILDER CLASS
# ==========================================
class PromptBuilder:
    """
    PromptBuilder
        - Builds model-family-aware prompts for BasicForge.
        - Output: BASIC code ONLY. No markdown. End with FIN~.
        - Supports multi-file output using REM FILE: markers.
        - Supports Modern BASIC and Classic BASIC modes.
    """
    # -------------------------
    # Build Prompt
    # -------------------------
    def build_prompt(self, topic: str, model_key: str, basic_mode: str = "auto") -> str:
        family = self._infer_family(model_key)

        if family == "gpt":
            return self._build_gpt_prompt(topic, basic_mode)
        if family == "mistral":
            return self._build_mistral_prompt(topic, basic_mode)
        if family == "qwen":
            return self._build_qwen_prompt(topic, basic_mode)
        if family == "deepseek":
            return self._build_deepseek_prompt(topic, basic_mode)
        if family == "phi":
            return self._build_phi_prompt(topic, basic_mode)

        # default → llama-style
        return self._build_llama_prompt(topic, basic_mode)

    # -------------------------
    # Infer Family
    # -------------------------
    def _infer_family(self, model_key: str) -> str:
        k = model_key.lower()

        if "gpt" in k:
            return "gpt"
        if "mistral" in k:
            return "mistral"
        if "qwen" in k:
            return "qwen"
        if "deepseek" in k:
            return "deepseek"
        if "phi" in k:
            return "phi"
        if "llama" in k or "hermes" in k:
            return "llama"

        return "llama"

# ==========================================
# TEMPLATE SECTION
# ==========================================
    # -------------------------
    # GPT template
    # -------------------------
    def _build_gpt_prompt(self, topic: str, mode: str) -> str:
        return (
            "<|start|>system<|message|>\n"
            "\"You are an Agent using BasicForge.\"\n"
            "\"Rules:\"\n"
            "\"1. All reasoning stays inside assistant analysis channel.\"\n"
            "\"2. Final output is pure BASIC code in assistant final channel.\"\n"
            "\"3. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"4. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"5. No markdown, no commentary, no backticks.\"\n"
            "\"6. Generate BASIC code ONLY.\"\n"
            "\"7. When you are complete end with FIN~.\"\n"
            f"\"8. BASIC Mode for this task: {mode}.\"\n"
            "<|end|>\n\n"
            "<|start|>user<|message|>\n"
            f"{topic}\n"
            "<|end|>\n\n"
            "<|start|>assistant<|channel|>analysis<|message|>\n"
            "...\n"
            "<|end|>\n\n"
            "<|start|>assistant<|channel|>final<|message|>\n"
        )

    # -------------------------
    # Mistral template
    # -------------------------
    def _build_mistral_prompt(self, topic: str, mode: str) -> str:
        return (
            "<|im_start|>system\n"
            "[INST]\n"
            "You are an Agent using BasicForge."
            "\"Rules:\"\n"
            "\"1. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"2. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"3. No markdown, no commentary, no backticks.\"\n"
            "\"4. Generate BASIC code ONLY.\"\n"
            "\"5. When you are complete end with FIN~.\"\n"
            f"\"6. BASIC Mode for this task: {mode}.\"\n"
            "[/INST]\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

    # -------------------------
    # Qwen template
    # -------------------------
    def _build_qwen_prompt(self, topic: str, mode: str) -> str:
        return (
            "<|im_start|>system\n"
            "You are an Agent using BasicForge."
            "\"Rules:\"\n"
            "\"1. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"2. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"3. No markdown, no commentary, no backticks.\"\n"
            "\"4. Generate BASIC code ONLY.\"\n"
            "\"5. When you are complete end with FIN~.\"\n"
            f"\"6. BASIC Mode for this task: {mode}.\"\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

    # -------------------------
    # DeepSeek template
    # -------------------------
    def _build_deepseek_prompt(self, topic: str, mode: str) -> str:
        return (
            "<|begin_of_text|><|system|>\n"
            "You are an Agent using BasicForge."
            "\"Rules:\"\n"
            "\"1. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"2. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"3. No markdown, no commentary, no backticks.\"\n"
            "\"4. Generate BASIC code ONLY.\"\n"
            "\"5. When you are complete end with FIN~.\"\n"
            f"\"6. BASIC Mode for this task: {mode}.\"\n"
            "<|end|>\n\n"
            "<|user|>\n"
            f"{topic}\n"
            "<|end|>\n\n"
            "<|assistant|>\n"
        )

    # -------------------------
    # Phi template
    # -------------------------
    def _build_phi_prompt(self, topic: str, mode: str) -> str:
        return (
            "### System\n"
            "You are an Agent using BasicForge."
            "\"Rules:\"\n"
            "\"1. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"2. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"3. No markdown, no commentary, no backticks.\"\n"
            "\"4. Generate BASIC code ONLY.\"\n"
            "\"5. When you are complete end with FIN~.\"\n"
            f"\"6. BASIC Mode for this task: {mode}.\"\n"
            "### User\n"
            f"{topic}\n\n"
            "### Assistant\n"
        )

    # -------------------------
    # Llama / default template
    # -------------------------
    def _build_llama_prompt(self, topic: str, mode: str) -> str:
        return (
            "<|im_start|>system\n"
            "You are an Agent using BasicForge."
            "\"Rules:\"\n"
            "\"1. Use REM FILE: markers for multi-file BASIC output.\"\n"
            "\"2. BASIC Mode: auto-detect, modern, or classic.\"\n"
            "\"3. No markdown, no commentary, no backticks.\"\n"
            "\"4. Generate BASIC code ONLY.\"\n"
            "\"5. When you are complete end with FIN~.\"\n"
            f"\"6. BASIC Mode for this task: {mode}.\"\n"
            "<|im_end|>\n\n"
            "<|im_start|>user\n"
            f"{topic}\n"
            "<|im_end|>\n\n"
            "<|im_start|>assistant\n"
        )

    # ==========================================
    # DEEP ANALYSIS PROMPTS
    # ==========================================

    # -------------------------
    # Chunk Summary Prompt
    # -------------------------
    def build_chunk_summary_prompt(self, code_chunk: str, basic_mode: str) -> str:
        return (
            f"Summarize the following BASIC code chunk.\n"
            f"BASIC Mode: {basic_mode}\n"
            "Focus on logic, variables, flow, and structure.\n"
            "Do NOT output code. Provide a structured summary only.\n"
            "End with FIN~.\n\n"
            f"{code_chunk}\n\nFIN~"
        )

    # -------------------------
    # Meta Summary Prompt
    # -------------------------
    def build_meta_summary_prompt(self, summaries: str, basic_mode: str) -> str:
        return (
            f"Merge the following BASIC code summaries into a single meta-summary.\n"
            f"BASIC Mode: {basic_mode}\n"
            "Do NOT output code. Provide a unified summary.\n"
            "End with FIN~.\n\n"
            f"{summaries}\n\nFIN~"
        )

    # -------------------------
    # Reconstruction Prompt
    # -------------------------
    def build_analysis_from_summary_prompt(self, meta_summary: str, basic_mode: str) -> str:
        return (
            f"Reconstruct BASIC code from the following meta-summary.\n"
            f"BASIC Mode: {basic_mode}\n"
            "Rules:\n"
            "- Output BASIC code ONLY.\n"
            "- No markdown, no commentary.\n"
            "- Use REM FILE: markers for multi-file output.\n"
            "- End with FIN~.\n\n"
            f"{meta_summary}\n\nFIN~"
        )

