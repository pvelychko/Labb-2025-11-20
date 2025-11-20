# -*- coding: utf-8 -*-
"""
Characterization tests for Gilded Rose
These tests document the current behavior of the system before refactoring
"""
import unittest
from gilded_rose import Item, GildedRose


class NormalItemsTest(unittest.TestCase):
    """Tests for normal items (not special items)"""

    def test_normal_item_before_sell_date(self):
        """Normal items degrade by 1 quality per day before sell date"""
        items = [Item("+5 Dexterity Vest", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 19)

    def test_normal_item_on_sell_date(self):
        """Normal items at sell date (sell_in=0) still degrade by 1"""
        items = [Item("Normal Item", sell_in=0, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 8)  # After sell date, degrades by 2

    def test_normal_item_after_sell_date(self):
        """Normal items degrade twice as fast after sell date"""
        items = [Item("Elixir of the Mongoose", sell_in=-1, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 8)  # Degrades by 2

    def test_normal_item_quality_never_negative(self):
        """Normal items quality never goes below 0"""
        items = [Item("Normal Item", sell_in=5, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)

    def test_normal_item_quality_zero_after_sell_date(self):
        """Quality stays at 0 even after sell date with 2x degradation"""
        items = [Item("Normal Item", sell_in=-1, quality=1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)

    def test_vegemite_as_normal_item(self):
        """Vegemite behaves as a normal item"""
        items = [Item("Vegemite", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 19)

    def test_vegemite_after_sell_date(self):
        """Vegemite degrades twice as fast after sell date"""
        items = [Item("Vegemite", sell_in=-1, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 8)

    def test_vegemite_multiple_days(self):
        """Vegemite degrades correctly over multiple days"""
        items = [Item("Vegemite", sell_in=2, quality=10)]
        gilded_rose = GildedRose(items)

        # Day 1: sell_in=2, quality=10 -> sell_in=1, quality=9
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 9)

        # Day 2: sell_in=1, quality=9 -> sell_in=0, quality=8
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 8)

        # Day 3: sell_in=0, quality=8 -> sell_in=-1, quality=6 (2x degradation)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 6)


class AgedBrieTest(unittest.TestCase):
    """Tests for Aged Brie - increases in quality over time"""

    def test_aged_brie_increases_quality_before_sell_date(self):
        """Aged Brie increases in quality by 1 before sell date"""
        items = [Item("Aged Brie", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 21)

    def test_aged_brie_increases_quality_at_sell_date(self):
        """Aged Brie increases quality at sell_in=0"""
        items = [Item("Aged Brie", sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 22)  # Increases by 2 after sell date

    def test_aged_brie_increases_twice_as_fast_after_sell_date(self):
        """Aged Brie increases by 2 quality per day after sell date"""
        items = [Item("Aged Brie", sell_in=-1, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 22)

    def test_aged_brie_quality_caps_at_50(self):
        """Aged Brie quality never exceeds 50"""
        items = [Item("Aged Brie", sell_in=10, quality=50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_aged_brie_quality_caps_at_50_after_sell_date(self):
        """Aged Brie quality caps at 50 even with +2 increase"""
        items = [Item("Aged Brie", sell_in=-1, quality=49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_aged_brie_from_zero_quality(self):
        """Aged Brie can start at 0 quality and increase"""
        items = [Item("Aged Brie", sell_in=5, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 1)


class BackstagePassesTest(unittest.TestCase):
    """Tests for Backstage passes - complex quality progression"""

    def test_backstage_passes_more_than_10_days(self):
        """Backstage passes increase by 1 when >10 days away"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 14)
        self.assertEqual(items[0].quality, 21)

    def test_backstage_passes_at_10_days(self):
        """Backstage passes increase by 2 at exactly 10 days"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 22)  # +2 when <=10 days

    def test_backstage_passes_between_6_and_10_days(self):
        """Backstage passes increase by 2 when 6-10 days away"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=8, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 7)
        self.assertEqual(items[0].quality, 22)

    def test_backstage_passes_at_5_days(self):
        """Backstage passes increase by 3 at exactly 5 days"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 23)  # +3 when <=5 days

    def test_backstage_passes_between_1_and_5_days(self):
        """Backstage passes increase by 3 when 1-5 days away"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=3, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 2)
        self.assertEqual(items[0].quality, 23)

    def test_backstage_passes_at_sell_date(self):
        """Backstage passes at sell_in=0 still increase by 3"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 0)  # Drops to 0 after concert

    def test_backstage_passes_after_concert(self):
        """Backstage passes drop to 0 quality after concert"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=-1, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 0)

    def test_backstage_passes_quality_caps_at_50(self):
        """Backstage passes quality never exceeds 50"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)  # Would be 52, but caps at 50

    def test_backstage_passes_near_max_quality_10_days(self):
        """Backstage passes at 49 quality with 10 days increases to 50"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_backstage_passes_multiple_days_progression(self):
        """Backstage passes progress correctly over multiple days"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=12, quality=20)]
        gilded_rose = GildedRose(items)

        # Day 1: 12->11, quality 20->21 (+1)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 11)
        self.assertEqual(items[0].quality, 21)

        # Day 2: 11->10, quality 21->22 (+1)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 10)
        self.assertEqual(items[0].quality, 22)

        # Day 3: 10->9, quality 22->24 (+2)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 24)


class SulfurasTest(unittest.TestCase):
    """Tests for Sulfuras - legendary item that never changes"""

    def test_sulfuras_quality_never_changes(self):
        """Sulfuras quality stays at 80"""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 80)

    def test_sulfuras_sell_in_never_changes(self):
        """Sulfuras sell_in never decreases"""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 10)

    def test_sulfuras_at_zero_sell_in(self):
        """Sulfuras at sell_in=0 never changes"""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 80)

    def test_sulfuras_after_sell_date(self):
        """Sulfuras with negative sell_in never changes"""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 80)

    def test_sulfuras_multiple_updates(self):
        """Sulfuras never changes even after multiple days"""
        items = [Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80)]
        gilded_rose = GildedRose(items)

        for _ in range(10):
            gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 5)
        self.assertEqual(items[0].quality, 80)


class QualityBoundsTest(unittest.TestCase):
    """Tests for quality boundaries (0-50)"""

    def test_quality_never_negative_normal_item(self):
        """Normal item quality stops at 0"""
        items = [Item("Normal Item", sell_in=5, quality=1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)

        # One more day should stay at 0
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0)

    def test_quality_never_exceeds_50_aged_brie(self):
        """Aged Brie quality stops at 50"""
        items = [Item("Aged Brie", sell_in=5, quality=50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_quality_never_exceeds_50_backstage_passes(self):
        """Backstage passes quality stops at 50"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_quality_at_49_can_reach_50(self):
        """Quality at 49 can increase to 50"""
        items = [Item("Aged Brie", sell_in=5, quality=49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_quality_at_48_with_double_increase(self):
        """Quality at 48 with +2 increase reaches 50"""
        items = [Item("Aged Brie", sell_in=-1, quality=48)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)

    def test_quality_at_48_with_triple_increase(self):
        """Quality at 48 with +3 increase caps at 50"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=48)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 50)


class SellInEdgeCasesTest(unittest.TestCase):
    """Tests for sell-in date edge cases"""

    def test_sell_in_decreases_for_normal_items(self):
        """Sell-in decreases by 1 each day for normal items"""
        items = [Item("Normal Item", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 4)

    def test_sell_in_decreases_for_aged_brie(self):
        """Sell-in decreases by 1 each day for Aged Brie"""
        items = [Item("Aged Brie", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 4)

    def test_sell_in_decreases_for_backstage_passes(self):
        """Sell-in decreases by 1 each day for Backstage passes"""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 4)

    def test_sell_in_can_go_negative(self):
        """Sell-in can go negative for normal items"""
        items = [Item("Normal Item", sell_in=0, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)

    def test_transition_at_sell_date_normal_item(self):
        """Normal item transitions from -1 quality to -2 quality at sell date"""
        items = [Item("Normal Item", sell_in=1, quality=10)]
        gilded_rose = GildedRose(items)

        # Day 1: sell_in=1, quality degrades by 1
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 9)

        # Day 2: sell_in=0->-1, quality degrades by 2
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 7)

    def test_transition_at_sell_date_aged_brie(self):
        """Aged Brie transitions from +1 quality to +2 quality at sell date"""
        items = [Item("Aged Brie", sell_in=1, quality=10)]
        gilded_rose = GildedRose(items)

        # Day 1: sell_in=1, quality increases by 1
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 11)

        # Day 2: sell_in=0->-1, quality increases by 2
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 13)


class MultipleItemsTest(unittest.TestCase):
    """Tests with multiple items at once"""

    def test_multiple_items_update_independently(self):
        """Multiple items update independently"""
        items = [
            Item("+5 Dexterity Vest", sell_in=10, quality=20),
            Item("Aged Brie", sell_in=2, quality=0),
            Item("Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Normal item
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 19)

        # Aged Brie
        self.assertEqual(items[1].sell_in, 1)
        self.assertEqual(items[1].quality, 1)

        # Sulfuras
        self.assertEqual(items[2].sell_in, 0)
        self.assertEqual(items[2].quality, 80)

    def test_all_item_types_together(self):
        """All item types work correctly together"""
        items = [
            Item("Normal Item", sell_in=5, quality=10),
            Item("Aged Brie", sell_in=5, quality=10),
            Item("Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10),
            Item("Sulfuras, Hand of Ragnaros", sell_in=5, quality=80),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 9)   # Normal: -1
        self.assertEqual(items[1].quality, 11)  # Brie: +1
        self.assertEqual(items[2].quality, 13)  # Backstage: +3 (<=5 days)
        self.assertEqual(items[3].quality, 80)  # Sulfuras: no change


class ConjuredItemsTest(unittest.TestCase):
    """Tests for Conjured items - degrade 2x as fast as normal items"""

    def test_conjured_item_before_sell_date(self):
        """Conjured items degrade by 2 quality per day before sell date"""
        items = [Item("Conjured Mana Cake", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 18)  # -2 quality (2x normal)

    def test_conjured_item_on_sell_date(self):
        """Conjured items at sell_in=0 degrade by 2"""
        items = [Item("Conjured Mana Cake", sell_in=0, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 6)  # -4 quality after sell date

    def test_conjured_item_after_sell_date(self):
        """Conjured items degrade by 4 quality per day after sell date"""
        items = [Item("Conjured Mana Cake", sell_in=-1, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 6)  # -4 quality (2x normal after sell)

    def test_conjured_item_quality_never_negative(self):
        """Conjured items quality never goes below 0"""
        items = [Item("Conjured Mana Cake", sell_in=5, quality=1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)  # Would be -1, but caps at 0

    def test_conjured_item_quality_zero_after_sell_date(self):
        """Conjured items quality stays at 0 even with 4x degradation"""
        items = [Item("Conjured Mana Cake", sell_in=-1, quality=2)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].quality, 0)  # Would be -2, but caps at 0

    def test_conjured_item_multiple_days(self):
        """Conjured items degrade correctly over multiple days"""
        items = [Item("Conjured Mana Cake", sell_in=2, quality=10)]
        gilded_rose = GildedRose(items)

        # Day 1: sell_in=2, quality=10 -> sell_in=1, quality=8 (-2)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 1)
        self.assertEqual(items[0].quality, 8)

        # Day 2: sell_in=1, quality=8 -> sell_in=0, quality=6 (-2)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 6)

        # Day 3: sell_in=0, quality=6 -> sell_in=-1, quality=2 (-4)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -1)
        self.assertEqual(items[0].quality, 2)

        # Day 4: sell_in=-1, quality=2 -> sell_in=-2, quality=0 (-4 but capped)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, -2)
        self.assertEqual(items[0].quality, 0)

    def test_conjured_with_different_name(self):
        """Any item with 'Conjured' prefix degrades 2x as fast"""
        items = [Item("Conjured Aged Brie", sell_in=5, quality=10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 4)
        self.assertEqual(items[0].quality, 8)  # -2 quality (conjured behavior)

    def test_conjured_mana_cake_original_spec(self):
        """Original spec test case for Conjured Mana Cake"""
        items = [Item("Conjured Mana Cake", sell_in=3, quality=6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        self.assertEqual(items[0].sell_in, 2)
        self.assertEqual(items[0].quality, 4)  # -2 quality (was -1, now fixed)


if __name__ == '__main__':
    unittest.main()
