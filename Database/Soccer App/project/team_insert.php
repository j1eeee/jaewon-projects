<?php
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host,$dbid,$dbpass,$dbname);

$team_name = $_POST['team_name'];
$manager = $_POST['manager'];
$president = $_POST['president'];
$found_date = $_POST['found_date'];
$league_name = $_POST['league_name'];
$stadium_id = $_POST['stadium_id'];

$ret = mysqli_query($conn, "insert into team (team_name, manager, president, found_date, league_name, stadium_id) values('$team_name', '$manager', '$president', '$found_date', '$league_name','$stadium_id')");
if(!$ret)
{
	echo mysqli_error($conn);
    msg('Query Error : '.mysqli_error($conn));
}
else
{
    s_msg ('성공적으로 입력 되었습니다');
    echo "<meta http-equiv='refresh' content='0;url=team_list.php'>";
}

?>


