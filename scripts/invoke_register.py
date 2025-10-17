import json
import importlib.util
import os
import sys

# Ensure project root is on sys.path so package imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load app.py as a module without executing it as __main__ (prevents starting the server)
app_path = os.path.join(project_root, 'app.py')
spec = importlib.util.spec_from_file_location('local_app', app_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# The Flask app object is exported as 'app' in app.py
client = module.app.test_client()

payload = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "Password1",
    "phone": "+1234567890",
    "location": "Test Farm",
    "farm_size": "small"
}

resp = client.post('/api/auth/register', json=payload)
print('STATUS:', resp.status_code)
print(resp.get_data(as_text=True))
