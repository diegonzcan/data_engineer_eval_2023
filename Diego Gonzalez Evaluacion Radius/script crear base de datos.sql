

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';



-- -----------------------------------------------------
-- Schema Sales
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Sales` DEFAULT CHARACTER SET utf8 ;
USE `Sales` ;

-- -----------------------------------------------------
-- Table `Sales`.`SalesTerritory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Sales`.`SalesTerritory` ;

CREATE TABLE IF NOT EXISTS `Sales`.`SalesTerritory` (
  `TerritoryID` INT NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  `CountryRegionCode` VARCHAR(3) NOT NULL,
  `Group` VARCHAR(50) NOT NULL,
  `SalesYTD` DOUBLE NOT NULL DEFAULT 0.0,
  `SalesLastYear` FLOAT NOT NULL,
  `CostYTD` FLOAT NOT NULL,
  `CostLastYear` FLOAT NOT NULL,
  `rowguid` VARCHAR(128) NOT NULL,
  `ModifiedDate` DATETIME NOT NULL,
  PRIMARY KEY (`TerritoryID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Sales`.`SalesOrderHeader`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Sales`.`SalesOrderHeader` ;

CREATE TABLE IF NOT EXISTS `Sales`.`SalesOrderHeader` (
  `SalesOrderID` INT NOT NULL,
  `RevisionNumber` TINYINT(10) NOT NULL,
  `OrderDate` DATETIME NOT NULL,
  `DueDate` DATETIME NOT NULL,
  `ShipDate` DATETIME NULL,
  `Status` TINYINT(10) NOT NULL,
  `OnlineOrderFlag` VARCHAR(20) NOT NULL,
  `SalesOrderNumber` TINYINT(10) NULL,
  `PurchaseOrderNumber` INT NULL,
  `AccountNumber` INT NULL,
  `TerritoryID` INT NULL,
  `CreditCardApprovalCode` VARCHAR(15) NULL,
  `SubTotal` FLOAT NOT NULL DEFAULT 0.0,
  `TaxAmt` FLOAT NOT NULL DEFAULT 0.0,
  `Freight` FLOAT NOT NULL DEFAULT 0.0,
  `TotalDue` FLOAT NOT NULL DEFAULT 0.0,
  `Comment` VARCHAR(128) NULL,
  `rowguid` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`SalesOrderID`),
  INDEX `TerritoryID_idx` (`TerritoryID` ASC) VISIBLE,
  CONSTRAINT `TerritoryID`
    FOREIGN KEY (`TerritoryID`)
    REFERENCES `Sales`.`SalesTerritory` (`TerritoryID`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Sales`.`SalesTerritoryHistory`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Sales`.`SalesTerritoryHistory` ;

CREATE TABLE IF NOT EXISTS `Sales`.`SalesTerritoryHistory` (
  `BusinessEntityID` INT NOT NULL,
  `TerritoryID_KEY` INT NOT NULL,
  `StartDate` DATETIME NOT NULL,
  `EndDate` DATETIME NULL,
  `rowguid` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`BusinessEntityID`),
  INDEX `TerritoryID_idx` (`TerritoryID_KEY` ASC) VISIBLE,
  CONSTRAINT `TerritoryID_KEY`
    FOREIGN KEY (`TerritoryID_KEY`)
    REFERENCES `Sales`.`SalesTerritory` (`TerritoryID`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Sales`.`SalesOrderDetail`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Sales`.`SalesOrderDetail` ;

CREATE TABLE IF NOT EXISTS `Sales`.`SalesOrderDetail` (
  `SalesOrderID` INT NOT NULL,
  `SalesOrderDetailID` INT NULL,
  `CarrierTrackingNumber` VARCHAR(25) NULL,
  `OrderQTY` SMALLINT(10) NULL,
  `ProductID` INT NULL,
  `SpecialOfferID` INT NULL,
  `UnitPrice` FLOAT NULL,
  `UnitPriceDiscount` FLOAT NULL,
  `LineTotal` FLOAT NULL,
  `rowguid` VARCHAR(45) NULL,
  `ModifiedDate` VARCHAR(45) NULL,
  PRIMARY KEY (`SalesOrderID`),
  CONSTRAINT `SalesOrderID`
    FOREIGN KEY (`SalesOrderID`)
    REFERENCES `Sales`.`SalesOrderHeader` (`SalesOrderID`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
