<?php
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host,$dbid,$dbpass,$dbname);

$player_id = $_POST['player_id'];
$player_name = $_POST['player_name'];
$nationality = $_POST['nationality'];
$age = $_POST['age'];
$team_id = $_POST['team_id'];
$rating = $_POST['rating'];
$price = $_POST['price'];

$ret = mysqli_query($conn, "update player set player_name = '$player_name', nationality = '$nationality', age = $age, team_id = $team_id, rating = $rating, price = '$price' where player_id = $player_id");

if(!$ret)
{
    msg('Query Error : '.mysqli_error($conn));
}
else
{
    s_msg ('성공적으로 수정 되었습니다');
    echo "<meta http-equiv='refresh' content='0;url=player_list.php'>";
}

?>
