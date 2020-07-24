CREATE TABLE brick_set_pieces (
    SetID int NOT NULL,
    BrickID int NOT NULL, 
    BrickCount int NOT NULL,
    BrickSize varchar(255) NOT NULL
);

CREATE TABLE items (
    ItemID int NOT NULL,
    BrickSize varchar(4),
    BrickColor varchar(10),
    BrickType VARCHAR(255),
    ItemType varchar(10) NOT NULL, 
    SetName varchar(255),
    SetPieceCount int, 
    ItemPrice DECIMAL(10,2) NOT NULL,
    Quantity int NOT NULL, 
    PRIMARY KEY(ItemID)
)

CREATE TABLE customer (
    CustomerID int NOT NULL,
    FirstName varchar(255) NOT NULL, 
    LastName varchar(255) NOT NULL,
    PhoneNumber varchar(255) NOT NULL, 
    Email varchar (255) NOT NULL, 
    HomeAddress varchar(255) NOT NULL,
    UserPassword varchar(255)
    PRIMARY KEY(CustomerID)
)

CREATE TABLE orders (
    OrderID int NOT NULL,
    CustomerID int NOT NULL, 
    PRIMARY KEY(OrderID),
    FOREIGN KEY(CustomerID) REFERENCES customer(CustomerID) ON DELETE CASCADE ON UPDATE CASCADE
)

CREATE TABLE order_items (
    OrderID int NOT NULL,
    ItemID int, 
    Quantity int, 
    Price int, 
    PRIMARY KEY(OrderID, ItemId),
    FOREIGN KEY(OrderID) REFERENCES orders (OrderID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(ItemID) REFERENCES items(ItemID) ON DELETE CASCADE ON UPDATE CASCADE
)

CREATE TABLE employees (
    EmployeeID int NOT NULL, 
    FirstName varchar(255),
    LastName varchar(255),
    Email varchar(255),
    EmpPassword varchar(255),
    PRIMARY KEY(EmployeeID)
)

SELECT * FROM items;
SELECT * FROM brick_set_pieces;
SELECT * FROM customer;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM employees;
