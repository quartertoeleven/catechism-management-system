import json
from main import create_app

def generate_spec():
    # This extracts the exact schema FastAPI generates automatically
    openapi_schema = create_app().openapi() 
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)

if __name__ == "__main__":
    generate_spec()
