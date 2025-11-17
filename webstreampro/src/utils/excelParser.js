const XLSX = require('xlsx');

function parseExcelFile(filePath) {
  try {
    const workbook = XLSX.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(worksheet);

    const broadcasts = data.map((row, index) => {
      const tags = row.tags ? 
        (typeof row.tags === 'string' ? row.tags.split(',').map(t => t.trim()) : []) : 
        [];

      return {
        title: row.title || `Untitled Broadcast ${index + 1}`,
        description: row.description || '',
        tags: tags,
        categoryId: row.categoryId ? String(row.categoryId) : '20',
        privacyStatus: row.privacyStatus || 'public',
        scheduledStartDate: row.scheduledStartDate || '',
        scheduledStartTime: row.scheduledStartTime || '',
        scheduledStartTime: formatScheduledTime(
          row.scheduledStartDate,
          row.scheduledStartTime
        ),
        thumbnailPath: row.thumbnailPath || '',
        streamId: row.streamId || '',
        streamKey: row.streamKey || '',
        latency: row.latency || 'normal',
        enableDvr: row.enableDvr !== false && row.enableDvr !== 'FALSE',
        enableEmbed: row.enableEmbed !== false && row.enableEmbed !== 'FALSE',
        recordFromStart: row.recordFromStart !== false && row.recordFromStart !== 'FALSE',
        madeForKids: row.madeForKids === true || row.madeForKids === 'TRUE',
        containsSyntheticMedia: row.containsSyntheticMedia === true || row.containsSyntheticMedia === 'TRUE',
        enableMonetization: row.enableMonetization === true || row.enableMonetization === 'TRUE'
      };
    });

    return { success: true, broadcasts };
  } catch (error) {
    console.error('Error parsing Excel file:', error);
    return { success: false, error: error.message };
  }
}

function formatScheduledTime(date, time) {
  if (!date || !time) {
    const now = new Date();
    now.setHours(now.getHours() + 1);
    return now.toISOString();
  }

  try {
    const dateStr = typeof date === 'string' ? date : excelDateToJSDate(date);
    const timeStr = typeof time === 'string' ? time : excelTimeToString(time);
    
    const [year, month, day] = dateStr.split('-');
    const [hour, minute] = timeStr.split(':');
    
    const scheduledDate = new Date(year, month - 1, day, hour, minute);
    return scheduledDate.toISOString();
  } catch (error) {
    console.error('Error formatting scheduled time:', error);
    const now = new Date();
    now.setHours(now.getHours() + 1);
    return now.toISOString();
  }
}

function excelDateToJSDate(excelDate) {
  const date = XLSX.SSF.parse_date_code(excelDate);
  return `${date.y}-${String(date.m).padStart(2, '0')}-${String(date.d).padStart(2, '0')}`;
}

function excelTimeToString(excelTime) {
  const totalMinutes = Math.round(excelTime * 24 * 60);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

module.exports = { parseExcelFile };
