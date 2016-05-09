CREATE TABLE IF NOT EXISTS `tracking`.`Ranges` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `Users_ID` INT NOT NULL,
    `Sniffers_ID` INT NOT NULL,
    `Range` INT NOT NULL,
    `Time` DATETIME NOT NULL,
    INDEX `fk_Ranges_Users1_idx` (`Users_ID` ASC),
    INDEX `fk_Ranges_Sniffers1_idx` (`Sniffers_ID` ASC),
    PRIMARY KEY (`ID`),
    CONSTRAINT `fk_Ranges_Users1` FOREIGN KEY (`Users_ID`)
        REFERENCES `tracking`.`Users` (`ID`)
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `fk_Ranges_Sniffers1` FOREIGN KEY (`Sniffers_ID`)
        REFERENCES `tracking`.`Sniffers` (`ID`)
        ON DELETE NO ACTION ON UPDATE NO ACTION
)  ENGINE=INNODB
