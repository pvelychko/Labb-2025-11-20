# Gilded Rose Business Rules

## Overview

The Gilded Rose inn maintains an inventory system that automatically updates item quality and sell-in values each day. This document provides a comprehensive reference for how different item types behave.

## Core Mechanics

- **SellIn**: Number of days remaining to sell the item (decreases by 1 each day)
- **Quality**: Value/condition of the item (ranges from 0-50 for most items)
- Items update at the end of each day

## Item Type Behavior Summary

| Item Type | Quality Change (Before Sell Date) | Quality Change (After Sell Date) | SellIn Changes | Quality Range |
|-----------|-----------------------------------|----------------------------------|----------------|---------------|
| **Normal Items** | -1 per day | -2 per day | -1 per day | 0-50 |
| **Aged Brie** | +1 per day | +2 per day | -1 per day | 0-50 |
| **Backstage Passes** | +1 (>10 days)<br>+2 (6-10 days)<br>+3 (1-5 days) | 0 (drops to zero) | -1 per day | 0-50 |
| **Sulfuras** | No change (stays at 80) | No change | No change | 80 (fixed) |
| **Conjured Items** | -2 per day | -4 per day | -1 per day | 0-50 |

## Detailed Rules

### Normal Items
- Quality decreases by 1 each day
- Once sell-by date passes (SellIn < 0), quality degrades twice as fast (-2 per day)
- Quality never goes below 0
- SellIn decreases by 1 each day

### Aged Brie
- Quality increases by 1 each day (gets better with age)
- Once sell-by date passes, quality increases by 2 per day
- Quality never exceeds 50
- SellIn decreases by 1 each day

### Backstage Passes to a TAFKAL80ETC Concert
- Quality increases as the concert approaches:
  - More than 10 days away: +1 quality per day
  - 10 days or less: +2 quality per day
  - 5 days or less: +3 quality per day
- After the concert (SellIn < 0): Quality drops to 0
- Quality never exceeds 50 (before concert)
- SellIn decreases by 1 each day

### Sulfuras, Hand of Ragnaros
- Legendary item with special properties:
  - Quality is always 80 (never changes)
  - Never has to be sold (SellIn never changes)
  - Never decreases in quality

### Conjured Items
- Degrade twice as fast as normal items
- Quality decreases by 2 each day
- Once sell-by date passes, quality degrades by 4 per day
- Quality never goes below 0
- SellIn decreases by 1 each day

## Universal Constraints

1. **Quality Bounds**: Quality of an item is never negative
2. **Quality Maximum**: Quality never exceeds 50 (except Sulfuras which is fixed at 80)
3. **Item Class Immutability**: The Item class cannot be modified (goblin's code)

## Examples

### Example 1: Normal Item Lifecycle

| Day | Name | SellIn | Quality | Notes |
|-----|------|--------|---------|-------|
| 0 | +5 Dexterity Vest | 10 | 20 | Initial state |
| 1 | +5 Dexterity Vest | 9 | 19 | -1 quality, -1 sell_in |
| 2 | +5 Dexterity Vest | 8 | 18 | -1 quality, -1 sell_in |
| 10 | +5 Dexterity Vest | 0 | 10 | At sell-by date |
| 11 | +5 Dexterity Vest | -1 | 8 | **Past sell date: -2 quality per day** |
| 12 | +5 Dexterity Vest | -2 | 6 | -2 quality, -1 sell_in |
| 15 | +5 Dexterity Vest | -5 | 0 | Quality bottoms out at 0 |

### Example 2: Aged Brie Lifecycle

| Day | Name | SellIn | Quality | Notes |
|-----|------|--------|---------|-------|
| 0 | Aged Brie | 2 | 0 | Initial state |
| 1 | Aged Brie | 1 | 1 | +1 quality, -1 sell_in |
| 2 | Aged Brie | 0 | 2 | +1 quality, -1 sell_in |
| 3 | Aged Brie | -1 | 4 | **Past sell date: +2 quality per day** |
| 4 | Aged Brie | -2 | 6 | +2 quality, -1 sell_in |
| 25 | Aged Brie | -23 | 50 | Quality caps at 50 |
| 26 | Aged Brie | -24 | 50 | Stays at maximum |

### Example 3: Backstage Passes Lifecycle

| Day | Name | SellIn | Quality | Notes |
|-----|------|--------|---------|-------|
| 0 | Backstage passes | 15 | 20 | Initial state (>10 days) |
| 1 | Backstage passes | 14 | 21 | +1 quality |
| 5 | Backstage passes | 10 | 25 | Still +1 quality |
| 6 | Backstage passes | 9 | 27 | **Now ≤10 days: +2 quality** |
| 10 | Backstage passes | 5 | 35 | At 5-day threshold |
| 11 | Backstage passes | 4 | 38 | **Now ≤5 days: +3 quality** |
| 14 | Backstage passes | 1 | 47 | +3 quality |
| 15 | Backstage passes | 0 | 50 | +3 quality (capped at 50) |
| 16 | Backstage passes | -1 | 0 | **Concert passed: drops to 0** |
| 17 | Backstage passes | -2 | 0 | Stays at 0 |

### Example 4: Sulfuras (Legendary Item)

| Day | Name | SellIn | Quality | Notes |
|-----|------|--------|---------|-------|
| 0 | Sulfuras, Hand of Ragnaros | 0 | 80 | Initial state |
| 1 | Sulfuras, Hand of Ragnaros | 0 | 80 | **Never changes** |
| 100 | Sulfuras, Hand of Ragnaros | 0 | 80 | **Still never changes** |

### Example 5: Conjured Item Lifecycle

| Day | Name | SellIn | Quality | Notes |
|-----|------|--------|---------|-------|
| 0 | Conjured Mana Cake | 3 | 6 | Initial state |
| 1 | Conjured Mana Cake | 2 | 4 | -2 quality, -1 sell_in |
| 2 | Conjured Mana Cake | 1 | 2 | -2 quality, -1 sell_in |
| 3 | Conjured Mana Cake | 0 | 0 | Reaches 0 quality |
| 4 | Conjured Mana Cake | -1 | 0 | **Past sell date: would be -4 but capped at 0** |

## Edge Cases

### Quality Boundaries
- Quality cannot go below 0 (even with accelerated degradation)
- Quality cannot exceed 50 (except Sulfuras at fixed 80)
- When quality would exceed 50, it remains at 50

### Sell-In Boundaries
- SellIn can go negative (except Sulfuras)
- The threshold for "expired" is SellIn < 0
- Backstage passes drop to 0 quality when SellIn < 0

### Multiple Quality Changes
Backstage passes can gain up to +3 quality per day, but total quality still cannot exceed 50.

## Implementation Notes

### DO NOT MODIFY
- The Item class structure (name, sell_in, quality fields)
- The items property

### CAN MODIFY
- The update_quality() method
- Add new classes or methods as needed
- Refactor internal logic
