<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);

if (array_key_exists("league_name", $_GET)) {
    $league_name = $_GET["league_name"];
    $query = "select * from league where league_name = '$league_name'";
    $res = mysqli_query($conn, $query);
    $league = mysqli_fetch_assoc($res);
    if (!$league) {
        msg("해당 리그가 존재하지 않습니다.");
    }
}
?>
    <div class="container fullwidth">

        <h3>리그 정보 상세 보기</h3>

        <p>
            <label for="league_name">리그 명</label>
            <input readonly type="text" id="league_name" name="league_name" value="<?= $league['league_name'] ?>"/>
        </p>

        <p>
            <label for="country">소속 국가</label>
            <input readonly type="text" id="country" name="country" value="<?= $league['country'] ?>"/>
        </p>
       
    </div>
<? include("footer.php") ?>