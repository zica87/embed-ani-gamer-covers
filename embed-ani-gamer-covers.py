import os, sys, argparse
import questionary
import tomli_w
from get_metadata import Episode
from embed_cover import embed

VERSION = "0.1.0"

def file_write_mode(path):
    if "args" in globals() and args.overwrite:
        return 'wb'
    if not os.path.isfile(path):
        return 'xb'
    parent_folder = os.path.dirname(path)
    if not parent_folder:
        parent_folder = os.getcwd()
    print(f"在 {parent_folder} 下，")
    print(f"已經有名為 {os.path.basename(path)} 的檔案，")
    if "args" in globals() and args.no_overwrite:
        print("退出程式")
        sys.exit(0)
    if questionary.confirm("要取代掉嗎？").ask():
        return 'wb'
    else:
        print("退出程式")
        sys.exit(0)

    # print("要取代掉嗎？(Y/N)")
    # for ith in range(1,4):
    #     try:
    #         ans = input()
    #     except KeyboardInterrupt:
    #         print("\n使用者按了 Ctrl + C 中斷程式")
    #         sys.exit(1)
    #     if ans in ('y', 'Y'):
    #         return 'wb'
    #     elif ans in ('n', 'N'):
    #         print("退出程式")
    #         sys.exit(0)
    #     elif i == 3:
    #         print("\n連續錯誤 3 次，退出程式。")
    #         sys.exit(1)
    #     else:
    #         print("請輸入 Y 或 N！")

def prompt_no_cover(url):
    print("\n失敗：此動畫沒有封面。")
    print("網址：")
    print(url)
    print("退出程式")
    sys.exit(1)

def check_mp4_exist(path):
    if not os.path.isfile(path):
        print("找不到 MP4 檔欸，是不是檔名打錯了？")
        print("檔名：")
        print(path)
        print("退出程式")
        sys.exit(1)

def is_dir(path):
    if os.path.isdir(path):
        return True
    return "資料夾無效、或是並非資料夾。"

def is_file(path):
    if os.path.isfile(path):
        return True
    return "檔案無效、或是並非檔案。"

def write_pic(path, mode, vi_or_co: str):
    try:
        with open (path, mode) as f:
            if vi_or_co == "visual":
                f.write(ep.visual_data)
            elif vi_or_co == "cover":
                f.write(ep.cover_data)
            # need?
            # else:
            #     raise SyntaxError
    except Exception as err:
        print("儲存縮圖時出錯，詳情：")
        print(err)
        print("退出程式")
        sys.exit(1)

def ensure_folder_exists(path:str) -> None:
    if os.path.exists(path):
        return None
    # else:
    print("指定資料夾不存在：")
    print('\t' + path)
    if "args" in globals() and args.dont_make_directory:
        print("退出程式")
        sys.exit(1)
    else:
        print("開始建立資料夾")
        try:
            os.makedirs(path)
        except Exception as err:
            print("建立資料夾時出錯，詳情：")
            print(err)
            print("退出程式")
            sys.exit(1)

def determine_path(arg, file_name:str) -> str:
    global FOLDER_PATH
    if arg:
        parent = os.path.dirname(arg)
        ensure_folder_exists(parent)
        return arg
    # use -d argument
    if FOLDER_PATH:
        return os.path.join(FOLDER_PATH, file_name)
    if args.directory:
        if os.path.isfile(args.directory):
            print("\n-d 後請加資料夾路徑，而非檔案！")
            print("退出程式")
            sys.exit(1)

        ensure_folder_exists(args.directory)
        if os.path.isdir(args.directory):
            FOLDER_PATH = args.directory
            return os.path.join(args.directory, file_name)
        else:
            print("資料夾無效。路徑：")
            print(args.directory)
            print("退出程式")
            sys.exit(1)
    elif args.mp4:
        FOLDER_PATH = os.path.dirname(args.mp4)
        return os.path.join(FOLDER_PATH, file_name)
    else:
        print("請指定檔案要儲存至何處！")
        print("退出程式")
        sys.exit(1)

def check_sn_format(sn_or_url):
    if len(sn_or_url) > 7 or sn_or_url.isnumeric():
        return True
    return "格式錯誤！範例 sn 碼：16231  範例網址：https://ani.gamer.com.tw/animeVideo.php?sn=16231"

def valid_path(path:str, fname:str) -> str:
    if os.path.isdir(path):
        ensure_folder_exists(path)
        return os.path.join(path, fname)
    else:
        ensure_folder_exists(os.path.dirname(path))
        return path

