from dbUtil import create_owner_tokens_table, insert_owner_token, owner_token_exists


if owner_token_exists("AbC123"):
    print("SI")
else:
    print("NO")
