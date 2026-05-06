DROP TABLE IF EXISTS Shipment;

DROP TABLE IF EXISTS Payment;

DROP TABLE IF EXISTS Bid;

DROP TABLE IF EXISTS Auction;

DROP TABLE IF EXISTS Item;

DROP TABLE IF EXISTS Users;

CREATE TABLE
    Users (
        login VARCHAR(50) PRIMARY KEY,
        password VARCHAR(100) NOT NULL,
        phoneNum VARCHAR(20) NOT NULL,
        role VARCHAR(10) NOT NULL CHECK (role IN ('Buyer', 'Seller', 'Admin')),
        address TEXT NOT NULL,
        favoriteCategory VARCHAR(50)
    );

CREATE TABLE
    Item (
        itemID INT PRIMARY KEY,
        itemName VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        imageURL TEXT,
        condition VARCHAR(50),
        description TEXT,
        startingPrice DECIMAL(10, 2) NOT NULL,
        seller_login VARCHAR(50) NOT NULL,
        FOREIGN KEY (seller_login) REFERENCES Users (login)
    );

CREATE TABLE
    Auction (
        auctionID INT PRIMARY KEY,
        auctionStatus VARCHAR(50) CHECK (auctionStatus IN ('Active', 'Closed')),
        currentHighestBid DECIMAL(10, 2),
        itemID INT UNIQUE NOT NULL,
        seller_login VARCHAR(50) NOT NULL,
        winner_login VARCHAR(50),
        FOREIGN KEY (itemID) REFERENCES Item (itemID),
        FOREIGN KEY (seller_login) REFERENCES Users (login),
        FOREIGN KEY (winner_login) REFERENCES Users (login)
    );

CREATE TABLE
    Bid (
        bidID INT PRIMARY KEY,
        bidAmount DECIMAL(10, 2) NOT NULL,
        bidTimestamp TIMESTAMP NOT NULL,
        auctionID INT NOT NULL,
        buyer_login VARCHAR(50) NOT NULL,
        FOREIGN KEY (auctionID) REFERENCES Auction (auctionID),
        FOREIGN KEY (buyer_login) REFERENCES Users (login)
    );

CREATE TABLE
    Payment (
        paymentID INT PRIMARY KEY,
        amount DECIMAL(10, 2) NOT NULL,
        paymentStatus VARCHAR(50) CHECK (
            paymentStatus IN ('Pending', 'Completed', 'Failed')
        ),
        auctionID INT UNIQUE NOT NULL,
        buyer_login VARCHAR(50) NOT NULL,
        FOREIGN KEY (auctionID) REFERENCES Auction (auctionID),
        FOREIGN KEY (buyer_login) REFERENCES Users (login)
    );

CREATE TABLE
    Shipment (
        shipmentID INT PRIMARY KEY,
        address TEXT NOT NULL,
        shipmentStatus VARCHAR(50) CHECK (
            shipmentStatus IN ('Pending', 'Shipped', 'Delivered')
        ),
        trackingNumber VARCHAR(100),
        auctionID INT UNIQUE NOT NULL,
        FOREIGN KEY (auctionID) REFERENCES Auction (auctionID)
    );