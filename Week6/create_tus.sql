CREATE TABLE tus (
  gid_1       INT  (10) UNSIGNED NOT NULL,
  gid_2       INT  (10) UNSIGNED NOT NULL,
  distance    INT  (10) UNSIGNED NOT NULL,
  status      ENUM('TP', 'TN') NOT NULL,
  prob        DOUBLE PRECISION NOT NULL,
  KEY (gid_1),
  KEY (gid_2)
)ENGINE=InnoDB;
