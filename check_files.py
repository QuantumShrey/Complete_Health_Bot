import os

def check_files():
    expected_structure = {
        'data': ['Training.csv', 'Testing.csv', 'doctors_dataset.csv'],
        'static': ['styles.css', 'script.js'],
        'templates': ['index.html', 'services.html'],
        '.': ['app.py']
    }
    
    all_good = True
    
    for directory, files in expected_structure.items():
        print(f"\nChecking {directory}...")
        for file in files:
            path = os.path.join(directory, file)
            if os.path.exists(path):
                print(f"✅ Found {file}")
            else:
                print(f"❌ Missing {file}")
                all_good = False
    
    if all_good:
        print("\n✅ All files are in the correct place!")
    else:
        print("\n❌ Some files are missing or in wrong locations.")

if __name__ == "__main__":
    check_files()
