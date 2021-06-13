create table datelog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  log_text string NOT NULL,
  detect string,
  DateInserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

