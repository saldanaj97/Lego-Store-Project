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
    PRIMARY KEY(SetID)
);

-- Make the table that will hold the piece type and count of each set 
CREATE TABLE brick_set_pieces (
    SetID int NOT NULL,
    BrickID int NOT NULL, 
    BrickCount int NOT NULL,
    BrickSize varchar(4) NOT NULL
);

SELECT * FROM individual_lego_bricks;

