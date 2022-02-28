<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);
$mode = "입력";
$action = "stadium_insert.php";

if (array_key_exists("stadium_id", $_GET)) { //수정 모드
    $stadium_id = $_GET["stadium_id"];
    $query =  "select * from stadium where stadium_id = $stadium_id";
    $res = mysqli_query($conn, $query);
    $stadium = mysqli_fetch_array($res);
    if(!$stadium) {
        msg("구장이 존재하지 않습니다."); //수정 누르기 전에 관리자가 삭제한게 아니라면 이 경우는 거의 존재하지 않음
    }
    $mode = "수정";
    $action = "stadium_modify.php";
}

$res = mysqli_query($conn, $query);
while($row = mysqli_fetch_array($res)) {
	$stadium[$row['stadium_id']] = $row['stadium_name'];
}

?>
    <div class="container">
        <form name="stadium_register" action="<?=$action?>" method="post" class="fullwidth">
            <input type="hidden" name="stadium_id" value="<?=$stadium['stadium_id']?>"/>
            <h3>구단 정보 <?=$mode?></h3>
            <p>
                <label for="stadium_name">구장 이름</label>
                <input type="text" placeholder="이름 입력" id='stadium_name' name="stadium_name" value="<?=$stadium['stadium_name']?>"/>
            </p>

            <p>
                <label for="constructed_year">설립 연도</label>
                <input type="text" placeholder="연도만 입력(ex.1998)" id='constructed_year' name="constructed_year" value="<?=$stadium['constructed_year']?>" />
            </p>
            
            <p>
                <label for="capacity">수용 인원</label>
                <input type="text" placeholder="수용 인원 입력" id="capacity" name="capacity" value="<?=$stadium['capacity']?>" />
            </p>

            <p>
                <label for="place">위 치</label>
                <input type="text" placeholder="위치 입력(도시만)" id="place" name="place" value="<?=$stadium['place']?>" />
            </p>
            
            <p align="center"><button class="button primary large" onclick="javascript:return validate();"><?=$mode?></button></p>

            <script>
                function validate() {
                    if(document.getElementById("stadium_name").value == "") {
                        alert ("구장 명을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("constructed_year").value == "") {
                        alert ("설립 연도를 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("capacity").value == "") {
                        alert ("수용 인원을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("place").value == "") {
                        alert ("위치를 입력해 주십시오"); return false;
                    }
                    return true;
                }
            </script>

        </form>
    </div>
<? include("footer.php") ?>