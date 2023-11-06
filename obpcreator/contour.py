import obpcreator.scanning_strategies.contour_strategies as contour_strategies

def generate_contour(paths, scan_settings):
    strategy_func = getattr(contour_strategies, scan_settings.scan_strategy, None)
    if strategy_func:
        return strategy_func(paths, scan_settings)
    else:
        print(f"No function named {scan_settings.scan_strategy} exists")
