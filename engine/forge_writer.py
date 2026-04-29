# /BasicForge/engine/forge_writer.py
# BasicForge Forge Writer
# Created By: David Kistner (Unconditional Love) at GlyphicMind Solutions LLC.



# system imports
import re
from pathlib import Path
from datetime import datetime



# ===========================================
# FORGE WRITER CLASS
# ===========================================
class ForgeWriter:
    """
    ForgeWriter for BasicForge.

    Responsibilities:
    - Accept multi-file BASIC output using REM FILE: markers
    - Write .bas files into storage/pending or storage/saved
    - Inject BasicForge brand tag
    - Log all write operations
    """

    # ----------------------
    # Initialize
    # ----------------------
    def __init__(self, storage_root: Path):
        self.storage_root = storage_root
        self.pending_dir = storage_root / "pending"
        self.saved_dir = storage_root / "saved"
        self.log_file = storage_root / "logs" / "forge.log"

        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.saved_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    # ----------------------
    # Log helper
    # ----------------------
    def _log(self, message: str):
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = f"[{timestamp}] {message}\n"
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(entry)

    # ----------------------
    # Parse multi-file BASIC output
    # ----------------------
    def _split_files(self, code: str):
        """
        Splits BASIC code using:
            REM FILE: filename.bas
        Returns dict: { filename: file_contents }
        """

        pattern = r"REM\s+FILE:\s*([A-Za-z0-9_\-./]+)"
        matches = list(re.finditer(pattern, code, flags=re.IGNORECASE))

        if not matches:
            # Single-file output
            return {"Main.bas": code.strip()}

        files = {}
        for i, match in enumerate(matches):
            filename = match.group(1).strip()
            start = match.end()

            end = matches[i + 1].start() if i + 1 < len(matches) else len(code)
            content = code[start:end].strip()

            files[filename] = content

        return files

    # ----------------------
    # Inject brand tag
    # ----------------------
    def _inject_brand_tag(self, content: str) -> str:
        tag = "REM --- Created with GlyphicMind Solutions: BasicForge ---"
        return f"{tag}\n{content}"

    # ----------------------
    # Write a single file
    # ----------------------
    def _write_file(self, filename: str, content: str, purpose: str):
        path = self.pending_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            path.write_text(content, encoding="utf-8")
            self._log(f"FORGED: {filename} | PURPOSE: {purpose}")
            return True
        except Exception as e:
            self._log(f"ERROR writing {filename}: {e}")
            return False

    # ----------------------
    # Public API: forge_script
    # ----------------------
    def forge_script(self, filename: str, code: str, purpose: str = "") -> bool:
        """
        Writes BASIC code to pending folder.
        Supports multi-file output via REM FILE: markers.
        """

        files = self._split_files(code)

        # If single-file mode, override filename
        if len(files) == 1 and filename:
            only_key = list(files.keys())[0]
            content = files[only_key]
            content = self._inject_brand_tag(content)
            return self._write_file(filename, content, purpose)

        # Multi-file mode
        ok = True
        for fname, content in files.items():
            content = self._inject_brand_tag(content)
            if not self._write_file(fname, content, purpose):
                ok = False

        return ok

