#!/usr/bin/env python3
"""
State Indicator Discovery Script

This script automatically discovers all available indicators for each state
and generates YAML configuration files.

Usage:
    # Discover all states
    python scripts/discover_state_indicators.py

    # Discover specific states
    python scripts/discover_state_indicators.py --states Assam "Himachal pradesh"

    # Discover and force overwrite existing configs
    python scripts/discover_state_indicators.py --force

    # Custom output directory
    python scripts/discover_state_indicators.py --output config/states_custom
"""

import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.state_indicator_discovery import StateIndicatorDiscovery, run_discovery
from utils.state_config_loader import StateConfigLoader


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Discover analytics indicators for multiple states"
    )

    parser.add_argument(
        "--states",
        nargs="+",
        help="Specific states to discover (default: all available states)"
    )

    parser.add_argument(
        "--output",
        default="config/states",
        help="Output directory for YAML configs (default: config/states)"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing configuration files"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate existing configurations instead of discovering"
    )

    return parser.parse_args()


def validate_configs(config_dir):
    """
    Validate existing state configurations

    Args:
        config_dir: Directory containing state configs
    """
    print("\n" + "="*70)
    print("VALIDATING STATE CONFIGURATIONS")
    print("="*70 + "\n")

    if not os.path.exists(config_dir):
        print(f"❌ Configuration directory not found: {config_dir}")
        print("Run discovery first without --validate flag")
        return False

    loader = StateConfigLoader(config_dir)

    if not loader.get_all_states():
        print(f"❌ No state configurations found in {config_dir}")
        return False

    print(f"✅ Found {len(loader.get_all_states())} state configurations\n")

    all_valid = True

    for state_key in loader.get_all_states():
        summary = loader.get_state_summary(state_key)

        print(f"\n{summary['state_name']} ({state_key}):")
        print(f"  Configuration File: {state_key}.yaml")
        print(f"  Total Indicators: {summary['total_indicators']}")

        if summary['total_indicators'] == 0:
            print(f"  ⚠️  WARNING: No indicators configured!")
            all_valid = False
            continue

        print(f"  Sections:")
        for section_key, section_info in summary['sections'].items():
            enabled = section_info.get('enabled_indicators', section_info['total_indicators'])
            print(f"    • {section_info['name']}: {enabled}/{section_info['total_indicators']} enabled")

        # Validate required sections
        required_sections = ["hazard", "exposure", "vulnerability", "government_response"]
        missing_sections = [s for s in required_sections if s not in summary['sections']]

        if missing_sections:
            print(f"  ⚠️  WARNING: Missing sections: {', '.join(missing_sections)}")
            all_valid = False
        else:
            print(f"  ✅ All required sections present")

    print("\n" + "="*70)

    if all_valid:
        print("✅ ALL CONFIGURATIONS VALID")
    else:
        print("⚠️  SOME CONFIGURATIONS HAVE ISSUES")

    print("="*70 + "\n")

    return all_valid


def main():
    """Main execution"""
    args = parse_args()

    # Validate mode
    if args.validate:
        valid = validate_configs(args.output)
        sys.exit(0 if valid else 1)

    # Check if configs exist and force flag not set
    if os.path.exists(args.output) and not args.force:
        response = input(
            f"\n⚠️  Configuration directory '{args.output}' already exists.\n"
            f"Do you want to overwrite? (yes/no): "
        )

        if response.lower() not in ['yes', 'y']:
            print("❌ Discovery cancelled. Use --force to overwrite automatically.")
            sys.exit(0)

    # Run discovery
    print("\n" + "="*70)
    print("STARTING STATE INDICATOR DISCOVERY")
    print("="*70 + "\n")

    discovery = StateIndicatorDiscovery()

    try:
        # Discover states
        results = discovery.discover_all_states(args.states)

        # Save configurations
        discovery.save_to_yaml(args.output)

        # Print summary
        print("\n" + "="*70)
        print("DISCOVERY COMPLETE!")
        print("="*70)

        total_states = results.get("total_states", 0)
        print(f"\n✅ Successfully discovered {total_states} states")

        print("\nConfiguration files created:")
        for state_key in results.get("states", {}).keys():
            print(f"  • {args.output}/{state_key}.yaml")

        print(f"  • {args.output}/states_master.yaml (master index)")

        print("\nNext steps:")
        print(f"  1. Review generated configs in: {args.output}/")
        print(f"  2. Validate configs: python scripts/discover_state_indicators.py --validate")
        print(f"  3. Run tests: pytest tests/test_analytics.py -v")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Discovery failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        discovery.cleanup()


if __name__ == "__main__":
    main()
