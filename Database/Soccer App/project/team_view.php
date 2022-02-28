<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);

if (array_key_exists("team_id", $_GET)) {
    $team_id = $_GET["team_id"];
    $query = "select * from team natural join stadium where team_id = $team_id";
    $res = mysqli_query($conn, $query);
    $team = mysqli_fetch_assoc($res);
    if (!$team) {
        msg("해당 구단이 존재하지 않습니다.");
    }
}
?>
    <div class="container fullwidth">

        <h3>구단 정보 상세 보기</h3>

        <p>
            <label for="team_id">구단 번호</label>
            <input readonly type="text" id="team_id" name="team_id" value="<?= $team['team_id'] ?>"/>
        </p>

        <p>
            <label for="team_name">구단 명</label>
            <input readonly type="text" id="team_name" name="team_name" value="<?= $team['team_name'] ?>"/>
        </p>

        <p>
            <label for="manager">감 독</label>
            <input readonly type="text" id="manager" name="manager" value="<?= $team['manager'] ?>"/>
        </p>
        
        <p>
            <label for="president">회 장</label>
            <input readonly type="text" id="president" name="president" value="<?= $team['president'] ?>"/>
        </p>
        
        <p>
            <label for="found_date">창 단</label>
            <input readonly type="text" id="found_date" name="found_date" value="<?= $team['found_date'] ?>"/>
        </p>

        <p>
            <label for="league_name">소속 리그</label>
            <input readonly type="text" id="league_name" name="league_name" value="<?= $team['league_name'] ?>"/>
        </p>
        
        <p>
            <label for="stadium_name">홈구장</label>
            <input readonly type="text" id="stadium_name" name="stadium_name" value="<?= $team['stadium_name'] ?>"/>
        </p>
        
        <p>
            <label for="place">위치</label>
            <input readonly type="text" id="place" name="place" value="<?= $team['place'] ?>"/>
        </p>
    </div>
<? include("footer.php") ?>