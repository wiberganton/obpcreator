import obpcreator.scanning_strategies.infill_strategies as infill_strategies

def generate_infill(point_infill, scan_settings):
    strategy_func = getattr(infill_strategies, scan_settings.scan_strategy, None)
    if strategy_func:
        return strategy_func(point_infill, scan_settings)
    else:
        print(f"No function named {scan_settings.scan_strategy} exists")

