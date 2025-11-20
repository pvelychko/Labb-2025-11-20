# Test Coverage Report - Gilded Rose

**Generated**: 2025-11-20
**Test Framework**: pytest + unittest
**Coverage Tool**: coverage.py

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | 41 |
| **Tests Passing** | 41 (100%) |
| **Code Coverage** | 97% |
| **Lines Covered** | 35/36 |
| **Missing Lines** | 1 (line 46: `__repr__` method) |

---

## Test Suite Organization

### 1. NormalItemsTest (5 tests)
Tests for standard items that degrade over time:
- ✅ Degradation before sell date (-1 quality/day)
- ✅ Degradation on sell date (sell_in=0)
- ✅ Accelerated degradation after sell date (-2 quality/day)
- ✅ Quality never goes negative
- ✅ Quality boundary at 0 with accelerated degradation

### 2. AgedBrieTest (6 tests)
Tests for Aged Brie (increases in quality):
- ✅ Quality increases before sell date (+1/day)
- ✅ Quality increases at sell date
- ✅ Quality increases twice as fast after sell date (+2/day)
- ✅ Quality caps at 50
- ✅ Quality caps at 50 with accelerated increase
- ✅ Quality starts from 0 and increases

### 3. BackstagePassesTest (10 tests)
Tests for Backstage passes (complex progression):
- ✅ Increase by 1 when >10 days away
- ✅ Increase by 2 at exactly 10 days
- ✅ Increase by 2 when 6-10 days away
- ✅ Increase by 3 at exactly 5 days
- ✅ Increase by 3 when 1-5 days away
- ✅ Behavior at sell date (sell_in=0)
- ✅ Quality drops to 0 after concert
- ✅ Quality caps at 50
- ✅ Quality near max with different thresholds
- ✅ Multi-day progression across thresholds

### 4. SulfurasTest (5 tests)
Tests for Sulfuras (legendary item):
- ✅ Quality never changes (stays at 80)
- ✅ Sell-in never decreases
- ✅ Behavior at sell_in=0
- ✅ Behavior after sell date (negative sell_in)
- ✅ Consistency over multiple days

### 5. QualityBoundsTest (6 tests)
Tests for quality boundaries (0-50):
- ✅ Quality never negative for normal items
- ✅ Quality never exceeds 50 for Aged Brie
- ✅ Quality never exceeds 50 for Backstage passes
- ✅ Quality at 49 can reach 50
- ✅ Quality at 48 with +2 increase caps at 50
- ✅ Quality at 48 with +3 increase caps at 50

### 6. SellInEdgeCasesTest (6 tests)
Tests for sell-in date transitions:
- ✅ Sell-in decreases for normal items
- ✅ Sell-in decreases for Aged Brie
- ✅ Sell-in decreases for Backstage passes
- ✅ Sell-in can go negative
- ✅ Normal item transition at sell date boundary
- ✅ Aged Brie transition at sell date boundary

### 7. MultipleItemsTest (2 tests)
Tests for multiple items updating together:
- ✅ Multiple items update independently
- ✅ All item types work correctly together

### 8. ConjuredItemsTest (1 test)
Documents current behavior (not yet implemented):
- ✅ Conjured items currently behave like normal items
- ⚠️ NOTE: Should degrade 2x as fast (-2/day) but currently degrades by -1/day

---

## Coverage Details

### Covered Code (97%)
The characterization tests cover:
- ✅ All quality update logic for normal items
- ✅ All quality update logic for Aged Brie
- ✅ All quality update logic for Backstage passes
- ✅ All quality update logic for Sulfuras
- ✅ Quality boundary enforcement (0 and 50)
- ✅ Sell-in date transitions
- ✅ All conditional branches in update_quality()
- ✅ Multiple items processing

### Missing Coverage (3%)
**Line 46**: `Item.__repr__` method
- This is the string representation method (`__repr__`)
- Not critical for business logic
- Only used for debugging/printing
- Can be tested if needed for completeness

