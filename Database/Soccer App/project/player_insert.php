<?php
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host,$dbid,$dbpass,$dbname);

$player_name = $_POST['player_name'];
$nationality = $_POST['nationality'];
$age = $_POST['age'];
$team_id = $_POST['team_id'];
$strong_foot = $_POST['strong_foot'];
$rating = $_POST['rating'];
$price = $_POST['price'];

$ret = mysqli_query($conn, "insert into player (player_name, nationality, age, team_id, strong_foot, rating, price) values('$player_name', '$nationality', '$age', '$team_id', '$strong_foot', '$rating','$price')");
if(!$ret)
{
	echo mysqli_error($conn);
    msg('Query Error : '.mysqli_error($conn));
}
else
{
    s_msg ('성공적으로 입력 되었습니다');
    echo "<meta http-equiv='refresh' content='0;url=player_list.php'>";
}

?>


