with open("mit_zip_code_list.txt") as f:
    ZIP_CODES = f.read().splitlines()
ZIP_CODES_PMF = {b: 1.0/len(ZIP_CODES) for b in sorted(ZIP_CODES)}