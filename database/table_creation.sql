-- Make the inventory tables for individual blocks
CREATE TABLE individual_lego_bricks (
    BrickID int NOT NULL,
    BrickSize varchar(4) NOT NULL,
    BrickColor varchar(10) NOT NULL,
    BrickPrice DECIMAL (8,2) NOT NULL,
    BrickQuantity int NOT NULL,
    BrickType VARCHAR(255),
    PRIMARY KEY (BrickID)
);

-- Make the inventory tables for sets
CREATE TABLE lego_brick_sets (
    SetID int NOT NULL,
    SetName varchar(255) NOT NULL,
    SetPieceCount int,
    SetQuantity int
    PRIMARY KEY(SetID)
);

-- Make the table that will hold the piece type and count of each set 
CREATE TABLE brick_set_pieces (
    SetID int NOT NULL,
    BrickID int NOT NULL, 
    BrickCount int NOT NULL,
    BrickSize varchar(255) NOT NULL
);

CREATE TABLE customer (
    CustomerID int NOT NULL,
    FirstName varchar(255) NOT NULL, 
    LastName varchar(255) NOT NULL,
    PhoneNumber varchar(255) NOT NULL, 
    Email varchar (255) NOT NULL, 
    HomeAddress varchar(255) NOT NULL,
    PRIMARY KEY(CustomerID)
)

CREATE TABLE orders (
    OrderID int NOT NULL,
    CustomerID int NOT NULL, 
    PRIMARY KEY(OrderID)
)

CREATE TABLE order_items (
    OrderID int NOT NULL,
    ItemID int, 
    Quantity int, 
    Price int, 
    PRIMARY KEY(OrderID, ItemId)
)

CREATE TABLE employees (
    EmployeeID int NOT NULL, 
    FirstName varchar(255),
    LastName varchar(255),
    Email varchar(255),
    PRIMARY KEY(EmployeeID)
)

SELECT * FROM brick_set_pieces;
SELECT * FROM customer;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM employees;
