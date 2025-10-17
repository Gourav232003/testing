#!/usr/bin/env python3
"""
EcoFarm Quest Backend Server
Main entry point for running the Flask application
"""

import os
from app import app

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("🌱 Starting EcoFarm Quest Backend API...")
    print(f"📡 Server: http://{host}:{port}")
    print(f"🔧 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🐛 Debug Mode: {debug}")
    print("=" * 50)
    
    # Determine whether to use the Werkzeug reloader.
    # On Windows the reloader + threaded server can sometimes cause
    # "An operation was attempted on something that is not a socket" (WinError 10038).
    use_reloader = debug
    if os.name == 'nt' and debug:
        # Disable the automatic reloader on Windows when debugging to avoid socket issues.
        use_reloader = False

    # Run the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True,
        use_reloader=use_reloader
    )
