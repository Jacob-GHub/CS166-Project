-- Auction lookups by status and seller (browse, my listings)
CREATE INDEX idx_auction_status ON auction (auction_status);

CREATE INDEX idx_auction_seller ON auction (seller_login);

CREATE INDEX idx_auction_winner ON auction (winner_login);

-- Bid lookups by auction (bid history, close auction)
CREATE INDEX idx_bid_auction ON bid (auction_id);

CREATE INDEX idx_bid_buyer ON bid (buyer_login);

-- Item category filter and name search
CREATE INDEX idx_item_category ON item (category);

-- Payment and shipment by auction
CREATE INDEX idx_payment_auction ON payment (auction_id);

CREATE INDEX idx_shipment_auction ON shipment (auction_id);