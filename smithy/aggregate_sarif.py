import json
import os
import sys

def convert_apigeelint_to_sarif(apigeelint_json_path):
    with open(apigeelint_json_path, 'r') as f:
        data = json.load(f)
    
    runs = [{
        "tool": {
            "driver": {
                "name": "apigeelint",
                "rules": []  # Can populate if needed
            }
        },
        "results": []
    }]
    
    for result in data.get('results', []):
        level = 'error' if result['severity'] == 'error' else 'warning'
        sarif_result = {
            "level": level,
            "message": {
                "text": result['message']
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": result['file']
                    },
                    "region": {
                        "startLine": result['line'],
                        "startColumn": result.get('column', 1)
                    }
                }
            }],
            "ruleId": result['ruleId']
        }
        runs[0]['results'].append(sarif_result)
    
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": runs
    }

def merge_sarif(files):
    base = {"$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0", "runs": []}
    for file in files:
        if not os.path.exists(file):
            continue
        if file.endswith('.json'):  # Assume apigeelint JSON
            sarif_data = convert_apigeelint_to_sarif(file)
        else:  # Assume native SARIF (e.g., from Cx)
            with open(file, 'r') as f:
                sarif_data = json.load(f)
        base['runs'].extend(sarif_data.get('runs', []))
    return base

if __name__ == "__main__":
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]
    merged = merge_sarif(input_files)
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=2)