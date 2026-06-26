import { google } from 'googleapis';
import axios from 'axios';

const name  = process.env.LEAD_NAME  || '—';
const phone = process.env.LEAD_PHONE || '—';
const tg    = process.env.LEAD_TG    || '—';
const date  = new Date().toLocaleString('uk-UA', { timeZone: 'Europe/Kiev' });

// Google Sheets
const auth = new google.auth.JWT(
  process.env.GOOGLE_CLIENT_EMAIL,
  null,
  process.env.GOOGLE_PRIVATE_KEY.replace(/\\n/g, '\n'),
  ['https://www.googleapis.com/auth/spreadsheets']
);
const sheets = google.sheets({ version: 'v4', auth });
await sheets.spreadsheets.values.append({
  spreadsheetId: '1C5hc-HYXTIeAZGKSL7wrZthBd6Lwd8P7-Ptm_7OW5q8',
  range: 'Ліди з сайту!A:E',
  valueInputOption: 'RAW',
  requestBody: { values: [[date, name, phone, tg, 'Сайт']] }
});
console.log('✓ Записано в Sheets');

// Telegram
await axios.post(`https://api.telegram.org/bot${process.env.TG_TOKEN}/sendMessage`, {
  chat_id: '-1003970612016',
  message_thread_id: 1088,
  text: `📋 *Лід збережено в таблицю*\n\n👤 ${name}\n📞 ${phone}${tg !== '—' ? '\n✈️ ' + tg : ''}\n🕐 ${date}`,
  parse_mode: 'Markdown'
});
console.log('✓ Telegram сповіщення надіслано');
