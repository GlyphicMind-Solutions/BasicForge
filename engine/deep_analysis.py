# /BasicForge/engine/deep_analysis.py
# BasicForge Deep Analysis Engine (Modern + Classic BASIC)
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import re, json
from datetime import datetime
from pathlib import Path



# ===========================================
# DEEP ANALYSIS ENGINE
# ===========================================
class DeepAnalysisEngine:
    """
    DeepAnalysisEngine for BasicForge.

    Supports:
    - Modern BASIC (SUB/FUNCTION, no line numbers)
    - Classic BASIC (line numbers, GOTO/GOSUB)
    - Auto-detect mode
    - Chunk → Summarize → Meta-Summarize → Reconstruct pipeline
    - Full Deep Analysis v2 logging
    """

    # ----------------------
    # Initialize
    # ----------------------
    def __init__(self, prompt_builder, llm_engine, model_fast, model_smart, basic_mode="auto"):
        self.prompt_builder = prompt_builder
        self.llm = llm_engine
        self.model_fast = model_fast
        self.model_smart = model_smart
        self.basic_mode = basic_mode  # "auto", "modern", "classic"

        self._log = []

    # ----------------------
    # Logging helper
    # ----------------------
    def _log_stage(self, stage, message, **extra):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "stage": stage,
            "message": message,
        }
        entry.update(extra)
        self._log.append(entry)

    # ----------------------
    # Get Log
    # ----------------------
    def get_log(self):
        return self._log

    # ----------------------
    # BASIC Mode Detection
    # ----------------------
    def _detect_basic_mode(self, code: str) -> str:
        """
        Auto-detect BASIC style:
        - Classic BASIC: line numbers, GOTO, GOSUB
        - Modern BASIC: SUB/FUNCTION, no line numbers
        """
        if self.basic_mode != "auto":
            return self.basic_mode

        # Classic BASIC detection
        if re.search(r"^\d+\s+", code, flags=re.MULTILINE):
            return "classic"
        if re.search(r"\bGOTO\b|\bGOSUB\b", code, flags=re.IGNORECASE):
            return "classic"

        # Modern BASIC detection
        if re.search(r"\bSUB\b|\bFUNCTION\b", code, flags=re.IGNORECASE):
            return "modern"

        # Default to modern if ambiguous
        return "modern"

    # ----------------------
    # Chunk Code
    # ----------------------
    def _chunk_code(self, code: str, max_chars=4000):
        chunks = []
        while code:
            chunks.append(code[:max_chars])
            code = code[max_chars:]
        return chunks

    # ----------------------
    # Summarize a chunk
    # ----------------------
    def _summarize_chunk(self, chunk: str, mode: str):
        prompt = self.prompt_builder.build_chunk_summary_prompt(
            code_chunk=chunk,
            basic_mode=mode,
        )
        raw = self.llm.generate(prompt, model_key=self.model_fast)
        return raw.split("FIN~")[0].strip()

    # ----------------------
    # Merge summaries
    # ----------------------
    def _merge_summaries(self, summaries: list, mode: str):
        combined = "\n\n".join(summaries)
        prompt = self.prompt_builder.build_meta_summary_prompt(
            summaries=combined,
            basic_mode=mode,
        )
        raw = self.llm.generate(prompt, model_key=self.model_fast)
        return raw.split("FIN~")[0].strip()

    # ----------------------
    # Final reconstruction
    # ----------------------
    def _reconstruct(self, meta_summary: str, mode: str):
        prompt = self.prompt_builder.build_analysis_from_summary_prompt(
            meta_summary=meta_summary,
            basic_mode=mode,
        )
        raw = self.llm.generate(prompt, model_key=self.model_smart)
        return raw.split("FIN~")[0].strip()

    # ----------------------
    # Run full pipeline
    # ----------------------
    def run(self, code: str):
        self._log.clear()

        # Detect BASIC mode
        mode = self._detect_basic_mode(code)
        self._log_stage("detect_mode", f"Detected BASIC mode: {mode}")

        # Chunk
        chunks = self._chunk_code(code)
        self._log_stage("chunk", f"Chunked into {len(chunks)} chunks")

        summaries = []
        for i, chunk in enumerate(chunks):
            summary = self._summarize_chunk(chunk, mode)
            summaries.append(summary)
            self._log_stage("chunk_summary", f"Summarized chunk {i}", summary=summary)

        # Merge summaries
        meta = self._merge_summaries(summaries, mode)
        self._log_stage("meta_summary", "Merged summaries", meta=meta)

        # Reconstruct
        corrected = self._reconstruct(meta, mode)
        self._log_stage("reconstruct", "Reconstructed BASIC code", corrected=corrected)

        return corrected

