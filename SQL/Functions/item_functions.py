import SQL.Commands.create_commands as create_commands
import SQL.Commands.select_commands as select_commands
import SQL.Commands.delete_commands as delete_commands
import SQL.Commands.drop_commands as drop_commands
import SQL.Commands.insert_commands as insert_commands
import SQL.Commands.update_commands as update_commands


def get_item_id_from_item_name(cur, item_name):
    cur.execute(select_commands.SELECT_ITEM_ID_FROM_ITEM_NAME, [item_name])
    r = cur.fetchone()
    return r[0]

def insert_items( cur, item_dict ):
    for item in item_dict.items():
        cur.execute(insert_commands.INSERT_ITEM,item)
    cur.connection.commit()