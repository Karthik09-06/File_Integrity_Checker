import hashlib
from tqdm import tqdm
import os
import sys

# Function to calculate sha256 with progress bar
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    file_size = os.path.getsize(file_path)

    with open(file_path, "rb") as f, tqdm(
        total=file_size,
        unit="B",
        unit_scale=True,
        desc=os.path.basename(file_path),
        ascii=True,
    ) as pbar:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
            pbar.update(len(chunk))

    return sha256.hexdigest()

# Function to check multiple files against expected hashes
def verify_files(checksum_file):
    success_count = 0
    fail_count = 0

    with open(checksum_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip empty or commented lines

        try:
            expected_hash, file_path = line.split(maxsplit=1)
            file_path = file_path.strip()
        except ValueError:
            print(f"❌ Invalid line format: {line}")
            continue

        if not os.path.isfile(file_path):
            print(f"❌ File not found: {file_path}")
            fail_count += 1
            continue

        print(f"\nChecking: {file_path}")
        calculated_hash = calculate_sha256(file_path)

        if calculated_hash.lower() == expected_hash.lower():
            print(f"✅ {file_path} integrity verified.")
            success_count += 1
        else:
            print(f"❌ {file_path} integrity check failed.")
            print(f"   Expected:   {expected_hash}")
            print(f"   Calculated: {calculated_hash}")
            fail_count += 1

    print("\nSummary:")
    print(f"  ✅ Passed: {success_count}")
    print(f"  ❌ Failed: {fail_count}")
    print(f"  Total: {success_count + fail_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_integrity.py <checksum_file>")
        sys.exit(1)

    checksum_file = sys.argv[1]
    if not os.path.isfile(checksum_file):
        print(f"Checksum file not found: {checksum_file}")
        sys.exit(1)

    verify_files(checksum_file)
