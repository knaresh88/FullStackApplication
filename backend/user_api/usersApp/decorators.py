import os
from unittest import skip

def skip_if_feature_flag_disabled(feature_flag):
    """
    Decorator to skip a test if a feature flag is disabled.
    """
    def decorator(test_func):
        def wrapper(self, *args, **kwargs):
            if os.environ.get(feature_flag, '0') == '0':
                self.skipTest(f"Skipping test because {feature_flag} is disabled")
            else:
                return test_func(self, *args, **kwargs)
        return wrapper
    return decorator

def skip_if_feature_flag_enabled(feature_flag):
    """
    Decorator to skip a test if a feature flag is enabled.
    """
    def decorator(test_func):
        def wrapper(self, *args, **kwargs):
            if os.environ.get(feature_flag, '0') == '1':
                self.skipTest(f"Skipping test because {feature_flag} is enabled")
            else:
                return test_func(self, *args, **kwargs)
        return wrapper
    return decorator
