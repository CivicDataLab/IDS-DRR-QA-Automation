"""
State Configuration Loader
Loads and provides access to state-specific indicator configurations
"""

import os
import yaml
from typing import Dict, List, Optional


class StateConfigLoader:
    """Loads and manages state-specific configurations"""

    def __init__(self, config_dir="config/states"):
        """
        Initialize configuration loader

        Args:
            config_dir: Directory containing state YAML files
        """
        self.config_dir = config_dir
        self.states_config = {}
        self.master_config = {}

        # Load configurations if directory exists
        if os.path.exists(config_dir):
            self.load_all_configs()

    def load_all_configs(self):
        """Load all state configurations from YAML files"""
        try:
            # Load master config first
            master_path = os.path.join(self.config_dir, "states_master.yaml")
            if os.path.exists(master_path):
                with open(master_path, 'r') as f:
                    self.master_config = yaml.safe_load(f)

            # Load individual state configs
            for state_key in self.master_config.get("states", {}).keys():
                state_file = f"{state_key}.yaml"
                state_path = os.path.join(self.config_dir, state_file)

                if os.path.exists(state_path):
                    with open(state_path, 'r') as f:
                        self.states_config[state_key] = yaml.safe_load(f)

            print(f"✅ Loaded configurations for {len(self.states_config)} states")

        except Exception as e:
            print(f"⚠️  Error loading state configurations: {e}")

    def get_state_config(self, state_key: str) -> Optional[Dict]:
        """
        Get configuration for a specific state

        Args:
            state_key: State key (e.g., 'assam', 'himachal_pradesh')

        Returns:
            dict: State configuration or None
        """
        return self.states_config.get(state_key)

    def get_all_states(self) -> List[str]:
        """
        Get list of all available states

        Returns:
            list: State keys
        """
        return list(self.states_config.keys())

    def get_state_indicators(self, state_key: str, section: str = None) -> List[Dict]:
        """
        Get indicators for a state

        Args:
            state_key: State key
            section: Optional section filter (hazard, exposure, etc.)

        Returns:
            list: Indicator configurations
        """
        state_config = self.get_state_config(state_key)

        if not state_config:
            return []

        indicators = []

        if section:
            # Get indicators for specific section
            section_data = state_config.get("sections", {}).get(section, {})
            indicators = section_data.get("indicators", [])
        else:
            # Get all indicators across all sections
            for section_data in state_config.get("sections", {}).values():
                indicators.extend(section_data.get("indicators", []))

        return indicators

    def get_indicator_by_key(self, state_key: str, indicator_key: str) -> Optional[Dict]:
        """
        Get specific indicator configuration

        Args:
            state_key: State key
            indicator_key: Indicator key

        Returns:
            dict: Indicator configuration or None
        """
        indicators = self.get_state_indicators(state_key)

        for indicator in indicators:
            if indicator.get("key") == indicator_key:
                return indicator

        return None

    def get_sections(self, state_key: str) -> Dict:
        """
        Get all sections for a state

        Args:
            state_key: State key

        Returns:
            dict: Sections configuration
        """
        state_config = self.get_state_config(state_key)

        if not state_config:
            return {}

        return state_config.get("sections", {})

    def get_test_parameters(self, states: List[str] = None, sections: List[str] = None):
        """
        Generate test parameters for pytest parametrize

        Args:
            states: List of states to include (None = all states)
            sections: List of sections to include (None = all sections)

        Returns:
            list: List of tuples (state_key, state_name, section, indicator)
        """
        test_params = []

        # Use all states if not specified
        if states is None:
            states = self.get_all_states()

        for state_key in states:
            state_config = self.get_state_config(state_key)

            if not state_config:
                continue

            state_name = state_config.get("state_name")
            sections_config = state_config.get("sections", {})

            for section_key, section_data in sections_config.items():
                # Filter by sections if specified
                if sections and section_key not in sections:
                    continue

                indicators = section_data.get("indicators", [])

                for indicator in indicators:
                    # Only include enabled indicators
                    if indicator.get("enabled", True):
                        test_params.append((
                            state_key,
                            state_name,
                            section_key,
                            indicator.get("key"),
                            indicator.get("name")
                        ))

        return test_params

    def get_state_summary(self, state_key: str) -> Dict:
        """
        Get summary information for a state

        Args:
            state_key: State key

        Returns:
            dict: Summary information
        """
        state_config = self.get_state_config(state_key)

        if not state_config:
            return {}

        sections = state_config.get("sections", {})

        summary = {
            "state_name": state_config.get("state_name"),
            "state_key": state_key,
            "discovered_at": state_config.get("discovered_at"),
            "total_indicators": sum(
                len(section.get("indicators", []))
                for section in sections.values()
            ),
            "sections": {}
        }

        for section_key, section_data in sections.items():
            summary["sections"][section_key] = {
                "name": section_data.get("name"),
                "total_indicators": len(section_data.get("indicators", [])),
                "enabled_indicators": len([
                    ind for ind in section_data.get("indicators", [])
                    if ind.get("enabled", True)
                ])
            }

        return summary

    def get_all_summaries(self) -> Dict:
        """
        Get summaries for all states

        Returns:
            dict: All state summaries
        """
        summaries = {}

        for state_key in self.get_all_states():
            summaries[state_key] = self.get_state_summary(state_key)

        return summaries


# Singleton instance
_config_loader = None


def get_config_loader(config_dir="config/states") -> StateConfigLoader:
    """
    Get singleton instance of StateConfigLoader

    Args:
        config_dir: Configuration directory

    Returns:
        StateConfigLoader: Config loader instance
    """
    global _config_loader

    if _config_loader is None:
        _config_loader = StateConfigLoader(config_dir)

    return _config_loader


if __name__ == "__main__":
    # Example usage
    loader = StateConfigLoader()

    print("\nAvailable States:")
    for state_key in loader.get_all_states():
        summary = loader.get_state_summary(state_key)
        print(f"\n{summary['state_name']} ({state_key}):")
        print(f"  Total Indicators: {summary['total_indicators']}")
        for section_key, section_info in summary['sections'].items():
            print(f"  - {section_info['name']}: {section_info['total_indicators']} indicators")
