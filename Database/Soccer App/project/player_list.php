<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수
?>
<div class="container">
    <?
    $conn = dbconnect($host, $dbid, $dbpass, $dbname);
    $query = "select * from team natural join player natural join evaluation";
    if (array_key_exists("search_keyword", $_POST)) {  // array_key_exists() : Checks if the specified key exists in the array
        $search_keyword = $_POST["search_keyword"];
        $query =  $query . " where player_name like '%$search_keyword%'";
    
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
            <th>선수 이름</th>
            <th>국적</th>
            <th>소속팀</th>
            <th>나이</th>
            <th>평점</th>
            <th>기능</th>
        </tr>
        </thead>
        <tbody>
        <?
        $row_index = 1;
        while ($row = mysqli_fetch_array($res)) {
            echo "<tr>";
            echo "<td>{$row_index}</td>";
            echo "<td><a href='player_view.php?player_id={$row['player_id']}'>{$row['player_name']}</a></td>"; //hypertext reference를 통해서 자세히 들여다보기
            echo "<td>{$row['nationality']}</td>";
            echo "<td><a href='team_view.php?team_id={$row['team_id']}'>{$row['team_name']}</a></td>"; //hypertext reference를 통해서 자세히 들여다보기
            echo "<td>{$row['age']}</td>";
            echo "<td><a href='evaluation_view.php?rating={$row['rating']}'>{$row['rating']}</a></td>";
            echo "<td width='17%'>
                <a href='player_register.php?player_id={$row['player_id']}'><button class='button primary small'>수정</button></a>
                 <button onclick='javascript:deleteConfirm({$row['player_id']})' class='button danger small'>삭제</button>
                </td>";
            echo "</tr>";
            $row_index++;
        }
        ?>
        </tbody>
    </table>
    <center><div><h4><a href = 'player_register.php'>축구선수 등록하기</a></h4></div></center>
    <script>
        function deleteConfirm(player_id) {
            if (confirm("정말 삭제하시겠습니까?") == true){    //확인
                window.location = "player_delete.php?player_id=" + player_id;
            }else{   //취소
                return;
            }
        }
    </script>
</div>
<? include("footer.php") ?>
