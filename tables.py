from urllib import request
from contextlib import closing
import json
import os

item_table = {}  # 物品表, key为物品全名, value为itemId
stage_table = {}  # 关卡表, key为关卡代码, value为stageId
find_item_name = {}  # 物品表的反函数
find_stage_code = {}  # 关卡表的反函数
formula_table = {}  # 合成公式表 key为itemId, value为另一个字典, 其key为合成素材的itemId, value为需要数量
rarity_table = {}  # 物品稀有度表, key为物品全名, value为物品的稀有度


def check_table_updates() -> bool:
    '''Check whether the table needs to be updated.

    Returns:
        * A `boolean` indicating whether the tables need updating
        * A `string` indicating the online version.


    Raises:
        SSLError:HTTPSConnectionPool: Max retries exceeded with url
    '''
    if not os.path.exists("gamedata/data_version.txt"):
        os.mkdir("gamedata/")
        open("gamedata/data_version.txt", "ab").close()

    with (open('gamedata/data_version.txt', 'rb') as f,
          closing(request.urlopen(
              'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/data_version.txt'
          )) as o):
        online_version = o.read()
        local_version = f.read()
        result = online_version != local_version
    return result, online_version


def load_tables() -> None:
    '''Load the tables.

    Tables include the following:
        * The `item_table` whose `key` is the `name` of the item and the `value` is the `id` of the item.
        * The `find_item_name` which is the `transposed` version of the `item_table`.
        * The 'rarity_table' whose 'key` is the `name` of the item and the `value` is the `rarity` of the item.
        * The `stage_table` whose `key` is the `code` of the stage and the `value` is the `id` of the stage.
        * The `find_stage_code` which is the `transposed` version of the `stage_table`.
        * The `formula_table` whose `key` is the `id` of the item to be synthesized into ,and the `value` is another `dict`
        whose `key` is the `id` of the item to be synthesized and the `value` is the `number` of the corresponding item.


    Raises:
        SSLError:HTTPSConnectionPool: Max retries exceeded with url.
    '''
    global item_table, stage_table, find_item_name, find_stage_code, formula_table, rarity_table

    check, online_version = check_table_updates()
    if check:
        with open('gamedata/data_version.txt', 'w') as f:
            f.write(online_version)

        with (open('gamedata/item_table.json', 'wb') as f,
              closing(request.urlopen(
                      'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json'
                      )) as o):
            online_version = o.read()
            f.write(online_version)

        with (open('gamedata/stage_table.json', 'wb') as f,
              closing(request.urlopen(
                      'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json'
                      )) as o):
            online_version = o.read()
            f.write(online_version)

        with (open('gamedata/building_data.json', 'wb') as f,
              closing(request.urlopen(
                      'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json'
                      )) as o):
            online_version = o.read()
            f.write(online_version)

    with open('gamedata/item_table.json', 'rb') as f:
        temp = json.load(f)['items']
        for value in temp.values():
            item_table[value["name"]] = value["itemId"]
            find_item_name[value['itemId']] = value['name']
            rarity_table[value['name']] = value['rarity']

    with open('gamedata/stage_table.json', 'rb') as f:
        temp = json.load(f)['stages']
        for value in temp.values():
            stage_table[value['code']] = value['stageId']
            find_stage_code[value['stageId']] = value['code']

    with open('gamedata/building_data.json', 'rb') as f:
        temp = json.load(f)['workshopFormulas']
        for value in temp.values():
            tempdir = {}
            for cost in value["costs"]:
                tempdir[cost['id']] = cost['count']
            formula_table[value['itemId']] = tempdir


def __main() -> int:
    load_tables()

    for key, value in formula_table.items():
        print(find_item_name[key], "的合成路径是:")
        for k, v in value.items():
            print(" ", find_item_name[k], ':', v)

    input("press enter to exit...")
    return 0


if __name__ == "__main__":
    __main()
