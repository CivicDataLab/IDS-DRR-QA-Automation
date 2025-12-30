#!/usr/bin/env python3
"""
Quick verification script to check if multi-state framework is set up correctly
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")

    dependencies = {
        'yaml': 'pyyaml',
        'selenium': 'selenium',
        'pytest': 'pytest',
        'dotenv': 'python-dotenv'
    }

    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False

    print("\n✅ All dependencies installed!")
    return True


def check_framework_files():
    """Check if framework files exist"""
    print("\n🔍 Checking framework files...")

    required_files = [
        'utils/state_indicator_discovery.py',
        'utils/state_config_loader.py',
        'utils/pytest_multistate_plugin.py',
        'tests/test_analytics_multistate.py',
        'scripts/discover_state_indicators.py',
        'docs/MULTISTATE_QUICKSTART.md',
        'MULTISTATE_FRAMEWORK.md'
    ]

    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING")
            missing.append(file_path)

    if missing:
        print(f"\n⚠️  Missing files!")
        return False

    print("\n✅ All framework files present!")
    return True


def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")

    from dotenv import load_dotenv
    load_dotenv()

    url = os.getenv('URL')
    dev_url = os.getenv('DEV_URL')
    username = os.getenv('HOME_URL_USERNAME')
    password = os.getenv('HOME_URL_PASSWORD')

    if dev_url:
        print(f"  ✅ DEV_URL configured: {dev_url}")
        print(f"     (Will test against development environment)")
    elif url:
        print(f"  ✅ URL configured: {url}")
        print(f"     (Will test against production environment)")
    else:
        print(f"  ❌ Neither URL nor DEV_URL configured!")
        print(f"     Set one in your .env file")
        return False

    if username and password:
        print(f"  ✅ Credentials configured")
    else:
        print(f"  ⚠️  Credentials not configured (may be required for testing)")

    return True


def check_state_configs():
    """Check if state configurations exist"""
    print("\n🔍 Checking state configurations...")

    config_dir = "config/states"

    if not os.path.exists(config_dir):
        print(f"  ⚠️  State configurations not found in {config_dir}")
        print(f"     Run: python scripts/discover_state_indicators.py")
        return False

    master_file = os.path.join(config_dir, "states_master.yaml")
    if os.path.exists(master_file):
        import yaml
        with open(master_file, 'r') as f:
            master_config = yaml.safe_load(f)

        total_states = master_config.get('total_states', 0)
        print(f"  ✅ Found {total_states} state configuration(s)")

        for state_key, state_info in master_config.get('states', {}).items():
            state_name = state_info.get('name')
            total_indicators = state_info.get('total_indicators', 0)
            print(f"     • {state_name}: {total_indicators} indicators")

        return True
    else:
        print(f"  ⚠️  Master configuration not found")
        print(f"     Run: python scripts/discover_state_indicators.py")
        return False


def main():
    """Run all verification checks"""
    print("="*70)
    print("  MULTI-STATE TESTING FRAMEWORK - SETUP VERIFICATION")
    print("="*70 + "\n")

    checks = [
        ("Dependencies", check_dependencies),
        ("Framework Files", check_framework_files),
        ("Environment", check_environment),
        ("State Configs", check_state_configs)
    ]

    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error checking {name}: {e}")
            results[name] = False

    print("\n" + "="*70)
    print("  VERIFICATION SUMMARY")
    print("="*70 + "\n")

    all_passed = all(results.values())

    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {name}")

    print("\n" + "="*70)

    if all_passed:
        print("\n🎉 Setup verification complete! Framework is ready to use.")
        print("\nNext steps:")
        print("  1. If state configs not found, run: python scripts/discover_state_indicators.py")
        print("  2. Run tests: pytest tests/test_analytics_multistate.py -v")
        print("  3. View documentation: docs/MULTISTATE_QUICKSTART.md")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the output above.")
        print("\nQuick fixes:")
        print("  • Missing dependencies: pip install -r requirements.txt")
        print("  • Missing configs: python scripts/discover_state_indicators.py")
        print("  • Environment setup: Copy .env.example to .env and configure")
        return 1


if __name__ == "__main__":
    sys.exit(main())
