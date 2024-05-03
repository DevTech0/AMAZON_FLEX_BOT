import requests, authCycle
import header_data
import signature_headers


def amz_request(method: str, url: str, json: dict=None, session: requests.Session=None, sign_request=False) -> requests.Response:
    print("url is ", url)
    if session:
        req = session.get if method == "get" else session.post
    else:
        req = requests.get if method == "get" else requests.post
    authCycle.requestId_refresh()
    headers = header_data.headers.copy()
    if url.endswith("AcceptOffer"):
        print("accepting offer")
        try:
            print("headers are ", headers)
            sig_req = requests.get(f'https://proxyserver-1.onrender.com/accept/357f7bab-25ed-4fdb-a8e5-a7b3a9f97411/{headers["x-amzn-marketplace-id"]}')

            print("sig_req is ", sig_req)
            sig_req = sig_req.json()
            headers["Signature"] = sig_req["signature"]
            headers["Signature-Input"] = sig_req["signature_input"]
            headers["User-Agent"] = sig_req["user_agent"]
        except Exception as e:
            print("exception occur: ",e)
    if url.endswith("GetOffersForProviderPost"):
        headers["Connection"] = "close"
        headers["X-Amzn-Identity-Auth-Domain"] = ".amazon.com"
    if url.endswith('ValidateChallenge'):
        print("validating challenge")
        try:
            sig_req = sig_req = requests.get(f'https://proxyserver-1.onrender.com/challenge/357f7bab-25ed-4fdb-a8e5-a7b3a9f97411/{headers["x-amzn-marketplace-id"]}')

            print("sig_req is ", sig_req)
            headers["Signature"] = sig_req["signature"]
            headers["Signature-Input"] = sig_req["signature_input"]
            headers["User-Agent"] = sig_req["user_agent"]
        except Exception as e:
            print("exception occur: ",e)

    res = req(url, headers=headers, json=json)
    print(res.status_code, res.text)

    if res.status_code == 403:
        authCycle.header_refresh()
        authCycle.requestId_refresh()
        headers = header_data.headers.copy()
        if sign_request:
            headers.update(signature_headers.signature_headers)
        res = req(url, headers=headers, json=json)
    
    if  url.endswith("ValidateChallenge"):
        print("accepting offer")
        print(res.status_code, res.text)
    return res