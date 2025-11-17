# Sample Excel Format

## Required Columns

| Column Name | Type | Description | Example |
|------------|------|-------------|---------|
| title | Text | Broadcast title | "My Live Stream #1" |
| description | Text | Broadcast description | "Welcome to my stream!" |
| tags | Text | Comma-separated tags | "gaming, live, fun" |
| categoryId | Number | YouTube category ID | 20 (Gaming) |
| privacyStatus | Text | Privacy setting | public, unlisted, private |

## Optional Columns

| Column Name | Type | Description | Default | Example |
|------------|------|-------------|---------|---------|
| scheduledStartDate | Date | Start date | Tomorrow | 2025-11-18 |
| scheduledStartTime | Time | Start time | 12:00 | 14:30 |
| thumbnailPath | Text | Path to thumbnail | (none) | C:\thumbnails\thumb1.jpg |
| streamId | Text | Reuse existing stream | (none) | abc123xyz |
| streamKey | Text | Custom stream key | (none) | my-stream-key |
| latency | Text | Stream latency | normal | normal, low, ultraLow |
| enableDvr | Boolean | Enable DVR | TRUE | TRUE, FALSE |
| enableEmbed | Boolean | Enable embed | TRUE | TRUE, FALSE |
| recordFromStart | Boolean | Record from start | TRUE | TRUE, FALSE |
| madeForKids | Boolean | Made for kids | FALSE | TRUE, FALSE |
| containsSyntheticMedia | Boolean | Has AI content | FALSE | TRUE, FALSE |
| enableMonetization | Boolean | Enable monetization | FALSE | TRUE, FALSE |

## Sample Data

### Example 1: Simple Broadcast

```
title,description,tags,categoryId,privacyStatus
My First Stream,This is my first live stream,gaming live fun,20,public
My Second Stream,Another awesome stream,gaming tutorial,20,unlisted
```

### Example 2: Complete Broadcast

```
title,description,tags,categoryId,privacyStatus,scheduledStartDate,scheduledStartTime,latency,enableDvr,madeForKids
Weekend Gaming,Join me for gaming,gaming live,20,public,2025-11-20,19:00,low,TRUE,FALSE
Tutorial Stream,Learning together,tutorial education,27,public,2025-11-21,15:00,normal,TRUE,FALSE
```

### Example 3: With Thumbnail

```
title,description,tags,categoryId,privacyStatus,thumbnailPath
Stream with Thumb,Check out this thumbnail!,gaming,20,public,C:\thumbnails\gaming.jpg
```

## YouTube Category IDs

Common category IDs:

- 1 = Film & Animation
- 2 = Autos & Vehicles
- 10 = Music
- 15 = Pets & Animals
- 17 = Sports
- 18 = Short Movies
- 19 = Travel & Events
- 20 = Gaming
- 22 = People & Blogs
- 23 = Comedy
- 24 = Entertainment
- 25 = News & Politics
- 26 = Howto & Style
- 27 = Education
- 28 = Science & Technology

## Tips

1. **Dates**: Use YYYY-MM-DD format (e.g., 2025-11-18)
2. **Times**: Use HH:MM 24-hour format (e.g., 14:30)
3. **Tags**: Separate multiple tags with commas
4. **Booleans**: Use TRUE or FALSE (case insensitive)
5. **Paths**: Use full path for thumbnails (e.g., C:\path\to\image.jpg)

## Creating Excel File

You can create the Excel file using:
- Microsoft Excel
- Google Sheets (export as .xlsx)
- LibreOffice Calc
- Any spreadsheet software that supports .xlsx format

Make sure to:
- Use the first row for column headers
- Match the column names exactly as shown above
- Save as .xlsx format
