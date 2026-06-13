# 🎓 C Language Auto-Grader

[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#-license)

A lightweight Python tool that automatically **compiles, runs, and grades C program submissions** against predefined test cases. Built to solve a real problem: manually checking dozens of beginner C assignments (sum, GCD, prime check, etc.) is slow and error-prone — this tool does it in seconds.

---

## 📑 Table of Contents

- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Usage](#-usage)
- [Test Case Format](#-test-case-format)
- [Numeric Comparison (Floats)](#-numeric-comparison-floats)
- [Multiple Problems Support](#-multiple-problems-support)
- [Example Run](#-example-run)
- [Limitations](#️-limitations)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## ⚙️ How It Works

For each `.c` file found in `submissions/`, the grader:

1. **Compiles** the file using `gcc -lm`
2. If compilation fails → reports `COMPILE_ERROR` (0 points)
3. If it succeeds, **runs the program** once per test case, feeding the `.in` file content into stdin (simulating keyboard input)
4. **Compares** the program's stdout output against the expected `.out` file
5. Prints a **PASS/FAIL** result per test case, plus a final score out of 10

---

## 📁 Project Structure

```
auto-grader/
├── grader.py                  # Main grading script
├── generate_testcases.py      # (optional) script to bulk-generate test cases
├── README.md
├── submissions/                # .c files to be graded
│   ├── student1.c
│   └── student2.c
└── testcases/
    ├── bai1_tong2so/            # Test cases for "sum of two numbers"
    │   ├── test1.in
    │   ├── test1.out
    │   ├── test2.in
    │   └── test2.out
    └── bai2_hieu2so/             # Test cases for "difference of two numbers"
        ├── test1.in
        ├── test1.out
        ├── test2.in
        └── test2.out
```

> 💡 Each problem has its own subfolder under `testcases/`, so test cases for different assignments don't overwrite each other and can be reused across semesters.

---

## 🛠️ Requirements

| Component | Requirement |
|---|---|
| Python | 3.8+ |
| Compiler | GCC (MinGW on Windows, or build-essential on Linux) |
| Python packages | None required for `grader.py` itself (standard library only) |

Check GCC is available:

```bash
gcc --version
```

---

## 🚀 Usage

Place student submissions in `submissions/`, then run:

```bash
python grader.py --testcases bai1_tong2so
```

To grade against a different problem's test cases:

```bash
python grader.py --testcases bai2_hieu2so
```

If `--testcases` is omitted, it defaults to `bai1_tong2so`.

---

## 📝 Test Case Format

Each test case is a pair of plain-text files inside a problem folder:

- **`testN.in`** — input fed to the program via stdin (what a user would type)
- **`testN.out`** — the expected output

### Example — "Sum of two numbers" (`bai1_tong2so/`)

`test1.in`:
```
5 3
```

`test1.out`:
```
8
```

### Example — "Difference of two numbers" (`bai2_hieu2so/`)

| Test | Input (a b) | Expected Output (a − b) | Purpose |
|---|---|---|---|
| test1 | `5 3` | `2` | basic case |
| test2 | `3 5` | `-2` | negative result |
| test3 | `0 0` | `0` | zero edge case |
| test4 | `-10 -20` | `10` | negative operands |
| test5 | `100 100` | `0` | equal operands |
| test6 | `-15 5` | `-20` | mixed sign |

Good test cases aren't random — they're chosen to cover **edge cases** (zero, negative numbers, equal values) that commonly expose bugs like sign errors or operand-order mistakes.

---

## 🔢 Numeric Comparison (Floats)

For problems involving real numbers (e.g. area of a circle), exact string comparison would unfairly fail correct answers that differ only in decimal precision (e.g. `12.566371` vs `12.5664`).

The grader tokenizes both outputs and, for tokens that are valid numbers, compares them with a tolerance:

```python
epsilon = 1e-4
abs(actual_value - expected_value) < epsilon
```

Non-numeric tokens (text, symbols) are still compared exactly. This makes the grader tolerant of formatting/precision differences while still catching genuinely wrong answers.

---

## 🧩 Multiple Problems Support

The grader accepts a `--testcases <folder_name>` argument, pointing to a subfolder under `testcases/`. This means:

- Test cases for each assignment are written **once** and reused every time that assignment is graded
- Switching to a new assignment doesn't require deleting or overwriting previous test cases — just create a new subfolder
- The same `submissions/` folder (containing multiple students' `.c` files) can be graded against different problems by changing one argument

```bash
python grader.py --testcases bai1_tong2so
python grader.py --testcases bai2_hieu2so
python grader.py --testcases bai3_gcd_lcm
```

---

## 📋 Example Run

```
=== Đang chấm: student1.c ===
  ✅ test1.in: PASS
  ✅ test2.in: PASS
  Điểm: 2/2 test pass -> 10.0/10

=== Đang chấm: student2.c ===
  ❌ test1.in: FAIL
  ❌ test2.in: FAIL
  Điểm: 0/2 test pass -> 0.0/10
```

---

## ⚠️ Limitations

This grader is designed for **simple stdin/stdout programs with a single correct answer**. It does **not** currently support:

- Problems with **multiple valid answers** (e.g. "print any prime number greater than 100")
- Programs that **read/write files** instead of using stdin/stdout (e.g. a student management system that persists to a `.txt` file)
- Problems where **output order doesn't matter**
- Programs requiring **special compiler flags** (`-lpthread`, graphics libraries, etc.)
- Interactive **menu-driven programs** with complex branching loops

For these cases, a custom checker per problem would be required — this is the same reason real judging systems (Codeforces, etc.) use per-problem "special judges" rather than one universal checker.

---

## 🔮 Roadmap

- [ ] Export results to CSV for whole-class grading
- [ ] Add per-test timeout to catch infinite loops
- [ ] Clean up generated `.exe` files automatically after grading
- [ ] Support custom checkers for problems with multiple valid answers
- [ ] Optional sandboxing (Docker) for running untrusted student code safely

---

## 📄 License

This project is released under the **MIT License** — free to use, modify, and distribute for educational purposes.
