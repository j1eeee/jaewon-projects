<?php
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수
/*
Requirements: 시스템 구현 요구사항 및 설계 내역의 반영 정도(10점)
Details: 정보(데이터) 및 기능의 상세 정도(10점)
Completeness: 시스템의 완성도(오류 발생 정도)(10점)
Usability: 사용자가 시스템을 얼마나 잘 편리하게 사용할 수 있는가의 측면(5점)*/

$conn = dbconnect($host,$dbid,$dbpass,$dbname);

$player_name = $_POST['player_name'];
$nationality = $_POST['nationality'];
$age = $_POST['age'];
$team_id = $_POST['team_id'];
$strong_foot = $_POST['strong_foot'];
$rating = $_POST['rating'];
$price = $_POST['price'];

mysqli_query($conn, "set autocommit = 0"); // autocommit 해제
mysqli_query($conn, "set transaction isolation level serializable"); //isolation level 최고 단계
mysqli_query($conn, "begin");

$ret = mysqli_query($conn, "insert into player (player_name, nationality, age, team_id, strong_foot, rating, price) values('$player_name', '$nationality', '$age', '$team_id', '$strong_foot', '$rating','$price')");
if(!$ret)
{
	mysqli_error($conn, "rollback");
    msg('Query Error : '.mysqli_error($conn));
}
else 
{
	$player_id = mysqli_insert_id($conn);
	mysqli_query($conn, "commit");
    s_msg ('성공적으로 입력 되었습니다');
    echo "<meta http-equiv='refresh' content='0;url=player_list.php'>";
}

?>

<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수
?>
<div class="container">
    <?
    $conn = dbconnect($host, $dbid, $dbpass, $dbname);
    $query = "select * from stadium";
    if (array_key_exists("search_keyword", $_POST)) {  // array_key_exists() : Checks if the specified key exists in the array
        $search_keyword = $_POST["search_keyword"];
        $query =  $query . " where stadium_name like '%$search_keyword%'";
    
    }
    $res = mysqli_query($conn, $query);
    if (!$res) {
         die('Query Error : 검색어를 다시 입력해주세요.' . mysqli_error());
    }
    ?>

    <table class="table table-striped table-bordered">
        <thead>
        <tr>
            <th>No.</th>
            <th>구장 이름</th>
            <th>시공 년도</th>
            <th>수용 인원</th>
            <th>위치</th>
            <th>기능</th>
        </tr>
        </thead>
        <tbody>
        <?
        $row_index = 1;
        while ($row = mysqli_fetch_array($res)) {
            echo "<tr>";
            echo "<td>{$row_index}</td>";
            echo "<td><a href='stadium_view.php?stadium_id={$row['stadium_id']}'>{$row['stadium_name']}</a></td>";
            echo "<td>{$row['constructed_year']}</td>";
            echo "<td>{$row['capacity']}</td>";
            echo "<td width='17%'>
                <a href='stadium_register.php?stadium_id={$row['stadium_id']}'><button class='button primary small'>수정</button></a>
                 <button onclick='javascript:deleteConfirm({$row['stadium_id']})' class='button danger small'>삭제</button>
                </td>";
            echo "</tr>";
            $row_index++;
        }
        ?>
        </tbody>
    </table>
    	<center><div>
    		<h4><a href = 'stadium_register.php'>구장 등록하기</a></h4>
    			</div></center>
    <script>
        function deleteConfirm(stadium_id) {
            if (confirm("정말 삭제하시겠습니까?") == true){    //확인
                window.location = "stadium_delete.php?stadium_id=" + stadium_id;
            }else{   //취소
                return;
            }
        }
    </script>
</div>
<? include("footer.php") ?>


