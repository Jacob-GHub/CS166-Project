def login(esql, username, password):
    rows = esql.execute_query(
        "SELECT login, role FROM users WHERE login = %s AND password = %s;",
        (username, password)
    )
    return rows[0] if rows else None


def register(esql, login, password, phone, address):
    esql.execute_update(
        "INSERT INTO users (login, password, phone_num, address, role) VALUES (%s,%s,%s,%s,'Buyer');",
        (login, password, phone, address)
    )


def get_profile(esql, login):
    return esql.execute_query(
        "SELECT login, role, phone_num, address, favorite_category FROM users WHERE login = %s;",
        (login,)
    )


def update_profile(esql, login, phone, address, fav_category):
    esql.execute_update(
        "UPDATE users SET phone_num=%s, address=%s, favorite_category=%s WHERE login=%s;",
        (phone, address, fav_category or None, login)
    )


def browse_active_auctions(esql):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.seller_login
           FROM auction a JOIN item i ON a.item_id = i.item_id
           WHERE a.auction_status = 'Active' ORDER BY a.auction_id;"""
    )


def search_auctions(esql, keyword):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, i.category, a.current_highest_bid, a.auction_status
           FROM auction a JOIN item i ON a.item_id = i.item_id
           WHERE i.item_name ILIKE %s ORDER BY a.auction_id;""",
        (f"%{keyword}%",)
    )


def view_auction_detail(esql, auction_id):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, i.category, i.item_condition,
                  i.description, i.starting_price, a.current_highest_bid,
                  a.auction_status, a.seller_login, a.winner_login
           FROM auction a JOIN item i ON a.item_id = i.item_id
           WHERE a.auction_id = %s;""",
        (auction_id,)
    )
    esql.execute_query(
        "SELECT buyer_login, bid_amount, bid_timestamp FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC;",
        (auction_id,)
    )


def place_bid(esql, auction_id, buyer_login, amount):
    rows = esql.execute_query(
        "SELECT auction_status, seller_login, current_highest_bid FROM auction WHERE auction_id = %s;",
        (auction_id,)
    )
    if not rows:
        print("Auction not found.")
        return
    status, seller, high = rows[0]
    if status != 'Active':
        print("Auction is not active.")
    elif seller == buyer_login:
        print("You cannot bid on your own auction.")
    elif float(amount) <= float(high):
        print(f"Bid must exceed current highest bid of ${high}.")
    else:
        next_id = esql.execute_query("SELECT COALESCE(MAX(bid_id),0)+1 FROM bid;")[0][0]
        esql.execute_update(
            "INSERT INTO bid (bid_id, auction_id, buyer_login, buyer_role, bid_amount) VALUES (%s,%s,%s,'Buyer',%s);",
            (next_id, auction_id, buyer_login, amount)
        )
        esql.execute_update(
            "UPDATE auction SET current_highest_bid = %s WHERE auction_id = %s;",
            (amount, auction_id)
        )
        print(f"Bid of ${amount} placed.")


def my_bids(esql, buyer_login):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, MAX(b.bid_amount) AS my_high,
                  a.current_highest_bid, a.auction_status
           FROM bid b
           JOIN auction a ON b.auction_id = a.auction_id
           JOIN item i ON a.item_id = i.item_id
           WHERE b.buyer_login = %s
           GROUP BY a.auction_id, i.item_name, a.current_highest_bid, a.auction_status
           ORDER BY a.auction_id;""",
        (buyer_login,)
    )


def won_auctions(esql, buyer_login):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, a.current_highest_bid,
                  COALESCE(p.payment_status, 'No payment') AS payment,
                  COALESCE(s.shipment_status, 'Not shipped') AS shipment
           FROM auction a
           JOIN item i ON a.item_id = i.item_id
           LEFT JOIN payment p ON p.auction_id = a.auction_id
           LEFT JOIN shipment s ON s.auction_id = a.auction_id
           WHERE a.winner_login = %s;""",
        (buyer_login,)
    )


def create_listing(esql, seller_login, name, category, price, condition, desc):
    iid = esql.execute_query("SELECT COALESCE(MAX(item_id),0)+1 FROM item;")[0][0]
    aid = esql.execute_query("SELECT COALESCE(MAX(auction_id),0)+1 FROM auction;")[0][0]
    esql.execute_update(
        "INSERT INTO item (item_id, item_name, category, starting_price, item_condition, description, seller_login, seller_role) VALUES (%s,%s,%s,%s,%s,%s,%s,'Seller');",
        (iid, name, category, price, condition, desc, seller_login)
    )
    esql.execute_update(
        "INSERT INTO auction (auction_id, item_id, seller_login, seller_role, current_highest_bid, auction_status) VALUES (%s,%s,%s,'Seller',%s,'Active');",
        (aid, iid, seller_login, price)
    )
    print(f"Item #{iid} listed. Auction #{aid} is now active.")


def my_listings(esql, seller_login):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, a.current_highest_bid,
                  a.auction_status, COALESCE(a.winner_login, '-') AS winner
           FROM auction a JOIN item i ON a.item_id = i.item_id
           WHERE a.seller_login = %s ORDER BY a.auction_id;""",
        (seller_login,)
    )


