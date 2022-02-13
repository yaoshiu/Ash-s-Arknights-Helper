from contextlib import closing
import requests
import tables


def get_plan(owned: dict[str:int] = {}, required: dict[str:int] = {}, extra_outc: bool = False, convertion_dr: float = 0,
             exp_demand: bool or int = True, gold_demand: bool or int = True, exclude: list[str] = [], store: bool = False,
             input_lang: str = 'zh', output_lang: str = 'zh', server: str = 'CN') -> dict[str:int or list[dict[str:str]]]:
    '''Get the plan for a given set of resources

    Args:
        * `owned`: A dict of items owned, where keys are item names.
        i.e. 'D32钢', values are numbers of items owned.
        * `required`: A dict of items required, where keys are item names.
        i.e. 'D32钢', values are numbers of items required.
        * `extra_outc`: Whether extra outcome of convertion is considered.
        * `conversion`:The drop rate of extra outcome.
        * `exp_demand`: Whether Battle Record(作战记录) is considered valuable.
        If True, the requirement of Battle Record is set to `1e9`.
        If input is an integer, the requirement of experiment is set to be equal to the input.
        * `gold_demand`: Whether LMD(龙门币) is considered valuable.
        If True, the requirement of LMD is set to `1e9`.
        If False, the value of LMD is set to 0. 
        If input is an integer, the requirement of LMD is set to be equal to the input.
        * `exclude`: Stages banned during calculation. Example: `['1-7', 'SA-5']
        * `store`: Whether to response green and yellow ticket values in stores.
        * `input_lang`: The language of the input. Available languages: `['zh', 'en', 'ja', 'ko'], and 'id' for item ids.
        * `output_lang`: The language of the output. Available languages: `['zh', 'en', 'ja', 'ko'], and 'id' for item ids.
        * `server`: Using active stages from this server. Available Servers: ['CN', 'US', 'JP', 'KR'].

    Returns:
        A dict mapping the cost, gold cost, exp, planned stages, syntheses and item values.
        example:

        {'cost': 145,
        'gcost': 421,
        'gold': 1744
        'exp': 1133,
        'stages': [
            {'stage': '3-4', 'count': '3', 'items': {'源岩': '0.6', '固源岩': '0.6', '破损装置': '0.2', '装置': '0.2', '全新装置': '0.7', '酯原料': '0.4', '聚酸酯': '0.4'}},
            {'stage': 'S4-1', 'count': '5', 'items': {'代糖': '0.8', '糖': '0.9', '异铁碎片': '0.6', '异铁': '0.7', '异铁组': '1', '异铁块': '0.2'}},
            {'stage': '2-6', 'count': '2', 'items': {'源岩': '0.7', '固源岩': '0.0', '破损装置': '0.3', '酯原料': '0.5', '聚酸酯组': '0.7'}},
        ],
        'syntheses':[
            {'target': '装置', 'count': '1', 'materials': {'破损装置': '0.5'}},
            {'target': '全新装置', 'count': '1', 'materials': {'装置': '0.4'}},
            {'target': '异铁', 'count': '1', 'materials': {'异铁碎片': '0.6'}},
            {'target': '异铁组', 'count': '1', 'materials': {'异铁': '0.9'}},
            {'target': '异铁块', 'count': '1', 'materials': {'异铁组': '1.7', '全新装置': '0.8', '聚酸酯组': '0.8'}},
            {'target': '聚酸酯', 'count': '1', 'materials': {'酯原料': '0.9'}},
            {'target': '聚酸酯组', 'count': '1', 'materials': {'聚酸酯': '0.7'}},
        ]
        'values': [{'level': '5', 'items': [...]}, {'level': '4', 'items': [...]}, {'level': '3', 'items': [...]}, {'level': '2', 'items': [...]}, {'level': '1', 'items': [...]}]}

        Raises:
            SSLError:HTTPSConnectionPool: Max retries exceeded with url
    '''
    url = 'https://planner.penguin-stats.io/plan'
    post_data = {
        'owned': owned,
        'required': required,
        'extra_outc': extra_outc,
        'convertion_dr': convertion_dr,
        'exp_demand': exp_demand,
        'gold_demand': gold_demand,
        'exclude': exclude,
        'store': store,
        'input_lang': input_lang,
        'output_lang': output_lang,
        'server': server,
    }
    with closing(requests.post(url, json=post_data)) as response:
        result = response.json()
    return result


def __main() -> int:
    tables.load_tables()
    plan = get_plan(required={'D32钢': 1, '晶体电子单元': 1, '聚合剂': 1, '双极纳米片': 1})
    print('需要刷的关卡有:')
    for map in plan['stages']:
        print(' ', map['stage'], ':', map['count'])
    plan['syntheses'].sort(key=lambda x, :
                           tables.rarity_table[x['target']])
    print('需要合成的路线为:')
    for map in plan['syntheses']:
        print(' ', map['target'], ':', map['count'])
    return 0


if __name__ == '__main__':
    __main()
