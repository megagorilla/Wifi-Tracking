CREATE TABLE IF NOT EXISTS `tracking`.`Locations` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Users_ID` INT NOT NULL,
  `X` DOUBLE NOT NULL,
  `Y` DOUBLE NOT NULL,
  `Z` DOUBLE NULL,
  `Time` DATETIME NULL,
  PRIMARY KEY (`ID`),
  INDEX `fk_Locations_Users_idx` (`Users_ID` ASC),
  CONSTRAINT `fk_Locations_Users`
    FOREIGN KEY (`Users_ID`)
    REFERENCES `tracking`.`Users` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