if len(sys.argv) > 1:
    parser = argparse.ArgumentParser(
        description="使用範例：%(prog)s 16231 -m /home/zica/cover/m.mp4 -c -d /home/zica/cover --download-cover --download-visual\n會把Lapis Re：LiGHTs [1]的封面嵌入到/home/zica/cover/m.mp4，並且把封面圖和視覺圖下載到/home/zica/cover。",
        epilog=f"GitHub repo 網址：https://github.com/zica87/embed-ani-gamer-covers\n版本：{VERSION}",
        formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("url",
                        metavar="sn 碼或網址",
                        help="請在以下選項前面先輸入動畫的 sn 碼或網址。")
    parser.add_argument("-m",
                        "--mp4",
                        metavar="檔名",
                        help="要嵌入縮圖的 MP4 檔名。")
    parser.add_argument("-v",
                        "--embed-visual",
                        action="store_true",
                        help="嵌入視覺圖。")
    parser.add_argument("-c",
                        "--embed-cover",
                        action="store_true",
                        help="嵌入封面。\n也指定「嵌入視覺圖」選項的話則會檢查有無封面，\n有封面的話就嵌入封面，沒有的話就嵌入視覺圖。")
                        #     嵌入封面。
                        #     也指定「嵌入視覺圖」選項的話則會檢查有無封面，
                        #     有封面的話就嵌入封面，沒有的話就嵌入視覺圖。
    parser.add_argument("-d",
                        "--directory",
                        "--folder",
                        metavar="資料夾",
                        help="下載下來的圖片要儲存到的資料夾，僅嵌入不下載的話免填。\n要下載但不填的話表示與 MP4 檔同資料夾。")
                        #     下載下來的圖片要儲存到的資料夾，僅嵌入不下載的話免填。
                        #     要下載但不填的話表示與 MP4 檔同資料夾。")
    parser.add_argument("--download-visual",
                        nargs='?',
                        default="not chose",
                        metavar="檔名（含路徑）",
                        help="下載視覺圖。\n後面接要儲存的檔名（含路徑），\n不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。")
                        #     下載視覺圖。
                        #     後面接要儲存的檔名（含路徑），
                        #     不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。"
    parser.add_argument("--download-cover",
                        nargs='?',
                        default="not chose",
                        metavar="檔名（含路徑）",
                        help="下載封面。\n後面接要儲存的檔名（含路徑），\n不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。")
                        #     下載封面。
                        #     後面接要儲存的檔名（含路徑），
                        #     不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。"
    parser.add_argument("--metadata",
                        nargs='?',
                        default="not chose",
                        metavar="檔名（含路徑）",
                        help="以 TOML 格式儲存動畫資訊。\n後面接要儲存的檔名（含路徑），\n不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。")
                        #     以 TOML 格式儲存動畫資訊。
                        #     後面接要儲存的檔名（含路徑），
                        #     不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。"
    overw_group = parser.add_mutually_exclusive_group()
    overw_group.add_argument("--overwrite",
                        action="store_true",
                        help="若已有與要儲存的檔案同名的檔案就覆寫。")
    overw_group.add_argument("--no-overwrite",
                        action="store_true",
                        help="若已有與要儲存的檔案同名的檔案就退出程式，不覆寫。")
    parser.add_argument("--dont-make-directory",
                        "--dont-make-folder",
                        action="store_true",
                        help="不存在指定資料夾時不建立資料夾，直接退出程式。")
    parser.add_argument("--version",
                        action="version",
                        version=VERSION,
                        help="顯示版本號碼。")

    args = parser.parse_args()
    #print(args)

    FOLDER_PATH = None

    # 僅輸入 sn 碼（而非網址）
    if len(args.url) < 7:
        if args.url.isnumeric():
            args.url = "https://ani.gamer.com.tw/animeVideo.php?sn=" + args.url
        else:
            print("格式錯誤！")
            print(f"您輸入的 sn 碼：{args.url}")
            print("\n範例 sn 碼：16231")
            print("範例網址：https://ani.gamer.com.tw/animeVideo.php?sn=16231")
            print("退出程式")
            sys.exit(1)

    if args.mp4:
        check_mp4_exist(args.mp4)

    try:
        ep = Episode(args.url)
        # show title first
        ep.title
    except FileNotFoundError:
        print(f"找不到此網址的動畫：\n{args.url}")
        # 找不到此網址的動畫：
        # https://ani.gamer.com.tw/animeVideo.php?sn=1
        print("退出程式")
        sys.exit(1)


    # write metadata
    if args.metadata != "not chose":
        metadata_file_path = determine_path(
            args.metadata, f"{ep.title} 資訊.toml")
        mode = file_write_mode(metadata_file_path)
        print("開始儲存動畫資訊")
        try:
            with open(metadata_file_path, mode) as f:
                tomli_w.dump(ep.metadata_as_dict(), f)
        except Exception as err:
            print("儲存動畫資訊時出錯，詳情：")
            print(err)
            print("退出程式")
            sys.exit(1)


    # embedding
    if args.embed_cover:
        if not args.mp4:
            print("\n請提供 MP4 檔名。")
            print("退出程式")
            sys.exit(1)
        if ep.cover_url != ep.visual_url:
            print("開始嵌入封面")
            embed(ep.cover_data, args.mp4)
        elif args.embed_visual:
            print("\n此動畫沒有封面。")
            print("開始嵌入視覺圖")
            embed(ep.visual_data, args.mp4)
        else:
            prompt_no_cover(args.url)
    elif args.embed_visual:
        if not args.mp4:
            print("\n請提供 MP4 檔名。")
            print("退出程式")
            sys.exit(1)
        print("開始嵌入視覺圖")
        embed(ep.visual_data, args.mp4)


    # downloading

    # "not chose" is default value, so user didn't choose
    if args.download_cover != "not chose":
        # 確定有封面
        if ep.cover_url != ep.visual_url:
            cover_file_path = determine_path(args.download_cover,
                                             f"{ep.title}.jpg")
            # 無同名檔案、或有同名檔案但使用者決定覆寫
            mode = file_write_mode(cover_file_path)
            print("開始儲存動畫封面")
            write_pic(cover_file_path, mode, "cover")
        elif args.download_visual != "not chose":
            print("\n失敗：此動畫沒有封面。")
        else:
            prompt_no_cover(args.url)

    if args.download_visual != "not chose":
        visual_file_path = determine_path(args.download_visual,
                                          f"{ep.series_title} 視覺圖.jpg")

        # 無同名檔案、或有同名檔案但使用者決定覆寫
        mode = file_write_mode(visual_file_path)
        print("開始儲存動畫視覺圖")
        write_pic(visual_file_path, mode, "visual")


else:
    print("未選擇選項（引數），因此進入互動模式")

    while True:
        url = questionary.text("請輸入 sn 碼或網址：", validate=check_sn_format).ask()

        if len(url) < 7:
            url = "https://ani.gamer.com.tw/animeVideo.php?sn=" + url

        try:
            ep = Episode(url)
            # show title first
            ep.title
        except FileNotFoundError:
            print(f"找不到此網址的動畫：\n{url}")
            # 找不到此網址的動畫：
            # https://ani.gamer.com.tw/animeVideo.php?sn=1
        else:
            break


    task = questionary.select("請選擇要程式做的事情：",
                              instruction="（按方向鍵上／下選擇）",
                              choices=["嵌入視覺圖",
                                       "嵌入封面",
                                       "下載視覺圖",
                                       "下載封面",
                                       "儲存動畫資訊"
                                      ]).ask()

    match task:
        case "嵌入視覺圖":
            mp4 = questionary.path("請輸入要嵌入封面的 MP4 檔：\n",
                                   validate = is_file,
                                   file_filter = is_file
                                  ).ask()
            embed(ep.visual_data, mp4)
        case "嵌入封面":
            mp4 = questionary.path("請輸入要嵌入封面的 MP4 檔：\n",
                                   validate = is_file,
                                   file_filter = is_file
                                  ).ask()
            if ep.cover_url != ep.visual_url:
                embed(ep.cover_data, mp4)
            elif questionary.confirm("此集沒有封面欸，要嵌入視覺圖嗎？").ask():
                embed(ep.visual_data, mp4)
            else:
                prompt_no_cover(url)
        case "下載視覺圖":
            path = questionary.path("請輸入下載下來的圖片要儲存到哪個資料夾（或直接指定檔名）：\n",
                                    only_directories = True
                                   ).ask()
            path = valid_path(path, ep.series_title + " 視覺圖.jpg")
            mode = file_write_mode(path)
            print("開始儲存動畫視覺圖")
            write_pic(path, mode, "visual")
        case "下載封面":
            path = questionary.path("請輸入下載下來的圖片要儲存到哪個資料夾（或直接指定檔名）：\n",
                                    only_directories = True
                                    ).ask()
            if ep.cover_url != ep.visual_url:
                path = valid_path(path, ep.title + ".jpg")
                mode = file_write_mode(path)
                print("開始儲存動畫封面")
                write_pic(path, mode, "cover")
            elif questionary.confirm("此集沒有封面欸，要下載視覺圖嗎？").ask():
                path = valid_path(path, ep.series_title + " 視覺圖.jpg")
                mode = file_write_mode(path)
                print("開始儲存動畫視覺圖")
                write_pic(path, mode, "visual")
            else:
                prompt_no_cover(url)
        case "儲存動畫資訊":
            path = questionary.path("請輸入要儲存到哪個資料夾（或直接指定檔名）：\n",
                                    only_directories = True
                                    ).ask()
            path = valid_path(path, ep.title + " 資訊.toml")
            mode = file_write_mode(path)
            print("開始儲存動畫資訊")
            try:
                with open(path, mode) as f:
                    tomli_w.dump(ep.metadata_as_dict(), f)
            except Exception as err:
                print("儲存動畫資訊時出錯，詳情：")
                print(err)
                print("退出程式")
                sys.exit(1)



print("順利完成！")
