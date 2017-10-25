#MySQL
CREATE TABLE "sinais"
(
  "sin_id" int(11) NOT NULL AUTO_INCREMENT,
  "sin_data" datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "sin_temp" float NOT NULL,
  "sin_umid" float NOT NULL,
)
ENGINE = InnoDB DEFAULT CHARSET = utf8;