import argparse
import requests
import sys

API = "http://127.0.0.1:5000"


def list_items():
    r = requests.get(f"{API}/inventory")
    r.raise_for_status()
    for i in r.json():
        print(f"{i['id']}: {i['name']} ({i.get('stock',0)} in stock) - ${i.get('price')}")


def get_item(item_id):
    r = requests.get(f"{API}/inventory/{item_id}")
    if r.status_code == 404:
        print("Not found")
        return
    r.raise_for_status()
    print(r.json())


def add_item(args):
    payload = {
        "name": args.name,
        "brand": args.brand,
        "price": args.price,
        "stock": args.stock,
        "barcode": args.barcode,
    }
    r = requests.post(f"{API}/inventory", json=payload)
    r.raise_for_status()
    print("Added:", r.json())


def update_item(args):
    payload = {}
    if args.price is not None:
        payload["price"] = args.price
    if args.stock is not None:
        payload["stock"] = args.stock
    r = requests.patch(f"{API}/inventory/{args.id}", json=payload)
    if r.status_code == 404:
        print("Not found")
        return
    r.raise_for_status()
    print("Updated:", r.json())


def delete_item_cli(item_id):
    r = requests.delete(f"{API}/inventory/{item_id}")
    if r.status_code == 404:
        print("Not found")
        return
    r.raise_for_status()
    print(r.json())


def fetch_and_print(q):
    r = requests.get(f"{API}/fetch", params={"q": q})
    if r.status_code == 404:
        print("External product not found")
        return
    r.raise_for_status()
    print(r.json())


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list")

    g = sub.add_parser("get")
    g.add_argument("id", type=int)

    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("--brand", default="")
    a.add_argument("--price", type=float, default=0.0)
    a.add_argument("--stock", type=int, default=0)
    a.add_argument("--barcode", default="")

    u = sub.add_parser("update")
    u.add_argument("id", type=int)
    u.add_argument("--price", type=float)
    u.add_argument("--stock", type=int)

    d = sub.add_parser("delete")
    d.add_argument("id", type=int)

    f = sub.add_parser("fetch")
    f.add_argument("q")

    args = p.parse_args()
    if args.cmd == "list":
        list_items()
    elif args.cmd == "get":
        get_item(args.id)
    elif args.cmd == "add":
        add_item(args)
    elif args.cmd == "update":
        update_item(args)
    elif args.cmd == "delete":
        delete_item_cli(args.id)
    elif args.cmd == "fetch":
        fetch_and_print(args.q)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
