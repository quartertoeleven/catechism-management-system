import json
from pathlib import Path
from main import create_app

def generate_spec():
    # This extracts the exact schema FastAPI generates automatically
    openapi_schema = create_app().openapi() 
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

def beautify_function_name():    
    file_path = Path("./openapi.json")
    openapi_content = json.loads(file_path.read_text())

    for path_data in openapi_content["paths"].values():
        for operation in path_data.values():
            tag = operation["tags"][0]
            operation_id = operation["operationId"]
            to_remove = f"{tag}-"
            new_operation_id = operation_id[len(to_remove) :]
            operation["operationId"] = new_operation_id

    file_path.write_text(json.dumps(openapi_content))

if __name__ == "__main__":
    generate_spec()
    beautify_function_name()
