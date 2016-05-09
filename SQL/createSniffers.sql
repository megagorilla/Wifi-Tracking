CREATE TABLE IF NOT EXISTS `tracking`.`Sniffers` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `NAME` VARCHAR(45) NULL,
  `X` DOUBLE NULL,
  `Y` DOUBLE NULL,
  `Z` DOUBLE NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
