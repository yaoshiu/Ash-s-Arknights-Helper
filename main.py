from urllib import request
import json


item_table = {}  # 物品表, key为物品全名, value为itemId
stage_table = {}  # 关卡表, key为关卡代码, value为stageId
find_item_name = {}  # 物品表的反函数
find_stage_code = {}  # 关卡表的反函数
formula_table = {}  # 合成公式表 key为itemId, value为另一个字典, 其key为合成素材的itemId, value为需要数量


def check_table_updates():
    with open('gamedata/data_version.txt', 'rb+') as f:
        online_version = request.urlopen(
            'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/data_version.txt'
        ).read()
        local_version = f.read()
        if (online_version == local_version):
            return True
        print("检测到最新表格数据:\n", online_version.decode("utf-8"),
              "本地表格数据:", local_version.decode("utf-8"), "\n正在更新数据中...")
        f.write(online_version)

    with open('gamedata/item_table.json', 'wb') as f:
        online_version = request.urlopen(
            'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json'
        ).read()
        f.write(online_version)

    with open('gamedata/stage_table.json', 'wb') as f:
        online_version = request.urlopen(
            'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/stage_table.json'
        ).read()
        f.write(online_version)

    with open('gamedata/building_data.json', 'wb') as f:
        online_version = request.urlopen(
            'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/building_data.json'
        ).read()
        f.write(online_version)

    return False


def load_tables():
    global item_table, stage_table, find_item_name, find_stage_code, formula_table

    with open('gamedata/item_table.json', 'rb') as f:
        temp = json.load(f)['items']
        for value in temp.values():
            item_table[value["name"]] = value["itemId"]
            find_item_name[value['itemId']] = value['name']

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


def main():
    check_table_updates()
    load_tables()

    for key, value in formula_table.items():
        print(find_item_name[key], "的合成路径是:")
        for k, v in value.items():
            print(" ", find_item_name[k], ':', v)

    input("press enter to exit...")
    return 0


if __name__ == "__main__":
    main()
