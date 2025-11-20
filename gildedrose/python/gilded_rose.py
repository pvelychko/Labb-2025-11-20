# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Update quality and sell_in for all items"""
        for item in self.items:
            if self._is_aged_brie(item):
                self._update_aged_brie(item)
            elif self._is_backstage_pass(item):
                self._update_backstage_pass(item)
            elif self._is_sulfuras(item):
                self._update_sulfuras(item)
            elif self._is_conjured(item):
                self._update_conjured(item)
            else:
                self._update_normal_item(item)

    # Item type identification methods

    def _is_aged_brie(self, item):
        """Check if item is Aged Brie"""
        return item.name == "Aged Brie"

    def _is_backstage_pass(self, item):
        """Check if item is a Backstage pass"""
        return item.name == "Backstage passes to a TAFKAL80ETC concert"

    def _is_sulfuras(self, item):
        """Check if item is Sulfuras (legendary item)"""
        return item.name == "Sulfuras, Hand of Ragnaros"

    def _is_conjured(self, item):
        """Check if item is Conjured (degrades 2x as fast)"""
        return item.name.startswith("Conjured")

    # Quality change helper methods

    def _increase_quality(self, item, amount=1):
        """Increase quality by amount, respecting max of 50"""
        item.quality = min(50, item.quality + amount)

    def _decrease_quality(self, item, amount=1):
        """Decrease quality by amount, respecting min of 0"""
        item.quality = max(0, item.quality - amount)

    def _decrease_sell_in(self, item):
        """Decrease sell_in by 1"""
        item.sell_in = item.sell_in - 1

    # Item-specific update methods

    def _update_normal_item(self, item):
        """Update normal items (degrade over time)"""
        # Decrease quality before sell date
        self._decrease_quality(item)

        # Decrease sell_in
        self._decrease_sell_in(item)

        # After sell date, quality degrades twice as fast
        if item.sell_in < 0:
            self._decrease_quality(item)

    def _update_aged_brie(self, item):
        """Update Aged Brie (increases in quality over time)"""
        # Increase quality before sell date
        self._increase_quality(item)

        # Decrease sell_in
        self._decrease_sell_in(item)

        # After sell date, quality increases twice as fast
        if item.sell_in < 0:
            self._increase_quality(item)

    def _update_backstage_pass(self, item):
        """Update Backstage passes (complex quality progression)"""
        # Base increase
        self._increase_quality(item)

        # Additional increase when 10 days or less
        if item.sell_in < 11:
            self._increase_quality(item)

        # Additional increase when 5 days or less
        if item.sell_in < 6:
            self._increase_quality(item)

        # Decrease sell_in
        self._decrease_sell_in(item)

        # After concert, quality drops to 0
        if item.sell_in < 0:
            item.quality = 0

    def _update_sulfuras(self, item):
        """Update Sulfuras (legendary item - never changes)"""
        # Sulfuras never changes quality or sell_in
        pass

    def _update_conjured(self, item):
        """Update Conjured items (degrade 2x as fast as normal items)"""
        # Decrease quality by 2 (2x normal degradation)
        self._decrease_quality(item, amount=2)

        # Decrease sell_in
        self._decrease_sell_in(item)

        # After sell date, quality degrades by 4 total (2x of 2x)
        if item.sell_in < 0:
            self._decrease_quality(item, amount=2)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
