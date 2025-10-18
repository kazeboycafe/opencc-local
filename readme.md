# 📘 Chinese DOCX Converter

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Convert Simplified Chinese ↔ Traditional Chinese in `.docx` files **while preserving all text formatting** (bold, italic, font, color, etc.), with built-in support for **Chinese characters commonly used in Macau**.


---

## ✨ Features

- **Preserves all formatting**: Processes text at the *run level* — no loss of bold, italic, font size, color, etc.
- **Macau-ready conversion**:  
  - `s2mo` mode: Converts Simplified → Hong Kong Traditional → **Macau-adjusted** via custom JSON dictionary
- **Flexible I/O**:  
  - Input: `.docx` file (required)  
  - Output: Auto-generated if omitted (`input.docx` → `input(t).docx` or `input(s).docx`)
- **Full table support**: Handles nested tables recursively


---

## 🛠️ Installation

### 1. Clone or download this repository
```bash
git clone https://github.com/kazeboycafe/opencc-word.git
cd opencc-word
```

### 2. Install dependencies
```bash
pip install python-docx opencc
```

> ⚠️ **Note**: Only `.docx` files are supported (not legacy `.doc`). The script will warn you if `.doc` is used.

---


### 🔧 Customize `hk2mo.json`
Define Chinese characters commonly used in Macau:

```json
{
  "衞": "衛"
}
```

> Add or modify entries to match your preferred Chinese characters.

---

## ▶️ Usage

### Basic: Simplified → Macau Traditional (auto output)
```bash
python opencc_word.py input.docx
# Output: input(t).docx
```

### Specify output filename
```bash
python opencc_word.py input.docx output.docx
```

### Traditional → Simplified
```bash
python opencc_word.py input.docx --type t2s
# Output: input(s).docx
```

### Full command syntax
```bash
python opencc_word.py <input.docx> [output.docx] [--type s2mo|t2s]
```

### Options
| Argument | Description |
|--------|-------------|
| `input` | Input `.docx` file (**required**) |
| `output` | Output file (optional; auto-generated if omitted) |
| `--type` | Conversion mode:<br>• `s2mo` (default): Simplified → Macau Traditional<br>• `t2s`: Traditional → Simplified |

---

## 🔄 How It Works

### `s2mo` Mode (Simplified → Macau)
1. Uses OpenCC’s `s2hk` profile to convert to **Hong Kong Traditional Chinese**
2. Applies custom replacements from `hk2mo.json` for **Macau-specific terms**

### `t2s` Mode (Traditional → Simplified)
- Uses OpenCC’s standard `t2s` conversion (no JSON post-processing)

---

## 📌 Limitations

- ❌ Does **not** process headers, footers, footnotes, or text boxes  
- ❌ Only supports `.docx` (not legacy `.doc`)  
- ❌ Replacements are exact string matches (no regex or word-boundary logic)

> 💡 **Tip**: For complex documents, consider converting headers/footers manually or using Microsoft Word’s built-in converter for those sections.


---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
