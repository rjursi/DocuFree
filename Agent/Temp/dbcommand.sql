create table datelog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  log_text string NOT NULL,
  datect string,
  DateInserted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

