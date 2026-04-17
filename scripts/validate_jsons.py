import os
import json
import sys
import jsonschema

blogs_dir = "blogs/"
schema_path = "scripts/.entry_schema.json"

with open(schema_path) as f:
    schema = json.load(f)

files = os.listdir(blogs_dir)

non_json = [f for f in files if not f.endswith(".json")]
if non_json:
    print("Error: the following files have the wrong extension (must end with .json):")
    for f in non_json:
        print(f"  {f}")
    sys.exit(1)

errors = []
for filename in files:
    path = os.path.join(blogs_dir, filename)
    with open(path) as f:
        data = json.load(f)
    validator = jsonschema.Draft4Validator(schema)
    file_errors = list(validator.iter_errors(data))
    for err in file_errors:
        errors.append(f"{filename}: {err.message} (path: {'/'.join(str(p) for p in err.absolute_path)})")

if errors:
    print("Validation failed:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

print(f"All {len(files)} JSON files are valid.")
