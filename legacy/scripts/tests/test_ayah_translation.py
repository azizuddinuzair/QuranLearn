import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))
from loader import load_ayah_translations

# Test cases: (surah, ayah, expected_substring)
test_cases = [
    (1, 6, "Show us the straight way"),
    (2, 259, "how shall Allah bring it (ever) to life"),
    (6, 129, "Thus do we make the wrong-doers turn to each other"),
    (10, 77, "Said Moses"),
    (12, 103, "Yet no faith will the greater part of mankind have"),
    (26, 129, "fine buildings"),
]

def run_tests():
    ayah_path = Path(__file__).parents[2] / 'data' / 'ayahs' / 'English_clean.csv'
    ayahs = load_ayah_translations(ayah_path)
    passed = 0
    for surah, ayah, expected in test_cases:
        result = ayahs.get((surah, ayah))
        print(f"Testing ({surah}, {ayah})...", end=' ')
        if result is None:
            print("FAIL: No translation found")
        elif expected in result:
            print("PASS")
            passed += 1
        else:
            print(f"FAIL: Translation mismatch\n  Got: {result}\n  Expected to contain: {expected}")
    print(f"\n{passed}/{len(test_cases)} tests passed.")

if __name__ == "__main__":
    run_tests()
