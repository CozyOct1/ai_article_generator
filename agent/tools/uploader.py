import time
import json
import uuid
import requests
import traceback


def zhihu_uploader(
    cookies: str, title: str, content: str, column_id: str = None
) -> bool:
    """
    上传文章到知乎或知乎专栏

    :param str cookies: cookies字符串
    :param str title: 文章标题
    :param str content: 文章内容（支持Markdown格式）
    :param str column_id: 专栏ID（可选），如果提供则发布到专栏，否则发布为个人文章
    :return bool: 是否上传成功
    """
    try:
        # 解析cookies字符串为字典
        cookie_dict = {}
        for item in cookies.split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                cookie_dict[key] = value

        # 设置请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/json",
            "Referer": "https://zhuanlan.zhihu.com/write",
            "Origin": "https://zhuanlan.zhihu.com",
            "X-Requested-With": "XMLHttpRequest",
        }

        # 创建session
        session = requests.Session()
        session.headers.update(headers)

        # 设置cookies
        for key, value in cookie_dict.items():
            session.cookies.set(key, value, domain=".zhihu.com")

        # 获取xsrf token
        xsrf_token = cookie_dict.get("_xsrf", "")
        if not xsrf_token:
            print("未找到_xsrf token")
            return False

        # 验证登录状态
        me_url = "https://www.zhihu.com/api/v4/me"
        me_response = session.get(me_url)
        if me_response.status_code != 200:
            print(f"登录验证失败，状态码: {me_response.status_code}")
            return False

        user_info = me_response.json()
        print(f"登录成功，用户: {user_info.get('name', 'Unknown')}")

        # 创建文章草稿
        draft_url = "https://zhuanlan.zhihu.com/api/articles/drafts"
        draft_data = {
            "title": title,
            "content": content,
            "delta_time": int(time.time()),
        }

        # 添加xsrf token到请求头
        session.headers.update({"X-Xsrftoken": xsrf_token})

        # 创建草稿
        draft_response = session.post(draft_url, json=draft_data)
        if draft_response.status_code != 200:
            print(f"创建草稿失败，状态码: {draft_response.status_code}")
            print(f"响应内容: {draft_response.text}")
            return False
        draft_info = draft_response.json()
        draft_id = draft_info.get("id")
        if not draft_id:
            print("未获取到草稿ID")
            return False
        print(f"草稿创建成功，ID: {draft_id}")

        # 发布文章
        publish_url = f"https://zhuanlan.zhihu.com/api/articles/{draft_id}/publish"
        publish_data = {"commentPermission": "anyone", "disclaimer_status": "close"}

        # 如果提供了专栏ID，则发布到专栏
        if column_id:
            if column_id.startswith("http"):
                column_slug = column_id.split("/")[-1]
            elif column_id.startswith("c_"):
                column_slug = column_id
            else:
                column_slug = column_id
            publish_data["column"] = {"slug": column_slug}
        else:
            publish_data["column"] = None

        # 发布文章
        publish_response = session.put(publish_url, json=publish_data)
        if publish_response.status_code != 200:
            print(f"发布文章失败，状态码: {publish_response.status_code}")
            print(f"响应内容: {publish_response.text}")
            return False
        publish_info = publish_response.json()
        article_url = publish_info.get("url", "")
        print(f"文章发布成功！")
        if article_url:
            print(f"文章链接: {article_url}")
        return True
    except Exception as e:
        print(f"[zhihu_uploader] <error>\n{traceback.format_exc()}")
        return False


def juejin_uploader(
    cookies: str, title: str, content: str, column_id: str = None
) -> bool:
    """
    上传文章到掘金或掘金专栏

    :param str cookies: cookies字符串
    :param str title: 文章标题
    :param str content: 文章内容（支持Markdown格式）
    :param str column_id: 专栏ID（可选），如果提供则发布到专栏，否则发布为个人文章
    :return bool: 是否上传成功
    """
    try:
        # 请求头和URL参数设置
        headers = {"content-type": "application/json", "cookie": cookies}
        url_params = {"aid": 2608, "uuid": str(uuid.uuid4())}

        # 创建文章草稿
        draft_url = "https://api.juejin.cn/content_api/v1/article_draft/create"
        draft_data = {
            "category_id": "6809637773935378440",  # AI分类ID
            "tag_ids": ["6809640375880253447"],  # Github标签
            "title": title,
            "brief_content": title,
            "edit_type": 10,
            "mark_content": content,
        }
        draft_response = requests.post(
            draft_url, headers=headers, params=url_params, data=json.dumps(draft_data)
        )
        draft_result = draft_response.json()
        if draft_result.get("err_no") != 0:
            print(f"草稿创建失败: {draft_result.get('err_msg')}")
            return False
        draft_id = draft_result["data"]["id"]
        print(f"草稿创建成功，草稿ID: {draft_id}")

        # 发布文章
        publish_url = "https://api.juejin.cn/content_api/v1/article/publish"
        column_ids = [column_id] if column_id else []
        publish_data = {
            "draft_id": draft_id,
            "sync_to_org": False,
            "column_ids": column_ids,
            "encrypted_word_count": len(content.encode("utf-8")),
            "origin_word_count": len(content),
        }
        publish_response = requests.post(
            publish_url,
            headers=headers,
            params=url_params,
            data=json.dumps(publish_data),
        )
        publish_result = publish_response.json()

        # 检查发布是否成功
        if publish_result.get("err_no") != 0:
            print(f"文章发布失败: {publish_result.get('err_msg')}")
            return False
        article_id = publish_result["data"]["article_id"]
        print(f"文章发布成功，文章ID: {article_id}")
        return True
    except Exception as e:
        print(f"[juejin_uploader] <error>\n{traceback.format_exc()}")
        return False
