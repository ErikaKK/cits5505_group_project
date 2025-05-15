# Routes
## `/account/upload-file`
- Key changes:
1. Now checks for actual timestamp overlaps within overlapping dates
2. Only considers it a conflict if the same exact  timestamp has different data
3. Merges complementary data even on overlapping dates
4. Preserves all unique entries from both datasets
5. Maintains chronological order
- The logic now is:
1. Find overlapping dates
2. For each overlapping date:
   1. Check if there are any common timestamps
   2. If common timestamps exist, compare the actual data
   3. Only flag as conflict if same timestamp has different data
3. If no real conflicts:
   1. Merge all unique entries
   2. Sort by timestamp
4. If real conflicts:
   1.  Show conflict dialog

## `/accocunt/replace-data`
