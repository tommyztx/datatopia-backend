CREATE TABLE Actor (
    ActorID VARCHAR(255) NULL,
    ActorName VARCHAR(255) NULL,
    ActorType VARCHAR(255) NULL,
    GenderCode VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE ArticleLabo (
    CnkNr VARCHAR(255) NULL,
    LaboratoryName VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Articles (
    CnkNr VARCHAR(255) NULL,
    ArtName VARCHAR(255) NULL,
    PATHOLOGY VARCHAR(255) NULL,
    cat1_fr VARCHAR(255) NULL,
    cat2_fr VARCHAR(255) NULL,
    cat3_fr VARCHAR(255) NULL,
    categories_simplifiees_fr VARCHAR(255) NULL,
    SupplierID VARCHAR(255) NULL,
    suppliername VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Customers (
    CustID VARCHAR(255) NULL,
    PatientID VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Historized_stocks (
    ArtID VARCHAR(255) NULL,
    QtyInStock int NULL,
    ReservedQty int NULL,
    MinThd int NULL,
    MaxThd int NULL,
    PubPricePerUnit float NULL,
    BuyPricePerUnit float NULL,
    stockDate date NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE last_orders (
    CnkNr VARCHAR(255) NULL,
    DateSupply date NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE min_max_recommendations (
    CnkNr VARCHAR(255) NULL,
    ArtName VARCHAR(255) NULL,
    Min_7d int NULL,
    Max_7d int NULL,
    Min_14d int NULL,
    Max_14d int NULL,
    Min_28d int NULL,
    Max_28d int NULL,
    problem int NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Patients (
    PatientID VARCHAR(255) NULL,
    IsRefPharmacist VARCHAR(255) NULL,
    DateBirth date NULL,
    GenderCode VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Sales (
    SlsID VARCHAR(255) NULL,
    SellerLabel VARCHAR(255) NULL,
    TimeSaleStart DATETIME NULL,
    CustID VARCHAR(255) NULL,
    SellerID VARCHAR(255) NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Salesitems (
    SlsID VARCHAR(255) NULL,
    VatRateCpy float NULL,
    ArtIDSold VARCHAR(255) NULL,
    SaleQty int NULL,
    PaidQty int NULL,
    Thirdpartypaid float NULL,
    AmntNetto float NULL,
    PubPerUnit float NULL,
    BuyPricePerUnit float NULL,
    AmntPaid float NULL,
    AmntRebateNetto float NULL,
    pharma_ID VARCHAR(10) NULL
);

CREATE TABLE Stocks (
    ArtID VARCHAR(255) NULL,
    QtyInStock int NULL,
    ReservedQty int NULL,
    MinThd int NULL,
    MaxThd int NULL,
    PubPricePerUnit float NULL,
    BuyPricePerUnit float NULL,
    stockDate date NULL,
    pharma_ID VARCHAR(10) NULL
);

# PharmaID is always 'BE_251410'

# If the question is unrelated to the pharmacy return 'I cannot answer questions that are not related to your pharmacy'

