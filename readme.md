# 📘 Chinese DOCX Converter

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Convert Simplified Chinese ↔ Traditional Chinese in `.docx` files **while preserving all text formatting** (bold, italic, font, color, etc.), with built-in support for **Macau-specific terminology**.

Perfect for legal, government, academic, or business documents requiring accurate regional Chinese variants.

---

## ✨ Features

- **Preserves all formatting**: Processes text at the *run level* — no loss of bold, italic, font size, color, etc.
- **Macau-ready conversion**:  
  - `s2mo` mode: Converts Simplified → Hong Kong Traditional → **Macau-adjusted** via custom JSON dictionary
- **Flexible I/O**:  
  - Input: `.docx` file (required)  
  - Output: Auto-generated if omitted (`report.docx` → `report(t).docx` or `report(s).docx`)
- **Full table support**: Handles nested tables recursively
- **Simple CLI**: Easy to use from terminal or integrate into workflows

---

## 🛠️ Installation

### 1. Clone or download this repository
```bash
git clone https://github.com/your-username/chinese-docx-convert.git
cd chinese-docx-convert
```

### 2. Install dependencies
```bash
pip install python-docx opencc-python-reimplemented
```

> ⚠️ **Note**: Only `.docx` files are supported (not legacy `.doc`). The script will warn you if `.doc` is used.

---

## 📁 Project Structure

```
chinese-docx-convert/
├── convert.py              # Main conversion script
├── hk2mo.json              # Macau terminology overrides (required for s2mo mode)
├── README.md
└── LICENSE
```

### 🔧 Customize `hk2mo.json`
Define your Macau-specific word replacements:

```json
{
  "軟件": "軟體",
  "打印機": "印表機",
  "鼠標": "滑鼠",
  "服務器": "伺服器",
  "人工智能": "人工智慧",
  "程序員": "程式員"
}
```

> Add or modify entries to match your organization's preferred terminology.

---

## ▶️ Usage

### Basic: Simplified → Macau Traditional (auto output)
```bash
python convert.py input.docx
# Output: input(t).docx
```

### Specify output filename
```bash
python convert.py report.docx macau_report.docx
```

### Traditional → Simplified
```bash
python convert.py traditional.docx
# Output: traditional(s).docx
```

### Full command syntax
```bash
python convert.py <input.docx> [output.docx] [--type s2mo|t2s]
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

## 🚀 Example Workflow

1. Prepare your `hk2mo.json` with Macau-preferred terms
2. Run:
   ```bash
   python convert.py application_form.docx
   ```
3. Get `application_form(t).docx` with:
   - Accurate Traditional Chinese conversion
   - Localized Macau terminology
   - All original formatting preserved

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR for:
- Support for headers/footers
- Regex-based replacement engine
- Additional regional profiles (e.g., `s2tw` for Taiwan)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

> Made with ❤️ for Macau and Greater China localization workflows.  
> Questions? Open an [Issue](https://github.com/your-username/chinese-docx-convert/issues)!