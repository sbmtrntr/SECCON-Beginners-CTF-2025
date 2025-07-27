CREATE DATABASE IF NOT EXISTS memodb
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE memodb;

CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  password TEXT
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS memos (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36),
  body TEXT,
  visibility ENUM('public','private','secret') NOT NULL,
  password TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

INSERT IGNORE INTO users (id, username, password) VALUES
('dummy_admin_id', 'admin', 'dummy_admin_pass');

INSERT IGNORE INTO memos (id, user_id, body, visibility, password) VALUES
('dummy_admin_memo_id', 'dummy_admin_id', 'ctf4b{dummy_flag}', 'secret', 'dummy_admin_memo_pass');