def close_auction(esql, auction_id, seller_login):
    rows = esql.execute_query(
        "SELECT auction_status, seller_login, current_highest_bid FROM auction WHERE auction_id = %s;",
        (auction_id,)
    )
    if not rows:
        print("Auction not found.")
        return
    status, seller, high = rows[0]
    if seller != seller_login:
        print("That's not your auction.")
        return
    if status == 'Closed':
        print("Already closed.")
        return
    winner_rows = esql.execute_query(
        "SELECT buyer_login FROM bid WHERE auction_id = %s ORDER BY bid_amount DESC LIMIT 1;",
        (auction_id,)
    )
    winner = winner_rows[0][0] if winner_rows else None
    esql.execute_update(
        "UPDATE auction SET auction_status='Closed', winner_login=%s, winner_role=CASE WHEN %s IS NOT NULL THEN 'Buyer' ELSE NULL END WHERE auction_id=%s;",
        (winner, winner, auction_id)
    )
    if winner:
        pid = esql.execute_query("SELECT COALESCE(MAX(payment_id),0)+1 FROM payment;")[0][0]
        esql.execute_update(
            "INSERT INTO payment (payment_id, auction_id, buyer_login, buyer_role, amount, payment_status) VALUES (%s,%s,%s,'Buyer',%s,'Pending');",
            (pid, auction_id, winner, high)
        )
        print(f"Closed. Winner: {winner}. Payment record created.")
    else:
        print("Closed. No bids placed.")


def all_users(esql):
    esql.execute_query("SELECT login, role, phone_num, address FROM users ORDER BY role, login;")


def change_role(esql, target, new_role):
    if new_role != 'Buyer':
        bids = esql.execute_query("SELECT COUNT(*) FROM bid WHERE buyer_login=%s;", (target,))
        if bids[0][0] > 0:
            print(f"Cannot change role: {target} has existing bids.")
            return
        pays = esql.execute_query("SELECT COUNT(*) FROM payment WHERE buyer_login=%s;", (target,))
        if pays[0][0] > 0:
            print(f"Cannot change role: {target} has existing payments.")
            return
    esql.execute_update("UPDATE users SET role=%s WHERE login=%s;", (new_role, target))
    print("Role updated.")


def all_auctions(esql):
    esql.execute_query(
        """SELECT a.auction_id, i.item_name, a.seller_login,
                  a.current_highest_bid, a.auction_status, COALESCE(a.winner_login,'-') AS winner
           FROM auction a JOIN item i ON a.item_id = i.item_id ORDER BY a.auction_id;"""
    )


def all_payments(esql):
    esql.execute_query(
        "SELECT payment_id, auction_id, buyer_login, amount, payment_status FROM payment ORDER BY payment_id;"
    )


def update_payment(esql, payment_id, status):
    esql.execute_update("UPDATE payment SET payment_status=%s WHERE payment_id=%s;", (status, payment_id))
    print("Payment updated.")
    if status == 'Completed':
        rows = esql.execute_query(
            "SELECT auction_id, buyer_login FROM payment WHERE payment_id=%s;", (payment_id,)
        )
        auction_id, buyer_login = rows[0]
        existing = esql.execute_query("SELECT 1 FROM shipment WHERE auction_id=%s;", (auction_id,))
        if not existing:
            address = esql.execute_query("SELECT address FROM users WHERE login=%s;", (buyer_login,))[0][0]
            sid = esql.execute_query("SELECT COALESCE(MAX(shipment_id),0)+1 FROM shipment;")[0][0]
            esql.execute_update(
                "INSERT INTO shipment (shipment_id, auction_id, address, shipment_status) VALUES (%s,%s,%s,'Pending');",
                (sid, auction_id, address)
            )
            print(f"Shipment created for auction #{auction_id}.")


def all_shipments(esql):
    esql.execute_query(
        """SELECT s.shipment_id, s.auction_id, s.address, s.shipment_status,
                  COALESCE(s.tracking_number,'N/A') AS tracking
           FROM shipment s ORDER BY s.shipment_id;"""
    )


def update_shipment(esql, shipment_id, status, tracking=None):
    if tracking:
        esql.execute_update(
            "UPDATE shipment SET shipment_status=%s, tracking_number=%s WHERE shipment_id=%s;",
            (status, tracking, shipment_id)
        )
    else:
        esql.execute_update(
            "UPDATE shipment SET shipment_status=%s WHERE shipment_id=%s;",
            (status, shipment_id)
        )
    print("Shipment updated.")