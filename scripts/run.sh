#!/bin/bash
export FLASK_APP=sync.server.app:create_app
export FLASK_ENV=development  # Optionnel, pour activer le mode debug

flask run
