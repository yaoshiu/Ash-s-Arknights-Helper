from contextlib import closing
import requests


def report(stage_id: str, drops: list[dict[str:str or int]], source: str = 'CLIENT_SOURCE', version: str = 'CLIENT_VERSION', server: str = 'CN') -> None:
    '''Report the drops to the Penguin Stats

    Args:
    * `stage_id`: The stage id of this drop
    * `drops`: An array of drop. PLease find it's model below。
        Model:
            {'dropType': string, 'itemId': string, quantity: int}
        Properties:
            `dropType` should be one of the four following values:`NORMAL_DROP` `SPECIAL_DROP` `EXTRA_DROP` `FURNITURE`

        Example:

            [
                {
                "dropType": "SPECIAL_DROP",
                "itemId": "randomMaterial_3",
                "quantity": 1
                },
                {
                "dropType": "EXTRA_DROP",
                "itemId": "30061",
                "quantity": 2,
                },
                {
                "dropType": "NORMAL_DROP",
                "itemId": "30013",
                "quantity": 1,
                },
                {
                "dropType": "FURNITURE",
                "itemId": "furni",
                "quantity": 1,
                },
            ]

    * `source`: Optional; The source is used to mark the client sending this request.
    Equivalent to 'User-Agent' presented in the header
    * `version`: Optional; The version of the source.
    * `server`: Optional; Indecate the server of this drop sample.
    Support 4 servers now: 'CN', 'US', 'JP', and 'KR'.
    '''
    url = "https://penguin-stats.io/PenguinStats/api/v2/report"
    post_data = {
        "drops": drops,
        "stageId": stage_id,
        "server": server,
        "source": source,
        "version": version,
    }
    with closing(requests.post(url, json=post_data)) as response:
        if response.status_code // 100 != 2:
            print(response.json())


def login(user_id: int) -> None:
    '''Login to the Penguin Statistics

    Args:
        `user_id`: The ID of the user.
    '''
    url = "https://penguin-stats.io/PenguinStats/api/v2/users"
    with closing(requests.post(url, json=user_id)) as response:
        if response.status_code // 100 != 2:
            print(response.json())


def __main():
    login(79381157)

    drops = [
        {
            "dropType": "SPECIAL_DROP",
            "itemId": "randomMaterial_3",
            "quantity": 1,
        },
        {
            "dropType": "EXTRA_DROP",
            "itemId": "30061",
            "quantity": 2,
        },
        {
            "dropType": "NORMAL_DROP",
            "itemId": "30013",
            "quantity": 1,
        },
        {
            "dropType": "FURNITURE",
            "itemId": "furni",
            "quantity": 1,
        },
    ]
    report("main_04-06", drops, "CLIENT_SOURCE", "CLIENT_VERSION")


if __name__ == "__main__":
    __main()
