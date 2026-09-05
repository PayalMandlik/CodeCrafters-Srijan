import asyncio
import sys

# 1. Test Arbitrage Engine
from tests.test_arbitrage import (
    test_manual_mathematical_validation,
    test_future_price_higher_store_and_hold,
    test_future_price_low_sell_immediately,
    test_high_spoilage_flips_recommendation,
    test_high_storage_cost_flips_recommendation,
    test_high_transit_cost_flips_recommendation,
    test_invalid_spoilage_raises_error,
    test_negative_current_price_raises_error,
)

# 2. Test Price Forecaster
from tests.test_forecast import (
    test_valid_historical_prices_forecast,
    test_forecast_horizon_14_days,
    test_forecast_horizon_30_days,
    test_invalid_horizon_rejected,
    test_deterministic_output,
)

# 3. Test Buyer Matcher
from tests.test_buyer_matching import (
    test_buyer_matcher_sorting_and_weights,
    test_empty_buyer_list,
)

# 4. Test API Routes
from tests.test_api import (
    test_health_endpoint,
    test_root_index_endpoint,
    test_analyze_valid_payload,
    test_analyze_invalid_quantity_returns_error,
)

# 5. Test Database & Fallback Layer
from tests.test_database_layer import (
    test_supabase_client_safe_unconfigured,
    test_market_service_fallback_mode,
    test_market_service_supabase_mode,
    test_market_service_empty_table_controlled_fallback,
    test_storage_service_fallback_and_supabase_modes,
    test_buyer_service_fallback_and_supabase_modes,
)

def run_all():
    print("========================================")
    print("RUNNING AGRIPREDICT AI ENGINE TEST SUITE")
    print("========================================")

    sync_tests = [
        test_manual_mathematical_validation,
        test_future_price_higher_store_and_hold,
        test_future_price_low_sell_immediately,
        test_high_spoilage_flips_recommendation,
        test_high_storage_cost_flips_recommendation,
        test_high_transit_cost_flips_recommendation,
        test_invalid_spoilage_raises_error,
        test_negative_current_price_raises_error,
        test_valid_historical_prices_forecast,
        test_forecast_horizon_14_days,
        test_forecast_horizon_30_days,
        test_invalid_horizon_rejected,
        test_deterministic_output,
        test_buyer_matcher_sorting_and_weights,
        test_empty_buyer_list,
        test_supabase_client_safe_unconfigured,
        test_market_service_fallback_mode,
        test_market_service_supabase_mode,
        test_market_service_empty_table_controlled_fallback,
        test_storage_service_fallback_and_supabase_modes,
        test_buyer_service_fallback_and_supabase_modes,
    ]

    async_tests = [
        test_health_endpoint,
        test_root_index_endpoint,
        test_analyze_valid_payload,
        test_analyze_invalid_quantity_returns_error,
    ]

    passed_count = 0
    total_count = len(sync_tests) + len(async_tests)

    for test_fn in sync_tests:
        try:
            test_fn()
            passed_count += 1
            print(f"[PASS] {test_fn.__name__}")
        except Exception as e:
            print(f"[FAIL] {test_fn.__name__}: {e}")

    for async_fn in async_tests:
        try:
            asyncio.run(async_fn())
            passed_count += 1
            print(f"[PASS] {async_fn.__name__}")
        except Exception as e:
            print(f"[FAIL] {async_fn.__name__}: {e}")

    print("========================================")
    print(f"RESULTS: {passed_count}/{total_count} TESTS PASSED SUCCESSFULLY ({(passed_count/total_count)*100:.1f}%)")
    print("========================================")

    if passed_count != total_count:
        sys.exit(1)

if __name__ == "__main__":
    run_all()
