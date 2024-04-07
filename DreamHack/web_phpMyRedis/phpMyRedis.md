<h1>1. 웹 페이지 분석</h1>

 

<메인>
![image](./image/phpMyRedis1.png)



접속한 첫 페이지에서는 입력을 받을 수 있는 공간이 있고 그 아래에 save 체크박스, submit 버튼, 그리고 Command History 가 있다. 그리고 오른쪽에는 Reset 링크가 있다. 

 

Command 에서 아무거나 입력하고 submit 하니 Command History 에 기록이 남는다.

 

그리고 우측 상단에는 Config 링크가 있는데 이 링크를 클릭하면 다른 페이지로 이동하게 된다.

 

<config>

![image](./image/phpMyRedis2.png)



이 페이지에는 GET,SET 을 선택할 수 있으며, key 와 value 를 입력하고 submit을 통해 값을 전송한다.

 
<h1>2. 코드 분석</h1>


첫 페이지인 index.php 코드의 일부를 가져왔다.


```
<?php 
if(isset($_POST['cmd'])){ // cmd
$redis = new Redis(); // redis 연동.
$redis->connect($REDIS_HOST); //REDIS_HOST 에 연결
$ret = json_encode($redis->eval($_POST['cmd']));
echo '<h1 class="subtitle">Result</h1>';
echo "<pre>$ret</pre>";
if (!array_key_exists('history_cnt', $_SESSION)) { // array_key_exists("확인하고자 하는 키",[배열명]) : 배열의 키가 존재하는지 확인하는 함수. 
배열이 키를 가지고 있으면 1을 반환하고, 그렇지 않다면 아무것도 반환하지 않는다.
	$_SESSION['history_cnt'] = 0;
}
$_SESSION['history_'.$_SESSION['history_cnt']] = $_POST['cmd'];
$_SESSION['history_cnt'] += 1;
             
if(isset($_POST['save'])) { // save 체크박스에 체크했을 때
	$path = './data/'. md5(session_id());
	$data = '> ' . $_POST['cmd'] . PHP_EOL . str_repeat('-',50) . PHP_EOL . $ret; // PHP_EOL : 줄바꿈, str_repeat('반복할 문자열',횟수) : 문자열 반복
	file_put_contents($path, $data); // file_put_contents("파일명","파일에 작성할 내용") : 파일에 내용을 작성
	echo "saved at : <a target='_blank' href='$path'>$path</a>";
	}
}
?>
```

