<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);

if (array_key_exists("stadium_id", $_GET)) {
    $stadium_id = $_GET["stadium_id"];
    $query = "select * from stadium where stadium_id = $stadium_id";
    $res = mysqli_query($conn, $query);
    $stadium = mysqli_fetch_assoc($res);
    if (!$stadium) {
        msg("해당 구장이 존재하지 않습니다.");
    }
}
?>
    <div class="container fullwidth">

        <h3>구장 정보 상세 보기</h3>

        <p>
            <label for="stadium_id">구장 번호</label>
            <input readonly type="text" id="stadium_id" name="stadium_id" value="<?= $stadium['stadium_id'] ?>"/>
        </p>

        <p>
            <label for="stadium_name">구장 명</label>
            <input readonly type="text" id="stadium_name" name="stadium_name" value="<?= $stadium['stadium_name'] ?>"/>
        </p>
        
        <p>
            <label for="constructed_year">설립 연도</label>
            <input readonly type="text" id="constructed_year" name="constructed_year" value="<?= $stadium['constructed_year'] ?>"/>
        </p>

        <p>
            <label for="capacity">수용인원</label>
            <input readonly type="text" id="capacity" name="capacity" value="<?= $stadium['capacity'] ?>"/>
        </p>

        <p>
            <label for="place">위 치</label>
            <input readonly type="text" id="place" name="place" value="<?= $stadium['place'] ?>"/>
        </p>
       
    </div>
<? include("footer.php") ?>