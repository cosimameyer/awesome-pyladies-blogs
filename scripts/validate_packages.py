import os
import json
import sys
import jsonschema

packages_dir = "data/packages/"
schema_path = "scripts/.package_schema.json"

with open(schema_path) as f:
    schema = json.load(f)

files = os.listdir(packages_dir)

non_json = [f for f in files if not f.endswith(".json")]
if non_json:
    print("Error: the following files have the wrong extension (must end with .json):")
    for f in non_json:
        print(f"  {f}")
    sys.exit(1)

errors = []
for filename in files:
    path = os.path.join(packages_dir, filename)
    with open(path) as f:
        data = json.load(f)
    validator = jsonschema.Draft4Validator(schema)
    for err in validator.iter_errors(data):
        loc = "/".join(str(p) for p in err.absolute_path)
        errors.append(f"{filename}: {err.message}" + (f" (path: {loc})" if loc else ""))

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print(f"All {len(files)} package JSON files are valid.")
