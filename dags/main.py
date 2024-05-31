from skt.ye import slack_send

def main(**kwargs):
    http_auth_id = kwargs.get('http_auth_id')
    http_auth_password = kwargs.get('http_auth_password')
    input_path = kwargs.get('input_path')
    vpce_host = kwargs.get('vpce')
    env = kwargs.get('env')

    print(f"http_auth_id Name: {http_auth_id}")
    print(f"http_auth_password: {http_auth_password}")
    print(f"input_path: {input_path}")
    print(f"vpce_host: {vpce_host}")
    print(f"env: {env}")

    template = f"""
        http_auth_id Name: {http_auth_id}
        http_auth_password: {http_auth_password}
        input_path: {input_path}
        vpce_host: {vpce_host}
        env: {env}
    """

    slack_send(
        text=template,
        username="SKT",
        channel="#prec_onemodel_alarming_stg",
        icon_emoji=":large_blue_circle:",
        blocks=None,
        dataframe=False,
        adot=True,
    )

if __name__ == "__main__":
    import sys
    main(**dict(arg.split('=') for arg in sys.argv[1:]))

