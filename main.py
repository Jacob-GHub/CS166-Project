import sys
import psycopg2
import queries


class EmbeddedSQL:
    def __init__(self, dbname, dbport, user, passwd=""):
        print("Connecting to database...")
        try:
            self._connection = psycopg2.connect(
                database=dbname, user=user, password=passwd,
                host="localhost", port=dbport
            )
            print(f"Connected to {dbname}\n")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(-1)

    def execute_update(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        self._connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        cursor = self._connection.cursor()
        cursor.execute(query, params)
        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        print("\t".join(col_names))
        for row in rows:
            print("\t".join(str(v) for v in row))
        print(f"{len(rows)} row(s)\n")
        return rows

    def cleanup(self):
        if self._connection:
            self._connection.close()


def read_choice():
    while True:
        try:
            return int(input("Choice: "))
        except ValueError:
            print("Enter a number.")


def buyer_menu(esql, login):
    while True:
        print("\nBUYER MENU")
        print("1. Browse active auctions")
        print("2. Search auctions")
        print("3. View auction detail + bid history")
        print("4. Place a bid")
        print("5. My bids")
        print("6. My won auctions")
        print("7. View/edit profile")
        print("9. Logout")
        c = read_choice()

        if c == 1:
            queries.browse_active_auctions(esql)
        elif c == 2:
            queries.search_auctions(esql, input("Keyword: ").strip())
        elif c == 3:
            queries.view_auction_detail(esql, input("Auction ID: ").strip())
        elif c == 4:
            queries.place_bid(esql, input("Auction ID: ").strip(), login, input("Bid amount: ").strip())
        elif c == 5:
            queries.my_bids(esql, login)
        elif c == 6:
            queries.won_auctions(esql, login)
        elif c == 7:
            profile_menu(esql, login)
        elif c == 9:
            break


def seller_menu(esql, login):
    while True:
        print("\nSELLER MENU")
        print("1. Create new listing")
        print("2. View my listings")
        print("3. Close an auction")
        print("4. Browse active auctions")
        print("5. View/edit profile")
        print("9. Logout")
        c = read_choice()

        if c == 1:
            queries.create_listing(
                esql, login,
                input("Item name: ").strip(),
                input("Category: ").strip(),
                input("Starting price: ").strip(),
                input("Condition: ").strip(),
                input("Description: ").strip()
            )
        elif c == 2:
            queries.my_listings(esql, login)
        elif c == 3:
            queries.close_auction(esql, input("Auction ID to close: ").strip(), login)
        elif c == 4:
            queries.browse_active_auctions(esql)
        elif c == 5:
            profile_menu(esql, login)
        elif c == 9:
            break


def admin_menu(esql, login):
    while True:
        print("\nADMIN MENU")
        print("1. All users")
        print("2. Change user role")
        print("3. All auctions")
        print("4. All payments")
        print("5. Update payment status")
        print("6. All shipments")
        print("7. Update shipment status")
        print("9. Logout")
        c = read_choice()

        if c == 1:
            queries.all_users(esql)
        elif c == 2:
            target= input("Username: ").strip()
            new_role = input("New role (Buyer/Seller/Admin): ").strip()
            if new_role not in ('Buyer', 'Seller', 'Admin'):
                print("Invalid role.")
            else:
                queries.change_role(esql, target, new_role)
        elif c == 3:
            queries.all_auctions(esql)
        elif c == 4:
            queries.all_payments(esql)
        elif c == 5:
            pid = input("Payment ID: ").strip()
            status = input("New status (Pending/Completed/Failed): ").strip()
            if status not in ('Pending', 'Completed', 'Failed'):
                print("Invalid status.")
            else:
                queries.update_payment(esql, pid, status)
        elif c == 6:
            queries.all_shipments(esql)
        elif c == 7:
            sid = input("Shipment ID: ").strip()
            status = input("New status (Pending/Shipped/Delivered): ").strip()
            tracking = input("Tracking number (Enter to skip): ").strip()
            if status not in ('Pending', 'Shipped', 'Delivered'):
                print("Invalid status.")
            else:
                queries.update_shipment(esql, sid, status, tracking or None)
        elif c == 9:
            break


def profile_menu(esql, login):
    rows = queries.get_profile(esql, login)
    if not rows:
        return
    _, _, phone, address, fav = rows[0]
    print("Press Enter to keep current value.")
    new_phone = input(f"Phone [{phone}]: ").strip()
    new_address = input(f"Address [{address}]: ").strip()
    new_fav = input(f"Favorite category [{fav}]: ").strip()
    queries.update_profile(
        esql, login,
        new_phone   or phone,
        new_address or address,
        new_fav     or fav
    )
    print("Profile updated.")


def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <dbname> <port> <user>")
        return

    esql = EmbeddedSQL(sys.argv[1], sys.argv[2], sys.argv[3])

    try:
        while True:
            print("\nMAIN MENU")
            print("1. Login")
            print("2. Register")
            print("9. Exit")
            c = read_choice()

            if c == 1:
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                session  = queries.login(esql, username, password)
                if session:
                    login_val, role = session
                    print(f"Welcome {login_val} ({role})")
                    if role == 'Buyer':
                        buyer_menu(esql, login_val)
                    elif role == 'Seller':
                        seller_menu(esql, login_val)
                    elif role == 'Admin':
                        admin_menu(esql, login_val)
                else:
                    print("Invalid credentials.")

            elif c == 2:
                login_val = input("Username: ").strip()
                password  = input("Password: ").strip()
                phone = input("Phone: ").strip()
                address = input("Address: ").strip()
                try:
                    queries.register(esql, login_val, password, phone, address)
                    print(f"Account created. Logged in as {login_val} (Buyer)")
                    buyer_menu(esql, login_val)
                except Exception as e:
                    print(f"Error: {e}")

            elif c == 9:
                break

    finally:
        esql.cleanup()
        print("Bye!")


if __name__ == "__main__":
    main()