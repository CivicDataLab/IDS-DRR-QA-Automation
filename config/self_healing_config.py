"""
Self-Healing Configuration Settings

This file contains settings for self-healing behavior
"""


class SelfHealingConfig:
    """Configuration for self-healing features"""

    # Enable/disable self-healing globally
    ENABLED = True

    # Maximum number of healing strategies to try before giving up
    # OPTIMIZED: Reduced from 5 to 3 for better performance
    MAX_HEALING_ATTEMPTS = 3

    # Timeout for each healing attempt (seconds)
    # OPTIMIZED: Reduced from 5 to 3 seconds for faster failure detection
    HEALING_TIMEOUT = 3

    # Enable learning mode (saves successful locators for future use)
    LEARNING_MODE = True

    # Path to store learned locators
    LEARNED_LOCATORS_PATH = "config/learned_locators.json"

    # Enable detailed logging of healing attempts
    # OPTIMIZED: Set to False for better performance (less I/O)
    VERBOSE_LOGGING = False

    # Retry configuration
    # OPTIMIZED: Reduced from 3 to 2 retries for faster execution
    MAX_RETRIES = 2
    RETRY_DELAY = 0.5  # seconds (reduced from 1)

    # Healing strategies to use (in order of preference)
    STRATEGIES = [
        "original",           # Try original locator first
        "learned",            # Try previously learned locators
        "relaxed_xpath",      # Try relaxed XPath variations
        "css_alternatives",   # Try CSS selector variations
        "tag_based",          # Try tag-based locators
        "text_based",         # Try text-based locators
    ]

    # Element-specific healing settings
    ELEMENT_SPECIFIC_SETTINGS = {
        "button": {
            "enabled": True,
            "timeout": 10,
            "strategies": ["original", "learned", "tag_based", "text_based"]
        },
        "input": {
            "enabled": True,
            "timeout": 8,
            "strategies": ["original", "learned", "tag_based"]
        },
        "dropdown": {
            "enabled": True,
            "timeout": 10,
            "strategies": ["original", "learned", "relaxed_xpath"]
        }
    }

    # Generate healing reports
    GENERATE_REPORTS = True
    REPORT_DIR = "reports/self_healing"

    # Auto-update locators in code (experimental - disabled by default)
    AUTO_UPDATE_LOCATORS = False

    # Threshold for suggesting locator updates
    # If a locator fails X times and healing succeeds, suggest update
    UPDATE_SUGGESTION_THRESHOLD = 3

    @classmethod
    def get_element_setting(cls, element_type, setting_name, default=None):
        """
        Get element-specific setting

        Args:
            element_type: Type of element (button, input, etc.)
            setting_name: Name of the setting
            default: Default value if not found

        Returns:
            Setting value or default
        """
        element_settings = cls.ELEMENT_SPECIFIC_SETTINGS.get(element_type, {})
        return element_settings.get(setting_name, default)

    @classmethod
    def is_strategy_enabled(cls, strategy_name):
        """Check if a healing strategy is enabled"""
        return strategy_name in cls.STRATEGIES

    @classmethod
    def get_timeout_for_element(cls, element_type):
        """Get timeout for specific element type"""
        return cls.get_element_setting(element_type, "timeout", cls.HEALING_TIMEOUT)
