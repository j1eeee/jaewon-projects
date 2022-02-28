<?php
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host,$dbid,$dbpass,$dbname);

$stadium_id = $_POST['stadium_id'];
$stadium_name = $_POST['stadium_name'];
$constructed_year = $_POST['constructed_year'];
$capacity = $_POST['capacity'];
$place = $_POST['place'];

$ret = mysqli_query($conn, "update stadium set stadium_name = '$stadium_name', constructed_year = '$constructed_year', capacity = $capacity, place = '$place' where stadium_id = $stadium_id");

if(!$ret)
{
    msg('Query Error : '.mysqli_error($conn));
}
else
{
    s_msg ('성공적으로 수정 되었습니다');
    echo "<meta http-equiv='refresh' content='0;url=stadium_list.php'>";
}

?>

