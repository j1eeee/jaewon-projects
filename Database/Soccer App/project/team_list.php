<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수
?>
<div class="container">
    <?
    $conn = dbconnect($host, $dbid, $dbpass, $dbname);
    $query = "select * from team natural join stadium";
    if (array_key_exists("search_keyword", $_POST)) {  // array_key_exists() : Checks if the specified key exists in the array
        $search_keyword = $_POST["search_keyword"];
        $query =  $query . " where team_name like '%$search_keyword%'";
    
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
            <th>구단 이름</th>
            <th>홈구장</th>
            <th>소속 리그</th>
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
            echo "<td><a href='team_view.php?team_id={$row['team_id']}'>{$row['team_name']}</a></td>";
            echo "<td><a href='stadium_view.php?stadium_id={$row['stadium_id']}'>{$row['stadium_name']}</a></td>";
            echo "<td><a href='league_view.php?league_name={$row['league_name']}'>{$row['league_name']}</a></td>";
            echo "<td>{$row['place']}</td>";
            echo "<td width='17%'>
                <a href='team_register.php?team_id={$row['team_id']}'><button class='button primary small'>수정</button></a>
                 <button onclick='javascript:deleteConfirm({$row['team_id']})' class='button danger small'>삭제</button>
                </td>";
            echo "</tr>";
            $row_index++;
        }
        ?>
        </tbody>
    </table>
    	<center><div>
    		<h4><a href = 'team_register.php'>구단 등록하기</a></h4>
    			</div></center>
    <script>
        function deleteConfirm(team_id) {
            if (confirm("정말 삭제하시겠습니까?") == true){    //확인
                window.location = "team_delete.php?team_id=" + team_id;
            }else{   //취소
                return;
            }
        }
    </script>
</div>
<? include("footer.php") ?>
