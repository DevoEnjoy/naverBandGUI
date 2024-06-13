# -*- coding: utf-8 -*-
# v240322
import os
import sys
# import time
from anyio import current_time
import yaml
import naverBandAPI.client as client
from __init__ import config_file_path, root_folder_path
sys.path.append(root_folder_path)
from library.basic import join_folder_path, clear, create_folder, path_exist, strip_quotes, write_to_file, path_exist
from library.lib_time import epoch_to_time
from library.lib_datetime import DateTimer
from naverBandAPI.client import BandOpenApi

# config_file_path = os.path.join(root_folder_path,'config.yaml')
test_band_key = None
test_post_key = None

with open(config_file_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    test_band_key = config['testBandKey']
    test_post_key = config['testPostKey']

timer = DateTimer()
today_yymmdd = int(timer.get_current_datetime('yyyyMMdd'))
# today_yyyymmdd = 20240101

def test(api:BandOpenApi, target_folder_path=root_folder_path):
    bands = api.get_bands()['bands']
    print(bands)
    """  
    {
        "result_code": 1,
        "result_data": {
            "bands" : [{
                "name" : "Golf Club",
                "band_key" : "AzIEz54gxWeSAB_nwygZ84",
                "cover" : "http://img.band.us/111.jpg",
                "member_count" : 100
                }
            ,{
                "name" : "Baseball team",
                "band_key" : "AzIEz54gxWeSAB_nwygZ95",
                "cover" : "http://img.band.us/222.jpg",
                "member_count" : 32
            }]
        }
}
    """
    # input("Enter to continue.")
    i = 1
    for band in bands:
        band_name = band['name']
        print('# 3. 글 목록 조회')
        band_key = band['band_key']
        posts = api.get_posts(band_key=band_key, locale='ko_KR')
        """  
        {
            "result_code": 1,
            "result_data": {
                "paging": {
                    "previous_params": null,
                    "next_params": {
                    "after": "AABsFASmeIbSAib8KSzihCBC",
                    "limit": "20",
                    "band_key": "bandkeyxxxx"
                    "access_token": "accsstokenxxxx"
                }
            },
            "items": [{
                "content": "Cotents <band:refer user_no=\"\">Jordan</band:refer>   <band:hashtag>#food</band:hashtag>",
                "post_key": "AABhEEQG08e1Fc227z2fRCwv",
                "created_at": 1444288237000,
                "photos": [{
                    "width": 640,
                    "height": 480,
                    "photo_key": "AAACTLxEYqMx09qji9nzAv1V",
                    "photo_album_key": null,
                    "author": {
                        "name": "Sujan",
                        "description": "This is desc.",
                        "profile_image_url": "http://band.phinf.campmobile.net/20130719_224/yyyyyy/yyyyy.jpg"
                    },
                    "url": "http://beta.coresos.phinf.naver.net/a/2g8728_c/28aUd015g6pesvlf89uq_ggxdbs.jpg",
                    "comment_count": 1,
                    "emotion_count": 1,
                    "created_at": 1444295780000,
                    "is_video_thumbnail": true
                }, {
                    "width": 1280,
                    "height": 720,
                    "photo_key": "AADtBkdo52blVIcH-4y_AotK",
                    "photo_album_key": null,
                    "author": {
                        "name": "Eddy",
                        "description": "This contents is so...",
                        "profile_image_url": "http://band.phinf.campmobile.net/20130719_224/xxxxxx/xxxxxx.jpg"
                    },
                    "url": "http://beta.coresos.phinf.naver.net/a/2g8701_9/ac2Ud01515ftew9215e27_ggxdbs.jpg",
                    "comment_count": 1,
                    "emotion_count": 1,
                    "created_at": 1444288237000,
                    "is_video_thumbnail": false
                }],
                "comment_count": 7,
                "author": {
                    "name": "Charley Lee",
                    "description": "This is a description",
                    "profile_image_url": "http://band.phinf.campmobile.net/20130719_224/zzzzzz/zzzzz.jpg"
                }
            }...]
            }
        }
        """
        # print(posts)
        # write_to_json(posts, rename(config_file_path, new_name=f"{band['name']}", new_extension='json'))
        j = 1

        for post in posts['items']:
            clear()
            print(f"{i}/{len(bands)}\n\t{band_name}")
            print(f"{j}/{len(posts['items'])}")
            j += 1
            post_key = post['post_key']

            # 20240101
            created_date = epoch_to_time(post['created_at'], 'yyyyMMdd_HHmm')
            yyyymmdd = int(created_date.split('_')[0])
            if yyyymmdd < today_yyyymmdd:
                continue

            last_folder_path = join_folder_path(target_folder_path, str(yyyymmdd)[2:])
            if not path_exist(last_folder_path): create_folder(last_folder_path)
            
            txt_file_path = join_folder_path(last_folder_path, f"{created_date}.txt")

            if path_exist(txt_file_path):
                print("the post file is already exist.")
                continue
            # input(api.get_post(band_key=band_key, post_key=post_key)['post']['content'])
            content = api.get_post(band_key=band_key, post_key=post_key)['post']['content']
            if str(content).__contains__('A new member was invited by'):
                continue
            write_to_file(txt_file_path, content)
        i += 1

# def main():
#     test_band_key = None
#     test_post_key = None
#     with open(config_file_path) as f:
#         config = yaml.load(f, Loader=yaml.FullLoader)
#         test_band_key = config['testBandKey']
#         test_post_key = config['testPostKey']
#     api = client.BandOpenApi()

#     print('# 1. 사용자 정보 조회')
#     print(api.get_profile())
#     time.sleep(1)

#     print('# 2. 밴드 목록 조회')
#     bands = api.get_bands()
#     print(bands)
#     # time.sleep(1)
#     # input()

#     # print('# 3. 글 목록 조회')
#     # posts = api.get_posts(band_key=test_band_key, locale='ko_KR')
#     # print(posts)
#     # # time.sleep(1)
#     # input()

#     # print('# 4. 글 상세 조회')
#     # band_key = posts['items'][0]['band_key']
#     # post_key = posts['items'][0]['post_key']
#     # post = api.get_post(band_key=band_key, post_key=post_key)
#     # print(post)
#     # time.sleep(1)

#     print('# 5. 글쓰기')
#     post = api.create_post(band_key=test_band_key, content='test')
#     print(post)
#     # time.sleep(1)
#     # input()
#     post_key = post['post_key']

#     test_post_key = post_key
    
#     print('# 8. 댓글 작성')
#     create_post_comment_result = api.create_post_comments(band_key=test_band_key, post_key=test_post_key, body='body')
#     print('create_post_comment_result', create_post_comment_result)
#     # time.sleep(1)
#     # input()
    
#     print('# 7. 댓글 목록 조회')
#     comments = api.get_post_comments(band_key=test_band_key, post_key=test_post_key)
#     print(comments)
#     time.sleep(1)
#     # input()

#     print('# 9. 댓글 삭제')
#     items = comments['items']
#     if items:
#         test_comment_key = items[0]['comment_key']
#         delete_comment_result = api.delete_post_comments(band_key=test_band_key, post_key=test_post_key,
#                                                         comment_key=test_comment_key)
#         print(delete_comment_result)
#         # time.sleep(1)
#         # input()

#     print('# 10. 앨범 목록 조회')
#     albums = api.get_albums(band_key=test_band_key)
#     print(albums)
#     time.sleep(1)

#     print('# 11. 사진 목록 조회')
#     items = albums['items']
#     if items:
#         photo_album_key = [0]['photo_album_key']
#         photos = api.get_album_photos(band_key=test_band_key, photo_album_key=photo_album_key)
#         print(photos)

#     print('# 6. 글 삭제')
    
#     post = api.delete_post(band_key=test_band_key, post_key=post_key)
#     print(post)
#     time.sleep(1)

if __name__ == "__main__":
    # main()
    api = client.BandOpenApi()
    target_folder_path = strip_quotes(input("Enter target folder path : "))
    test(api, target_folder_path=target_folder_path)