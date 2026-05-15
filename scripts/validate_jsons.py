import os
import json
import sys
import jsonschema


def validate_directory(data_dir, schema_path):
    with open(schema_path) as f:
        schema = json.load(f)

    files = os.listdir(data_dir)

    non_json = [f for f in files if not f.endswith(".json")]
    if non_json:
        print(f"Error: non-JSON files found in {data_dir}:")
        for f in non_json:
            print(f"  {f}")
        return False

    errors = []
    for filename in files:
        path = os.path.join(data_dir, filename)
        with open(path) as f:
            data = json.load(f)
        validator = jsonschema.Draft4Validator(schema)
        for err in validator.iter_errors(data):
            loc = "/".join(str(p) for p in err.absolute_path)
            errors.append(f"{filename}: {err.message}" + (f" (path: {loc})" if loc else ""))

    if errors:
        print(f"Validation failed in {data_dir}:")
        for e in errors:
            print(f"  {e}")
        return False

    print(f"All {len(files)} files in {data_dir} are valid.")
    return True


ok = True
ok &= validate_directory("data/content/",  "scripts/.entry_schema.json")
ok &= validate_directory("data/packages/", "scripts/.package_schema.json")

if not ok:
    sys.exit(1)
