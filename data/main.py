import json
import yaml


def extract_taxonomy(path):
    # 提取路径中 ${BOOKMARKS_BAR} 后面的路径，并返回切割后的路径部分
    return path.split('${BOOKMARKS_BAR}/')[-1]


def convert_json_to_yaml(json_data):
    dict_data = []
    taxonomies = {}

    for bookmark in json_data["bookmarks"]:
        title = bookmark["title"]
        url = bookmark["url"]

        path_segments = extract_taxonomy(bookmark["path"]).split('/')
        taxonomy = path_segments[0] if path_segments else "未分类"
        term = path_segments[1] if len(path_segments) > 1 else None

        hostname = url.split('/')[2]
        favicon_url_template = "https://api.iowen.cn/favicon/{hostname}.png" # 定义统一的链接图标获取方式
        favicon_url = favicon_url_template.format(hostname=hostname)

        if taxonomy not in taxonomies:
            taxonomies[taxonomy] = {
                "taxonomy": taxonomy,
                "icon": "fas fa-shield-alt fa-lg icon-fw icon-lg mr-2" # 设置统一的分类图标
            }

        link_dict = {"title": title, "logo": favicon_url, "url": url, "description": ""}
        if term:
            link_container = {"term": term, "links": []}

            if "list" not in taxonomies[taxonomy]:
                taxonomies[taxonomy]["list"] = []
                taxonomies[taxonomy]["list"].append(link_container)

            termlist = taxonomies[taxonomy]['list']

            us_intel_exists = False
            us_intel_index = None
            for i, sublist in enumerate(termlist):
                if sublist['term'] == term:
                    us_intel_exists = True
                    us_intel_index = i
                    break

            if us_intel_exists:
                termlist[us_intel_index]['links'].append(link_dict)
            else:
                new_us_intel = {'term': term, 'links': [link_dict]}
                termlist.append(new_us_intel)
        else:
            if "links" not in taxonomies[taxonomy]:
                taxonomies[taxonomy]["links"] = []
            taxonomies[taxonomy]["links"].append(link_dict)

    # 将taxonomies转换为列表
    for taxonomy_info in taxonomies.values():
        dict_data.append(taxonomy_info)

    return dict_data


# 只支持提取到Chrome书签二级文件夹，因Chrome书签限制，未实现：1.分类图标，2.链接描述

# 从Json Bookmarks导出的文件bookmarks.v2.json提取json数据
json_file_path = 'bookmarks.v2.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)


# 将字典转换为YAML格式
yaml_data = convert_json_to_yaml(json_data)
yaml_output = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)


# 将YAML数据写入到文件webstack.yml
with open('webstack.yml', 'w', encoding='utf-8') as file:
    file.write(yaml_output)

print('YAML data has been written to webstack.yml')
