"""
把 json 转换成 pydantic 的 BaseModel

例如:
{
    "hello": "world"
}

转换成:

from pydantic import BaseModel, Field

class D(BaseModel):
    hello: str = Field(..., title='???')

"""
import json
import os
import sys

import click


def gen_field(k, v) -> str:
    if v is None:
        return f'{k}: Optional[str] = fields.{k}_field'
    else:
        return f'{k}: Optional[{v.__class__.__name__}] = fields.{k}_field'


def gen_fields(d: dict) -> str:
    fields = []
    for k, v in d.items():
        fields.append(gen_field(k, v))

    return '\n'.join(map(lambda x: f'    {x}', fields))


def file_to_content_item_name(f_name: str) -> str:
    """
    convert 'hell_world_resp' to 'HelloWorldModel'

    :param f_name:
    :return:
    """
    parts = f_name.split('_')[:-1]

    return ''.join(map(lambda x: x.capitalize(), parts)) + 'Model'


def file_to_class_name(f_name: str) -> str:
    """
    convert 'hell_world_model' to 'HelloWorldModel'

    :param f_name:
    :return:
    """
    parts = f_name.split('_')

    return ''.join(map(lambda x: x.capitalize(), parts))


def convert_json_to_py(f):
    (b, ext) = os.path.splitext(os.path.basename(f))
    if b in {'item_detail_resp'}:  # no need to convert
        print(f'ignore file: {f}')
        return

    out_py = os.path.join(os.path.dirname(f), f'{b.replace("resp", "model")}.py')
    print(f'process file: {f}')
    with open(f) as fp:
        j = json.load(fp)
        data = j['content'][0]

        assert isinstance(data, dict)
        fields_code = gen_fields(data)

        t = """# 这个文件是由 json_code_gen_model.py 自动生成的 请不要修改

from typing import Optional

from pydantic import BaseModel

from ..api import fields


class cls_name(BaseModel):
""".replace('cls_name', file_to_content_item_name(b))

        code = t + fields_code

        with open(out_py, 'w') as out_fp:
            out_fp.write(code)


@click.command('json_code_gen_model')
@click.argument('d')
def main(d):
    """
    把 json 转换成 pydantic 的 BaseModel

    d 要转换的目录

    会把所有的 *.json 转换成 *.py 文件
    """
    if not os.path.isdir(d):
        print(f'{d} is not directory')
        sys.exit(1)

    for f in os.listdir(d):
        if not f.endswith('json'):
            continue

        convert_json_to_py(os.path.join(d, f))


if __name__ == '__main__':
    main()
