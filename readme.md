# 📘 Simplified <-> Traditional Chinese .docx Converter

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-WTFPL-blue.svg)](LICENSE)

Convert Simplified Chinese <-> Traditional Chinese in `.docx` files **while preserving all text formatting** (bold, italic, font, color, etc.) and runs opencc locally with webpage interface, with built-in support for further replacing text with **Chinese characters commonly used in Macau**.

---

## ✨ Features

- **Preserves all formatting**: Processes text at the *run level* — no loss of bold, italic, font size, color, etc.
- **Macau-ready conversion**: Converts Simplified → Hong Kong Traditional → **Macau-adjusted** via custom JSON dictionary
- **Flexible I/O**:  
  - Input: `.docx` file (required)  
  - Output: Auto-generated (`input.docx` → `input(t).docx` or `input(s).docx`)
- **Full table support**: Handles nested tables recursively


---

## 🛠️ Installation and How to Use

### 1. Clone or download this repository
```bash
git clone https://github.com/kazeboycafe/opencc-local.git
cd opencc-local
```

### 2. Install dependencies
```bash
pip install python-docx opencc flask
```

> ⚠️ **Note**: Only `.docx` files are supported (not legacy `.doc`). The script will warn you if `.doc` is used.

### 3. Start the server
```bash
python server.py
```
> ⚠️ or you may just use the server.sh to start the server

### 4. Open the webpage interface
Open the opencc_local.url, which is http://localhost:15733/

> ⚠️ or you may just use the launch.sh to start the server and open the webpage

---



### 🔧 Customize `hk2mo.json`
Define Chinese characters commonly used in Macau:

```json
{
  "衞": "衛",
  "羣": "群",
  "户": "戶",
}
```

> Add or modify entries to match your preferred Chinese characters.

---

## 🔄 How It Works

### Simplified → Traditional
1. Uses OpenCC’s `s2hk` profile to convert to **Hong Kong Traditional Chinese**
2. Applies custom replacements from `hk2mo.json` for **Macau-specific Chinese characters**

### Traditional → Simplified
- Uses OpenCC’s standard `t2s` conversion (no JSON post-processing)

---

## 📌 Limitations

- ❌ Does **not** process headers, footers, footnotes, or text boxes  
- ❌ Only supports `.docx` (not legacy `.doc`)  
- ❌ Replacements are exact string matches (no regex or word-boundary logic)

> 💡 **Tip**: For complex documents, consider converting headers/footers manually or using Microsoft Word’s built-in converter for those sections.


---

## 📄 License

This project is licensed under the WTFPL License.

---