---

## Key Test Patterns

### Boundary Testing
- Quality at 0, 1, 48, 49, 50
- Sell-in at -1, 0, 1, 5, 10, 11, 15
- Transitions across thresholds

### Edge Cases Covered
- Quality boundaries (min/max)
- Sell date transitions (before/at/after)
- Multiple quality increases per day (Backstage passes)
- No changes (Sulfuras)
- Accelerated degradation (past sell date)

### Multi-Day Progression
- Tests verify behavior over consecutive days
- Ensures state changes compound correctly
- Validates threshold crossings

---

## Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.0.1, pluggy-1.6.0
rootdir: C:\Workspace\Labb-2025-11-20\gildedrose\python
plugins: approvaltests-15.3.2, approvaltests-0.2.4
collected 41 items

tests/test_gilded_rose.py .........................................      [100%]

============================= 41 passed in 0.10s ==============================
```

### Coverage Report
```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
gilded_rose.py      36      1    97%   46
----------------------------------------------
TOTAL               36      1    97%
```

---

## Comparison: Before vs After

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Test Count | 1 (failing) | 41 (passing) | +4000% |
| Code Coverage | 53% | 97% | +44 percentage points |
| Test Classes | 1 | 8 | +700% |
| Business Logic Coverage | Partial | Comprehensive | ✅ Complete |

---

## Known Limitations

### Conjured Items
The "Conjured Mana Cake" feature is **not implemented** in the current codebase:
- **Current behavior**: Degrades like normal items (-1 quality/day)
- **Expected behavior**: Should degrade 2x as fast (-2 quality/day before sell date, -4 after)
- **Test status**: Test documents current behavior (passes)
- **Action needed**: Implement Conjured items feature

### Approval Tests
The approval test (`test_gilded_rose_approvals.py`) is currently failing due to:
- Missing/empty baseline file
- Reporter configuration issues
- Can be fixed by updating the approved baseline

---

## Recommendations

### For Refactoring
1. ✅ **Ready to refactor** - 97% coverage provides excellent safety net
2. Run tests frequently during refactoring
3. All tests should continue to pass after refactoring
4. Consider adding one test for `__repr__` if aiming for 100% coverage

### For New Features
1. **Implement Conjured items**:
   - Update test expectations in `ConjuredItemsTest`
   - Add comprehensive tests for conjured behavior
   - Test both before and after sell date
2. **Fix approval test**:
   - Update baseline file
   - Configure reporter for approval tests

### For Maintenance
1. Keep tests as characterization tests during refactoring
2. After refactoring, tests serve as regression tests
3. Add new tests for edge cases discovered during refactoring
4. Consider parameterized tests to reduce duplication

---

## Test Execution

### Run All Tests
```bash
cd python
python -m pytest tests/test_gilded_rose.py -v
```

### Run with Coverage
```bash
cd python
python -m coverage run --source=gilded_rose -m pytest tests/test_gilded_rose.py
python -m coverage report -m
python -m coverage html  # Generate HTML report in htmlcov/
```

### Run Specific Test Class
```bash
python -m pytest tests/test_gilded_rose.py::NormalItemsTest -v
python -m pytest tests/test_gilded_rose.py::BackstagePassesTest -v
```

### Run Single Test
```bash
python -m pytest tests/test_gilded_rose.py::NormalItemsTest::test_normal_item_after_sell_date -v
```

---

## Conclusion

The characterization test suite successfully captures all current behavior of the Gilded Rose inventory system with **97% code coverage**. All 41 tests pass, providing a comprehensive safety net for refactoring. The tests document:

- ✅ Normal item degradation patterns
- ✅ Aged Brie quality improvements
- ✅ Complex Backstage pass progression rules
- ✅ Sulfuras legendary item behavior
- ✅ Quality boundaries and constraints
- ✅ Sell-in date transitions and edge cases

**The codebase is now ready for safe refactoring.**
