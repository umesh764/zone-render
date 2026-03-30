from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug=False for production (security)
    # Host='0.0.0.0' allows external access
    app.run(host='0.0.0.0', port=5000, debug=False)