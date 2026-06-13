import subprocess
import os
import argparse
from pathlib import Path


def compile_c_file(c_file_path, output_exe):
    """Compile file .c, trả về (success, error_message)"""
    result = subprocess.run(
        ["gcc", str(c_file_path), "-o", str(output_exe), "-lm"],
        capture_output=True, text=True, timeout=10
    )
    return result.returncode == 0, result.stderr

def run_test(exe_path, input_data, timeout=5):
    """Chạy file exe với input, trả về output (hoặc None nếu lỗi/timeout)"""
    try:
        result = subprocess.run(
            [str(exe_path)],
            input=input_data,
            capture_output=True, text=True, timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return None

def normalize(text):
    """Chuẩn hóa output: bỏ khoảng trắng dư, xuống dòng cuối"""
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

def is_number(s):
    """Kiểm tra string có phải số (int hoặc float) không"""
    try:
        float(s)
        return True
    except ValueError:
        return False

def compare_outputs(actual, expected, epsilon=1e-4):
    """So sánh 2 output, cho phép sai số nhỏ với số thực.
       Trả về True nếu khớp."""
    actual_tokens = normalize(actual).split()
    expected_tokens = normalize(expected).split()

    if len(actual_tokens) != len(expected_tokens):
        return False

    for a_tok, e_tok in zip(actual_tokens, expected_tokens):
        if is_number(a_tok) and is_number(e_tok):
            # So sánh số với sai số cho phép
            if abs(float(a_tok) - float(e_tok)) > epsilon:
                return False
        else:
            # So sánh string thông thường
            if a_tok != e_tok:
                return False

    return True

def grade_submission(c_file, testcases_dir):
    exe_path = c_file.with_suffix(".exe")

    # Bước 1: Compile
    success, error = compile_c_file(c_file, exe_path)
    if not success:
        return {"status": "COMPILE_ERROR", "error": error, "passed": 0, "total": 0}

    # Bước 2: Lấy danh sách test case
    test_inputs = sorted(Path(testcases_dir).glob("*.in"))
    passed = 0
    total = len(test_inputs)
    details = []

    for test_in in test_inputs:
        test_out = test_in.with_suffix(".out")
        if not test_out.exists():
            continue

        input_data = test_in.read_text(encoding="utf-8")
        expected = test_out.read_text(encoding="utf-8")

        actual = run_test(exe_path, input_data)

        if actual is None:
            details.append((test_in.name, "TIMEOUT"))
        elif compare_outputs(actual, expected):
            passed += 1
            details.append((test_in.name, "PASS"))
        else:
            details.append((test_in.name, "FAIL"))

    return {
        "status": "OK",
        "passed": passed,
        "total": total,
        "details": details
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--testcases", default="bai1_tong2so",
                         help="Tên folder con trong testcases/ chứa test case")
    args = parser.parse_args()

    submissions_dir = Path("submissions")
    testcases_dir = Path("testcases") / args.testcases

    for c_file in submissions_dir.glob("*.c"):
        print(f"\n=== Đang chấm: {c_file.name} ===")
        result = grade_submission(c_file, testcases_dir)

        if result["status"] == "COMPILE_ERROR":
            print("❌ LỖI COMPILE:")
            print(result["error"])
            continue

        for test_name, status in result["details"]:
            icon = "✅" if status == "PASS" else "❌"
            print(f"  {icon} {test_name}: {status}")

        score = (result["passed"] / result["total"]) * 10 if result["total"] > 0 else 0
        print(f"  Điểm: {result['passed']}/{result['total']} test pass -> {score:.1f}/10")

if __name__ == "__main__":
    main()