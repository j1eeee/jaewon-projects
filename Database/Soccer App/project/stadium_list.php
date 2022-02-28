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
