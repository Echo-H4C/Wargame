# 1. 웹페이지

해당 문제의 웹페이지에 접속 시 Hello 라는 문자열이 출력되고 이외의 기능은 보이지 않아 바로 소스코드를 보고 문제를 풀기로 하였다.

![image](./images/1_수정.png)

# 2. 소스코드 분석

![image](./images/2_수정.png)

소스코드를 보니 메인 페이지 이외에 /fetch 엔드포인트가 있는 것을 확인하였다. 자세한 기능을 분석하기 이전에 간단히 살펴보면 요청 시 url 파라미터를 통해 입력값을 받는 것을 확인할 수 있다.

![image](./images/3_수정.png)

출력결과를 보니 다시 메인 페이지가 출력된다. 우리가 url 파라미터에 입력한 값이 어떻게 이용되는지 알아보기 위해 /fetch 엔드포인트의 소스코드를 상세히 분석하였다.

```javascript
1 app.get("/fetch", async (req, res) => {
2  const url = req.query.url;
3
4  if (!url) return res.send("?url=<br>ex) http://localhost:3000/");
5
6  let host;
7  try {
8    const urlObject = new URL(url);
9    host = urlObject.hostname;
10
11    if (host !== "localhost" && !host.endsWith("localhost")) return res.send("rejected");
12  } catch (error) {
13    return res.send("Invalid Url");
14  }
15
16  try {
17    let result = await node_fetch(url, {
18      method: "GET",
19      headers: { "Cookie": `FLAG=${FLAG}` },
20    });
21    const data = await result.text();
22    res.send(data);
23  } catch {
24    return res.send("Request Failed");
25  }
