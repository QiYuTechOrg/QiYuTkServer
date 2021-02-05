import click


@click.command('json_code_gen')
@click.argument('d')
def main(d):
    """
    把 json 转换成 python 的 dataclass

    d 要转换的目录

    会把所有的 *.json 转换成 *.py 文件
    """
    print('nothing, use django management command gen the code')


if __name__ == '__main__':
    main()
